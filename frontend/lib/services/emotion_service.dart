import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:thoughts_tracker/models/emotion.dart';
import 'package:thoughts_tracker/services/api_config.dart';

class EmotionService {
  static Future<List<Emotion>> fetchEmotions() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/emotions/'),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final emotions =
          (data['emotions'] as List).map((e) => Emotion.fromJson(e)).toList();
      return emotions;
    } else {
      throw Exception("Failed to load emotions");
    }
  }
}
