import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:thoughts_tracker/services/api_config.dart';

class InsightsService {
  static Future<String> _getAuthToken() async {
    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      throw Exception("User not logged in.");
    }

    final token = await user.getIdToken();
    if (token == null) {
      throw Exception("Failed to get authentication token.");
    }
    return token;
  }

  static Future<Map<String, dynamic>> _fetchData(String endpoint) async {
    try {
      final token = await _getAuthToken();
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/$endpoint'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception("Failed to load data from $endpoint: ${response.body}");
      }
    } catch (e) {
      throw Exception("API request failed: ${e.toString()}");
    }
  }

  static Future<Map<String, dynamic>> fetchInsightsSummary() async {
    try {
      final data = await _fetchData('thought-records/insights-summary');

      print("DATA IN FETCH: $data");

      // Handle top_emotions (list) -> top_emotion (string)
      final topEmotions = (data['top_emotions'] as List?)?.cast<String>() ?? [];
      final topEmotion = topEmotions.isNotEmpty ? topEmotions[0] : 'N/A';

      // Convert top_emotions list to emotions_distribution format
      final emotionsDistribution =
          topEmotions
              .map(
                (emotion) => {
                  'emotion': emotion,
                  'count': 1, // Default count since API doesn't provide counts
                },
              )
              .toList();

      return {
        'total_thoughts': data['total_thoughts'] as int? ?? 0,
        'top_emotion': topEmotion,
        'most_common_symptom': data['most_common_symptom'] as String? ?? 'N/A',
        'active_days': data['active_days'] as int? ?? 0,
        'emotions_distribution': emotionsDistribution,
        'frequent_keywords':
            (data['frequent_keywords'] as List?)?.cast<String>() ?? [],
        'keyword_counts':
            (data['keyword_counts'] as Map?)?.cast<String, num>() ?? {},
        'common_time_ranges':
            (data['common_time_ranges'] as List?)?.cast<String>() ?? [],
      };
    } catch (e) {
      rethrow;
    }
  }

  static Future<Map<String, dynamic>> fetchSymptomTimePatterns() async {
    final data = await _fetchData('symptoms/symptoms-time-patterns');

    if (data['status'] == 'success') {
      return {
        'data': data['data'] ?? [],
        'message': data['message'] ?? 'Symptom time patterns retrieved',
      };
    } else {
      throw Exception(data['message'] ?? 'Failed to parse symptom patterns');
    }
  }
}
