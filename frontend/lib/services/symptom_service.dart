import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:thoughts_tracker/models/symptom.dart';
import 'package:thoughts_tracker/services/api_config.dart';

class SymptomService {
  static Future<List<Symptom>> fetchSymptoms() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/symptoms/'),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final symptoms =
          (data['symptoms'] as List).map((e) => Symptom.fromJson(e)).toList();
      return symptoms;
    } else {
      throw Exception("Failed to load symptoms");
    }
  }
}
