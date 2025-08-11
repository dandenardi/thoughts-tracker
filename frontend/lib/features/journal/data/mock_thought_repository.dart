import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import 'package:uuid/uuid.dart';
import '../domain/thought_entry.dart';
import '../domain/thought_repository.dart';

class MockThoughtRepository implements ThoughtRepository {
  final List<ThoughtEntry> _db;
  final Duration latency;
  final double errorRate; // 0.0–1.0

  MockThoughtRepository(
    this._db, {
    this.latency = const Duration(milliseconds: 250),
    this.errorRate = 0.0,
  });

  static Future<MockThoughtRepository> fromAsset(
    String path, {
    Duration latency = const Duration(milliseconds: 250),
    double errorRate = 0.0,
  }) async {
    final jsonStr = await rootBundle.loadString(path);
    final list =
        (json.decode(jsonStr) as List)
            .map((e) => ThoughtEntry.fromJson(Map<String, dynamic>.from(e)))
            .toList();
    return MockThoughtRepository(list, latency: latency, errorRate: errorRate);
  }

  Future<T> _withLatency<T>(T Function() body) async {
    await Future.delayed(latency);
    if (errorRate > 0 && _hit()) throw Exception('Mock error');
    return body();
  }

  bool _hit() {
    final n = (1 / errorRate).round();
    return n > 0 ? DateTime.now().microsecond % n == 0 : false;
  }

  @override
  Future<List<ThoughtEntry>> list() =>
      _withLatency(() => List.unmodifiable(_db));

  @override
  Future<ThoughtEntry> getById(String id) =>
      _withLatency(() => _db.firstWhere((e) => e.id == id));

  @override
  Future<ThoughtEntry> create(ThoughtEntry entry) => _withLatency(() {
    final e = ThoughtEntry(
      id: const Uuid().v4(),
      date: entry.date,
      situation: entry.situation,
      thought: entry.thought,
      emotions: entry.emotions,
      intensity: entry.intensity,
      behavior: entry.behavior,
      tags: entry.tags,
      distortions: entry.distortions,
    );
    _db.add(e);
    return e;
  });

  @override
  Future<void> delete(String id) => _withLatency(() {
    _db.removeWhere((e) => e.id == id);
  });
}
