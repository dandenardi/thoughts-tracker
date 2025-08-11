import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:thoughts_tracker/core/theme/app_theme.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:thoughts_tracker/firebase_options.dart';
import 'package:thoughts_tracker/services/navigation_service.dart';
import 'package:thoughts_tracker/screens/auth/login_screen.dart';

import 'package:thoughts_tracker/features/journal/presentation/journal_page.dart';
import 'package:thoughts_tracker/features/journal/data/mock_thought_repository.dart';
import 'package:thoughts_tracker/features/journal/domain/thought_repository.dart';
import 'package:thoughts_tracker/shared/di.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: 'assets/.env');

  final isMock = (dotenv.maybeGet("MOCK_MODE") ?? "").toLowerCase() == "true";

  if (!isMock) {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
  }

  ThoughtRepository? mockRepo;
  if (isMock) {
    mockRepo = await MockThoughtRepository.fromAsset(
      'assets/mock/entries_baseline.json',
      latency: const Duration(milliseconds: 300),
      errorRate: 0.0,
    );
  }

  runApp(
    ProviderScope(
      overrides: [
        if (mockRepo != null) thoughtRepoProvider.overrideWithValue(mockRepo),
      ],
      child: ThoughtsTrackerApp(isMock: isMock),
    ),
  );
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
