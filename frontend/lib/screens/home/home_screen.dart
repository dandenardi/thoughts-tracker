import 'package:flutter/material.dart';
import '../new_thought/new_thought_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Hello, Welcome back!"),
        actions: [
          IconButton(
            icon: const Icon(Icons.analytics),
            tooltip: "Check analysis",
            onPressed: () {
              // Navigator.push to the analysis page
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Recent overview",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildSummaryCard(
              title: "Most common emotions",
              content: "Sadness, Ansiety, Joy",
              icon: Icons.emoji_emotions,
            ),
            const SizedBox(height: 12),
            _buildSummaryCard(
              title: "Most common hours",
              content: "Night (18h - 22h)",
              icon: Icons.schedule,
            ),
            const SizedBox(height: 12),
            _buildSummaryCard(
              title: "Recurrent situations",
              content: "Work conflicts, Social interactions",
              icon: Icons.repeat,
            ),
            const Spacer(),
            Text(
              "Tip: registering right after the event improves the analysis accuracy.",
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const NewThoughtScreen()),
          );
        },
        label: const Text("New registry"),
        icon: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildSummaryCard({
    required String title,
    required String content,
    required IconData icon,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: Icon(icon, color: Colors.deepPurple),
        title: Text(title),
        subtitle: Text(content),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () {
          //Could open the related analysis
        },
      ),
    );
  }
}
