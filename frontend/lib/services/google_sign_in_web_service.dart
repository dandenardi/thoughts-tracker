import 'package:google_sign_in/google_sign_in.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

class GoogleSignInWebService {
  static GoogleSignIn? _googleSignIn;
  static void initGoogleSignIn({required String clientId}) {
    if (kIsWeb) {
      _googleSignIn = GoogleSignIn(
        clientId: clientId,
        scopes: <String>['email'],
      );
    }
  }

  static GoogleSignIn? get instance => _googleSignIn;

  static Future<GoogleSignInAccount?> signInWithGoogle() async {
    if (_googleSignIn == null) {
      throw Exception("Google Sign-In not initialized.");
    }

    try {
      return await _googleSignIn!.signIn();
    } catch (e) {
      throw Exception("Google Sgin-In error: $e");
    }
  }

  static Future<GoogleSignInAccount?> signInSilently() async {
    if (_googleSignIn == null) {
      throw Exception("Google Sign-In not initialized.");
    }
    try {
      return await _googleSignIn!.signInSilently();
    } catch (e) {
      throw Exception("Google Sign-In silent error: $e");
    }
  }

  static Future<void> signOut() async {
    if (_googleSignIn == null) {
      throw Exception("Google Sign-In not initialized.");
    }
    try {
      await _googleSignIn!.signOut();
    } catch (e) {
      throw Exception("Google Sign-Out error: $e");
    }
  }
}
