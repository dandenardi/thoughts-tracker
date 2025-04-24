import 'package:flutter/material.dart';
import 'package:thoughts_tracker/screens/thoughts_list/thoughts_list_screen.dart';
import '../new_thought/new_thought_screen.dart';
import 'package:thoughts_tracker/services/insights_service.dart';
import 'package:thoughts_tracker/services/navigation_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with RouteAware {
  String _commonEmotions = "Loading...";
  String _commonHours = "Loading...";
  String _commonSituations = "Loading...";
  String? _errorMessage;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    routeObserver.subscribe(this, ModalRoute.of(context)!);
  }

  @override
  void initState() {
    super.initState();
    _loadInsights();
  }

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    super.dispose();
  }

  @override
  void didPopNext() {
    _loadInsights();
  }

  Future<void> _loadInsights() async {
    try {
      final insights = await InsightsService.fetchInsightsSummary();
      setState(() {
        _commonEmotions = insights['top_emotions'].join(', ');
        _commonHours = insights['common_time_ranges'].join(', ');
        _commonSituations = insights['frequent_keywords'].join(', ');
      });
    } catch (e) {
      setState(() {
        _errorMessage = "Failed to load insights: $e";
        _commonEmotions = _commonHours = _commonSituations = "Unavailable";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Hello, Welcome back!"),
        actions: [
          IconButton(
            icon: const Icon(Icons.list),
            tooltip: "View all thoughts",
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const ThoughtsListScreen()),
              );

              // Navigator.push to the analysis page
            },
          ),
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
            if (_errorMessage != null)
              Text(_errorMessage!, style: const TextStyle(color: Colors.red)),
            _buildSummaryCard(
              title: "Most common emotions",
              content: _commonEmotions,
              icon: Icons.emoji_emotions,
            ),
            const SizedBox(height: 12),
            _buildSummaryCard(
              title: "Most common hours",
              content: _commonHours,
              icon: Icons.schedule,
            ),
            const SizedBox(height: 12),
            _buildSummaryCard(
              title: "Recurrent situations",
              content: _commonSituations,
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
