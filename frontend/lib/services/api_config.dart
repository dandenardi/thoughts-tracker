import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiConfig {
  static bool get isProduction => dotenv.env['ENVIRONMENT'] == 'production';

  static String get baseUrl {
    if (isProduction) {
      return "https://thoughts-tracker-production.up.railway.app";
    }

    if (kIsWeb) {
      return "http://localhost:8000";
    } else if (Platform.isAndroid) {
      return "http://10.0.2.2:8000";
    } else {
      return "http:localhost:8000";
    }
  }
}
