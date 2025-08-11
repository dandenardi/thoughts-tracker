import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/thought_entry.dart';
import '../../../shared/di.dart';

final entriesProvider = FutureProvider<List<ThoughtEntry>>((ref) {
  final repo = ref.watch(thoughtRepoProvider);
  return repo.list();
});

class JournalPage extends ConsumerWidget {
  const JournalPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final async = ref.watch(entriesProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Journal')),
      body: async.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Erro: $e')),
        data:
            (items) =>
                items.isEmpty
                    ? const Center(child: Text('Sem registros ainda'))
                    : ListView.separated(
                      itemCount: items.length,
                      separatorBuilder: (_, __) => const Divider(height: 1),
                      itemBuilder: (_, i) {
                        final e = items[i];
                        return ListTile(
                          title: Text(e.thought),
                          subtitle: Text(e.situation),
                          trailing: Text('${e.intensity}/10'),
                          onTap: () {
                            // TODO: navegar para detalhe (mockado também)
                          },
                        );
                      },
                    ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: abrir criação mockada
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
