import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:thoughts_tracker/services/google_sign_in_web_service.dart'; // Aqui você pode importar o serviço

class AuthController {
  final FirebaseAuth _firebaseAuth = FirebaseAuth.instance;
  bool _isGoogleSignInInitialized = false;

  Future<void> _ensureGoogleSignInInitialized() async {
    if (!_isGoogleSignInInitialized && kIsWeb) {
      final clientId = dotenv.env['GOOGLE_CLIENT_ID_WEB'];
      if (clientId == null || clientId.isEmpty) {
        throw Exception("GOOGLE_CLIENT_ID_WEB not found in .env");
      }
      GoogleSignInWebService.initGoogleSignIn(clientId: clientId);
      _isGoogleSignInInitialized = true;
    }
  }

  Future<void> initGoogleSignIn(String clientId) async {
    GoogleSignInWebService.initGoogleSignIn(clientId: clientId);
  }

  Future<UserCredential?> loginWithGoogle() async {
    await _ensureGoogleSignInInitialized();

    final googleSignInAccount = await GoogleSignInWebService.signInWithGoogle();
    if (googleSignInAccount != null) {
      final googleAuth = await googleSignInAccount.authentication;
      final credential = GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );
      return await _firebaseAuth.signInWithCredential(credential);
    }
    return null;
  }

  // Login silencioso com Google
  Future<UserCredential?> loginWithGoogleSilently() async {
    await _ensureGoogleSignInInitialized();

    final googleSignInAccount = await GoogleSignInWebService.signInSilently();
    if (googleSignInAccount != null) {
      final googleAuth = await googleSignInAccount.authentication;
      final credential = GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );
      return await _firebaseAuth.signInWithCredential(credential);
    }
    return null;
  }

  // Login com email e senha
  Future<UserCredential?> loginWithEmail(String email, String password) async {
    try {
      return await _firebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
    } catch (e) {
      rethrow;
    }
  }

  // Verifica se o usuário já está autenticado
  Future<User?> checkExistingLogin() async {
    return _firebaseAuth.currentUser;
  }
}
