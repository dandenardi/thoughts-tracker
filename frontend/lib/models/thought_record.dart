import 'emotion.dart';
import 'symptom.dart';

class ThoughtRecord {
  final String? id;
  final String? userId;
  final String? timestamp;
  final String title;
  final String? situationDescription;
  final Emotion? emotion;
  final List<Symptom> symptoms;
  final String? underlyingBelief;

  ThoughtRecord({
    this.id,
    this.userId,
    this.timestamp,
    required this.title,
    this.situationDescription,
    required this.emotion,
    required this.symptoms,
    this.underlyingBelief,
  });

  factory ThoughtRecord.fromJson(Map<String, dynamic> json) {
    return ThoughtRecord(
      id: json['id'],
      userId: json['userId'],
      timestamp: json['timestamp'],
      title: json['title'],
      situationDescription: json['situationDescription'],
      emotion:
          json['emotion'] != null ? Emotion.fromJson(json['emotion']) : null,
      symptoms:
          (json['symptoms'] as List<dynamic>)
              .map((s) => Symptom.fromJson(s))
              .toList(),
      underlyingBelief: json['underlying_belief'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'situation_description': situationDescription,
      'emotion': emotion?.toJson(),
      'symptoms': symptoms.map((s) => s.toJson()).toList(),
      'underlying_belief': underlyingBelief,
    };
  }
}
