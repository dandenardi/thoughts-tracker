import 'package:flutter/material.dart';
import 'package:thoughts_tracker/core/theme/app_theme.dart';
import 'package:thoughts_tracker/screens/auth/login_screen.dart';

void main() {
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
    );
  }
}