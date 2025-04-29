import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
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
  Map<String, dynamic>? _insightsData;
  List<dynamic>? _timePatternsData;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    routeObserver.subscribe(this, ModalRoute.of(context)!);
  }

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    super.dispose();
  }

  @override
  void didPopNext() {
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final insights = await InsightsService.fetchInsightsSummary();
      final patterns = await InsightsService.fetchSymptomTimePatterns();
      print("INSIGHTS: $insights ");
      setState(() {
        _insightsData = insights;
        _timePatternsData = patterns['data'];
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = "Failed to load insights: ${e.toString()}";
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Thoughts Tracker Dashboard"),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadData,
            tooltip: "Refresh data",
          ),
          IconButton(
            icon: const Icon(Icons.list),
            onPressed:
                () => Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const ThoughtsListScreen()),
                ),
            tooltip: "View all thoughts",
          ),
        ],
      ),
      body:
          _isLoading
              ? const Center(child: CircularProgressIndicator())
              : _errorMessage != null
              ? Center(
                child: Text(
                  _errorMessage!,
                  style: const TextStyle(color: Colors.red),
                ),
              )
              : SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildSummarySection(),

                    const SizedBox(height: 24),

                    _buildEmotionsRadarChart(),

                    const SizedBox(height: 24),

                    _buildTimePatternsChart(),

                    const SizedBox(height: 24),

                    _buildWordCloudSection(),

                    const SizedBox(height: 24),

                    _buildUserTip(),
                  ],
                ),
              ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed:
            () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const NewThoughtScreen()),
            ),
        label: const Text("New Thought"),
        icon: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildSummarySection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          "Your Mental health Overview",
          style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 16),
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                title: "Total Thoughts",
                value: _insightsData?['total_thoughts']?.toString() ?? '0',
                icon: Icons.notes,
                color: Colors.blue,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildMetricCard(
                title: "Top Emotion",
                value: _insightsData?['top_emotion'] ?? 'N/A',
                icon: Icons.emoji_emotions,
                color: Colors.purple,
              ),
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                title: "Common Symptom",
                value: _insightsData?['most_common_symptom'] ?? 'N/A',
                icon: Icons.medical_services,
                color: Colors.orange,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildMetricCard(
                title: "Active Days",
                value: _insightsData?['active_days']?.toString() ?? '0',
                icon: Icons.calendar_today,
                color: Colors.green,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: _buildMetricCard(
                title: "Common Time",
                value: _insightsData?['common_time_ranges']?.first ?? 'N/A',
                icon: Icons.calendar_today,
                color: Colors.teal,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildMetricCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, size: 20, color: color),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: const TextStyle(fontSize: 14, color: Colors.grey),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmotionsRadarChart() {
    // Verificação segura dos dados
    final emotionsData =
        (_insightsData?['emotions_distribution'] as List?)
            ?.cast<Map<String, dynamic>>() ??
        [];

    // Se não houver dados suficientes, mostra mensagem
    if (emotionsData.isEmpty || emotionsData.length < 3) {
      return _buildEmptyChartPlaceholder("Not enough emotion data to display");
    }

    // Converte os dados para RadarEntry
    final radarEntries =
        emotionsData.map<RadarEntry>((e) {
          return RadarEntry(value: (e['count'] as num?)?.toDouble() ?? 0.0);
        }).toList();

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Emotions Distribution",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 300,
              child: RadarChart(
                RadarChartData(
                  dataSets: [
                    RadarDataSet(
                      dataEntries: radarEntries,
                      fillColor: Colors.deepPurple.withOpacity(0.3),
                      borderColor: Colors.deepPurple,
                      borderWidth: 2,
                    ),
                  ],
                  radarBackgroundColor: Colors.transparent,
                  radarShape: RadarShape.polygon,
                  titleTextStyle: const TextStyle(
                    color: Colors.black,
                    fontSize: 12,
                  ),
                  getTitle: (index, _) {
                    if (index >= 0 && index < emotionsData.length) {
                      return RadarChartTitle(
                        text: emotionsData[index]['emotion'].toString(),
                      );
                    }
                    return const RadarChartTitle(text: '');
                  },
                  titlePositionPercentageOffset: 0.1,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyChartPlaceholder(String message) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Emotions Distribution",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 300,
              child: Center(
                child: Text(
                  message,
                  style: TextStyle(fontSize: 16, color: Colors.grey[600]),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _getEmotionColor(String emotion) {
    final colors = {
      'happy': Colors.yellow,
      'sad': Colors.blue,
      'angry': Colors.red,
      'anxious': Colors.orange,
      'calm': Colors.green,
      'excited': Colors.pink,
    };
    return colors[emotion.toLowerCase()] ?? Colors.deepPurple;
  }

  Widget _buildTimePatternsChart() {
    if (_timePatternsData == null || _timePatternsData!.isEmpty) {
      return const SizedBox.shrink();
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Symptom Time Patterns",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 300,
              child: BarChart(
                BarChartData(
                  barTouchData: BarTouchData(enabled: false),
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      axisNameWidget: const Text('Time Range'),
                      axisNameSize: 16,
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          final index = value.toInt();
                          if (index >= 0 && index < _timePatternsData!.length) {
                            return Padding(
                              padding: const EdgeInsets.only(top: 8.0),
                              child: Text(
                                _timePatternsData![index]['time_range']
                                    .toString(),
                                style: const TextStyle(fontSize: 10),
                              ),
                            );
                          }
                          return const SizedBox.shrink();
                        },
                        reservedSize: 40,
                      ),
                    ),
                    leftTitles: AxisTitles(
                      axisNameWidget: const Text('Count'),
                      axisNameSize: 16,
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 40,
                        interval: _calculateInterval(_timePatternsData!),
                        getTitlesWidget: (value, meta) {
                          return Text(value.toInt().toString());
                        },
                      ),
                    ),
                    rightTitles: const AxisTitles(),
                    topTitles: const AxisTitles(),
                  ),
                  borderData: FlBorderData(show: false),
                  barGroups:
                      _timePatternsData!.asMap().entries.map((entry) {
                        final index = entry.key;
                        final data = entry.value;
                        return BarChartGroupData(
                          x: index,
                          barRods: [
                            BarChartRodData(
                              toY: (data['count'] as num?)?.toDouble() ?? 0.0,
                              color: _getTimeRangeColor(data['time_range']),
                              width: 16,
                              borderRadius: BorderRadius.circular(4),
                            ),
                          ],
                          showingTooltipIndicators: [0],
                        );
                      }).toList(),
                  gridData: FlGridData(show: false),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  double _calculateInterval(List<dynamic> data) {
    final maxCount = data.fold<double>(0, (max, item) {
      final count = (item['count'] as num?)?.toDouble() ?? 0.0;
      return count > max ? count : max;
    });

    if (maxCount <= 0) return 1;
    if (maxCount <= 5) return 1;
    if (maxCount <= 10) return 2;
    return maxCount / 5;
  }

  Color _getTimeRangeColor(String range) {
    switch (range) {
      case 'Morning':
        return Colors.blue;
      case 'Afternoon':
        return Colors.green;
      case 'Night':
        return Colors.red;
      case 'Dawn':
        return Colors.purple;
      default:
        return Colors.grey;
    }
  }

  Widget _buildWordCloudSection() {
    // Verificação segura dos dados
    final keywords =
        _insightsData?['frequent_keywords'] is List
            ? List<String>.from(_insightsData!['frequent_keywords'] ?? [])
            : <String>[];

    final keywordCounts =
        _insightsData?['keyword_counts'] is Map
            ? Map<String, dynamic>.from(_insightsData!['keyword_counts'] ?? {})
            : <String, dynamic>{};

    if (keywords.isEmpty) {
      return const SizedBox.shrink();
    }

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Frequent Contexts",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children:
                  keywords.map<Widget>((keyword) {
                    // Tratamento seguro para contagem de palavras
                    final count =
                        keywordCounts[keyword] is num
                            ? (keywordCounts[keyword] as num).toInt()
                            : 1;

                    return Chip(
                      label: Text(keyword),
                      backgroundColor: Color.fromRGBO(103, 58, 183, 0.1),
                      labelStyle: TextStyle(
                        fontSize: 12 + (count * 2).toDouble(),
                        color: Colors.deepPurple,
                      ),
                    );
                  }).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUserTip() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Color.fromRGBO(103, 58, 183, 0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          const Icon(Icons.lightbulb_outline, color: Colors.deepPurple),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              "Tip: Tracking your thoughts right after they occur improves analysis accuracy.",
              style: TextStyle(color: Colors.deepPurple[800]),
            ),
          ),
        ],
      ),
    );
  }
}
