import 'package:flutter/material.dart';
import 'package:thoughts_tracker/services/thought_service.dart';

class ThoughtDetailScreen extends StatefulWidget {
  final Map<String, dynamic> thought;

  const ThoughtDetailScreen({super.key, required this.thought});

  @override
  State<ThoughtDetailScreen> createState() => _ThoughtDetailScreenState();
}

class _ThoughtDetailScreenState extends State<ThoughtDetailScreen> {
  late TextEditingController _titleController;
  late TextEditingController _emotionController;
  late TextEditingController _situationController;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.thought['title']);
    _emotionController = TextEditingController(text: widget.thought['emotion']);
    _situationController = TextEditingController(
      text: widget.thought['situation_description'],
    );
  }

  Future<void> _saveChanges() async {
    final updatedThought = {
      ...widget.thought,
      'title': _titleController.text,
      'emotion': _emotionController.text,
      'situation_description': _situationController.text,
    };

    try {
      await ThoughtService.updateThought(updatedThought);

      if (!mounted) return;

      Navigator.of(context).pop(true);
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text("Error while saving: $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Edit Thought")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: "Title"),
            ),
            TextField(
              controller: _emotionController,
              decoration: const InputDecoration(labelText: "Emotion"),
            ),
            TextField(
              controller: _situationController,
              decoration: const InputDecoration(labelText: "Situation"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: _saveChanges, child: const Text("Save")),
          ],
        ),
      ),
    );
  }
}
