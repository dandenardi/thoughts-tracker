import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thoughts_tracker/features/journal/domain/thought_repository.dart';

final thoughtRepoProvider = Provider<ThoughtRepository>((ref) {
  throw UnimplementedError("Override me in main()");
});
