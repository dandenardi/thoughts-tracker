import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:thoughts_tracker/core/theme/app_theme.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:thoughts_tracker/firebase_options.dart';
import 'package:thoughts_tracker/services/navigation_service.dart';
import 'package:thoughts_tracker/screens/auth/login_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: 'assets/.env');
  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);

  runApp(const ThoughtsTrackerApp());
}

class ThoughtsTrackerApp extends StatelessWidget {
  // This widget is the root of your application.
  const ThoughtsTrackerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Thoughts Tracker',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const LoginScreen(),
      navigatorObservers: [routeObserver],
    );
  }
}
