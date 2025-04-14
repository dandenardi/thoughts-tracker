import 'package:http/http.dart' as http;
import 'package:firebase_auth/firebase_auth.dart';
import 'dart:convert';
import 'package:thoughts_tracker/services/api_config.dart';

class ThoughtService {
  static final _baseUrl = ApiConfig.baseUrl;

  static Future<Map<String, String>> _getAuthHeaders() async {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) {
      throw Exception("Usuário não autenticado.");
    }
    final idToken = await user.getIdToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $idToken',
    };
  }

  static Future<void> sendThought(Map<String, dynamic> thoughtData) async {
    try {
      final headers = await _getAuthHeaders();
      final url = Uri.parse("$_baseUrl/thought-records");

      final response = await http.post(
        url,
        headers: headers,
        body: jsonEncode(thoughtData),
      );

      if (response.statusCode != 200) {
        throw Exception(
          "Erro ao enviar pensamento: ${response.statusCode} - ${response.body}",
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  static Future<List<Map<String, dynamic>>> getThoughts() async {
    try {
      final headers = await _getAuthHeaders();
      final url = Uri.parse("$_baseUrl/thought-records");

      final response = await http.get(url, headers: headers);

      if (response.statusCode == 200) {
        final List<dynamic> jsonData = jsonDecode(response.body);
        return jsonData.cast<Map<String, dynamic>>();
      } else {
        throw Exception(
          'Error while recovering thoughts: ${response.statusCode}',
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  static Future<void> updateThought(Map<String, dynamic> updatedThought) async {
    try {
      final headers = await _getAuthHeaders();
      final url = Uri.parse(
        "$_baseUrl/thought-records/${updatedThought['id']}",
      );

      final response = await http.put(
        url,
        headers: headers,
        body: jsonEncode(updatedThought),
      );

      if (response.statusCode != 200) {
        throw Exception(
          "Error while updating thought: ${response.statusCode} - ${response.body}",
        );
      }
    } catch (e) {
      rethrow;
    }
  }
}
