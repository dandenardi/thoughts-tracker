import 'package:flutter/material.dart';
import 'package:thoughts_tracker/models/emotion.dart';
import 'package:thoughts_tracker/models/symptom.dart';
import 'package:thoughts_tracker/services/emotion_service.dart';
import 'package:thoughts_tracker/services/symptom_service.dart';
import 'package:thoughts_tracker/services/thought_service.dart';

class NewThoughtScreen extends StatefulWidget {
  const NewThoughtScreen({super.key});

  @override
  State<NewThoughtScreen> createState() => _NewThoughtScreenState();
}

class _NewThoughtScreenState extends State<NewThoughtScreen> {
  final _formKey = GlobalKey<FormState>();

  final _titleController = TextEditingController();
  final _situationController = TextEditingController();
  final _beliefController = TextEditingController();

  List<Emotion> _emotions = [];
  List<Symptom> _allSymptoms = [];
  Emotion? _selectedEmotion;
  final List<Symptom> _selectedSymptoms = [];

  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final emotions = await EmotionService.fetchEmotions();
      final symptoms = await SymptomService.fetchSymptoms();

      setState(() {
        _emotions = emotions;
        _allSymptoms = symptoms;
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Error loading data: $e')));
    }
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      final newRecord = {
        'title': _titleController.text,
        'situation_description': _situationController.text,
        'emotion': _selectedEmotion?.name,
        'underlying_belief': _beliefController.text,
        'symptoms': _selectedSymptoms.map((s) => s.name).toList(),
      };

      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => const Center(child: CircularProgressIndicator()),
      );

      try {
        await ThoughtService.sendThought(newRecord);
        if (!mounted) return;
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Registry saved successfully!")),
        );
        Navigator.of(context).pop();
      } catch (e) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("Error: $e")));
      }
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _situationController.dispose();
    _beliefController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('New Registry')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(
                  labelText: 'Title (optional)',
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _situationController,
                decoration: const InputDecoration(
                  labelText: 'Describe the situation',
                ),
                maxLines: 3,
                validator:
                    (value) =>
                        value == null || value.isEmpty
                            ? 'Please, describe the situation.'
                            : null,
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<Emotion>(
                value: _selectedEmotion,
                items:
                    _emotions
                        .map(
                          (e) =>
                              DropdownMenuItem(value: e, child: Text(e.name)),
                        )
                        .toList(),
                onChanged: (value) {
                  setState(() {
                    _selectedEmotion = value;
                  });
                },
                decoration: const InputDecoration(
                  labelText: 'Predominant emotion',
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _beliefController,
                decoration: const InputDecoration(
                  labelText: 'Subjacent belief (optional)',
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'Symptoms (optional)',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              Wrap(
                spacing: 8,
                runSpacing: 4,
                children:
                    _allSymptoms.map((symptom) {
                      final isSelected = _selectedSymptoms.contains(symptom);
                      return FilterChip(
                        label: Text(symptom.name),
                        selected: isSelected,
                        onSelected: (bool selected) {
                          setState(() {
                            if (selected) {
                              _selectedSymptoms.add(symptom);
                            } else {
                              _selectedSymptoms.remove(symptom);
                            }
                          });
                        },
                      );
                    }).toList(),
              ),
              const SizedBox(height: 24),
              ElevatedButton(onPressed: _submitForm, child: const Text("Save")),
            ],
          ),
        ),
      ),
    );
  }
}
