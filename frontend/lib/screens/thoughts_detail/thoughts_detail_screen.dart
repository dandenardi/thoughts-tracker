import 'package:flutter/material.dart';
import 'package:thoughts_tracker/services/thought_service.dart';
import 'package:thoughts_tracker/services/symptom_service.dart';
import 'package:thoughts_tracker/services/emotion_service.dart';
import 'package:thoughts_tracker/models/emotion.dart';
import 'package:thoughts_tracker/models/symptom.dart';

class ThoughtDetailScreen extends StatefulWidget {
  final Map<String, dynamic> thought;

  const ThoughtDetailScreen({super.key, required this.thought});

  @override
  State<ThoughtDetailScreen> createState() => _ThoughtDetailScreenState();
}

class _ThoughtDetailScreenState extends State<ThoughtDetailScreen> {
  late TextEditingController _titleController;
  late TextEditingController _situationController;
  late TextEditingController _underlyingBeliefController;

  late String _selectedEmotion;
  late List<String> _selectedSymptoms;
  late List<Emotion> _allEmotions;
  late List<Symptom> _allSymptoms;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.thought['title']);
    _situationController = TextEditingController(
      text: widget.thought['situation_description'],
    );

    _selectedEmotion = widget.thought['emotion'] ?? '';
    _selectedSymptoms = List<String>.from(widget.thought['symptoms'] ?? []);
    _underlyingBeliefController = TextEditingController(
      text: widget.thought['underlying_belief'] ?? '',
    );

    _allEmotions = [];
    _allSymptoms = [];

    _loadEmotionsAndSymptoms();
  }

  Future<void> _loadEmotionsAndSymptoms() async {
    try {
      final emotions = await EmotionService.fetchEmotions();
      final symptoms = await SymptomService.fetchSymptoms();

      setState(() {
        _allEmotions = emotions;
        _allSymptoms = symptoms;
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error loading data: $e')));
    }
  }

  Future<void> _saveChanges() async {
    final updatedThought = {
      ...widget.thought,
      'title': _titleController.text,
      'emotion': _selectedEmotion,
      'situation_description': _situationController.text,
      'symptoms': _selectedSymptoms,
      'underlying_belief': _underlyingBeliefController.text,
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
  void dispose() {
    _titleController.dispose();
    _situationController.dispose();
    _underlyingBeliefController.dispose();
    super.dispose();
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
            DropdownButton<String>(
              value: _selectedEmotion,
              onChanged: (String? newValue) {
                setState(() {
                  _selectedEmotion = newValue!;
                });
              },
              items:
                  _allEmotions.map<DropdownMenuItem<String>>((Emotion emotion) {
                    return DropdownMenuItem<String>(
                      value: emotion.name,
                      child: Text(emotion.name),
                    );
                  }).toList(),
            ),
            TextField(
              controller: _situationController,
              decoration: const InputDecoration(labelText: "Situation"),
            ),
            TextField(
              controller: _underlyingBeliefController,
              decoration: const InputDecoration(labelText: "Underlying Belief"),
            ),
            const SizedBox(height: 20),
            Text('Symptoms: '),
            ..._allSymptoms.map((symptom) {
              return CheckboxListTile(
                title: Text(symptom.name),
                value: _selectedSymptoms.contains(symptom.name),
                onChanged: (bool? value) {
                  setState(() {
                    if (value == true) {
                      _selectedSymptoms.add(symptom.name);
                    } else {
                      _selectedSymptoms.remove(symptom.name);
                    }
                  });
                },
              );
            }),
            ElevatedButton(onPressed: _saveChanges, child: const Text("Save")),
          ],
        ),
      ),
    );
  }
}
