import 'package:flutter/material.dart';
import 'package:thoughts_tracker/services/thought_service.dart';

class NewThoughtScreen extends StatefulWidget {
  const NewThoughtScreen({super.key});

  @override
  State<NewThoughtScreen> createState() => _NewThoughtScreenState();
}

class _NewThoughtScreenState extends State<NewThoughtScreen> {
  final _formKey = GlobalKey<FormState>();

  final List<String> _allSymptoms = [
    'Cold sweat',
    'Leg shaking',
    'Trouble to breath',
    'Dizziness',
    'Sadness',
    'Anxiety',
    'Isolation',
    'Impotence sensation',
    'Self devalue (feeling)',
  ];

  final _titleController = TextEditingController();
  final _situationController = TextEditingController();
  final _emotionController = TextEditingController();
  final _beliefController = TextEditingController();
  final List<String> _selectedSymptoms = [];

  @override
  void dispose() {
    _titleController.dispose();
    _situationController.dispose();
    _emotionController.dispose();
    _beliefController.dispose();
    super.dispose();
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      final newRecord = {
        'title': _titleController.text,
        'situation_description': _situationController.text,
        'emotion': _emotionController.text,
        'underlying_belief': _beliefController.text,
        'symptoms': _selectedSymptoms,
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
              TextFormField(
                controller: _emotionController,
                decoration: const InputDecoration(
                  labelText: 'Predominant emotion',
                ),
                validator:
                    (value) =>
                        value == null || value.isEmpty
                            ? 'Which was the predominant emotion?'
                            : null,
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
                        label: Text(symptom),
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
