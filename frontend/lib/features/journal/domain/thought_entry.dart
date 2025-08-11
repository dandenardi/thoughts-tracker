class ThoughtEntry {
  final String id;
  final DateTime date;
  final String situation;
  final String thought;
  final List<String> emotions;
  final int intensity;
  final String? behavior;
  final List<String> tags;
  final List<String> distortions;

  ThoughtEntry({
    required this.id,
    required this.date,
    required this.situation,
    required this.thought,
    this.emotions = const [],
    this.intensity = 0,
    this.behavior,
    this.tags = const [],
    this.distortions = const [],
  });

  factory ThoughtEntry.fromJson(Map<String, dynamic> json) => ThoughtEntry(
    id: json['id'] as String,
    date: DateTime.parse(json['date'] as String),
    situation: json['situation'] as String,
    thought: json['thought'] as String,
    emotions: List<String>.from(json['emotions'] ?? const []),
    intensity: (json['intensity'] ?? 0) as int,
    behavior: json['behavior'] as String?,
    tags: List<String>.from(json['tags'] ?? const []),
    distortions: List<String>.from(json['distortions'] ?? const []),
  );
}
