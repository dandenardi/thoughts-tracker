import 'package:flutter/material.dart';
import 'package:thoughts_tracker/services/thought_service.dart';

class ThoughtsListScreen extends StatefulWidget {
  const ThoughtsListScreen({super.key});

  @override
  State<ThoughtsListScreen> createState() => _ThoughtsListScreenState();
}

class _ThoughtsListScreenState extends State<ThoughtsListScreen> {
  late Future<List<Map<String, dynamic>>> _thoughtsFuture;

  @override
  void initState() {
    super.initState();
    _thoughtsFuture = ThoughtService.getThoughts();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Your thoughts')),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _thoughtsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text("No thoughts registered."));
          }

          final thoughts = snapshot.data!;
          return ListView.builder(
            itemCount: thoughts.length,
            itemBuilder: (context, index) {
              final thought = thoughts[index];
              return ListTile(
                title: Text(thought['title'] ?? 'No title'),
                subtitle: Text(thought['emotion'] ?? 'No emotion'),
                onTap: () {
                  // TODO: add detailed view and edit options
                },
              );
            },
          );
        },
      ),
    );
  }
}
