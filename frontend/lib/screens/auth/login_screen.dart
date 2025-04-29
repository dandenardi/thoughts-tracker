import 'package:flutter/material.dart';
import 'package:thoughts_tracker/screens/home/home_screen.dart';
import 'package:firebase_ui_auth/firebase_ui_auth.dart';
import 'package:firebase_ui_oauth_google/firebase_ui_oauth_google.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SignInScreen(
      providers: [
        EmailAuthProvider(),
        GoogleProvider(clientId: dotenv.env['GOOGLE_CLIENT_ID']!),
      ],
      actions: [
        AuthStateChangeAction<SignedIn>((context, state) {
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => const HomeScreen()),
          );
        }),
      ],
      headerBuilder: (context, constraints, _) {
        return const Padding(
          padding: EdgeInsets.all(16),
          child: Text(
            'Welcome to the Thoughts Tracker!',
            style: TextStyle(fontSize: 24),
          ),
        );
      },
    );
  }
}
