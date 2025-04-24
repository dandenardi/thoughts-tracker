import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:http/http.dart' as http;
import 'package:thoughts_tracker/services/api_config.dart';

class InsightsService {
  static Future<Map<String, dynamic>> fetchInsightsSummary() async {
    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      throw Exception("User not logged in.");
    }

    final token = await user.getIdToken();
    print("Token $token");
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/thought-records/insights-summary'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body) as Map<String, dynamic>;
    } else {
      throw Exception("Failed to load insights: ${response.body}");
    }
  }
}
