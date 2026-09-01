# Graph Freshness Record

```yaml
timestamp: <ISO-8601>
project: <graph-project-id>
repo_path: ${PROJECT_ROOT}
git_head: <hash-or-UNKNOWN>
working_tree: clean | dirty
changed_paths: []
nodes: <integer>
edges: <integer>
graph_status: ready | failed
exact_worktree_freshness: PASS | UNKNOWN
```

`ready` proves query availability, not exact working-tree synchronization unless the graph API supplies a matching revision or fingerprint.
