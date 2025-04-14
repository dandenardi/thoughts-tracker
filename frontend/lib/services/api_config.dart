import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

class ApiConfig {
  static String get baseUrl {
    if (kIsWeb) {
      return "http://localhost:8000";
    } else if (Platform.isAndroid) {
      return "http://10.0.2.2:8000";
    } else {
      return "http:localhost:8000";
    }
  }
}
