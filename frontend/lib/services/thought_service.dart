import 'package:http/http.dart' as http;
import 'package:firebase_auth/firebase_auth.dart';
import 'dart:convert';
import 'package:thoughts_tracker/services/api_config.dart';

class ThoughtService {
  static final _baseUrl = ApiConfig.baseUrl;

  static Future<void> sendThought(Map<String, dynamic> thoughtData) async {
    try {
      final user = FirebaseAuth.instance.currentUser;
      if (user == null) {
        throw Exception("User not authenticated.");
      }
      final idToken = await user.getIdToken(true);

      final url = Uri.parse("$_baseUrl/thought-records");
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $idToken',
        },
        body: jsonEncode(thoughtData),
      );

      if (response.statusCode != 200) {
        throw Exception(
          "Error while sending thought: ${response.statusCode} - ${response.body}",
        );
      }
    } catch (e) {
      rethrow;
    }
  }
}
