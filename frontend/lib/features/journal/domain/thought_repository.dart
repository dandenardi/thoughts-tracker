import 'thought_entry.dart';

abstract class ThoughtRepository {
  Future<List<ThoughtEntry>> list();
  Future<ThoughtEntry> getById(String id);
  Future<ThoughtEntry> create(ThoughtEntry entry);
  Future<void> delete(String id);
}
