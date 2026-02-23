import json
import sys

def load_workflow(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_nodes_map(workflow):
    return {node['name']: node for node in workflow.get('nodes', [])}

def compare_nodes(node1, node2):
    diffs = []
    # Compare parameters
    params1 = node1.get('parameters', {})
    params2 = node2.get('parameters', {})

    # Check for keys in params1 that are different in params2
    for k, v in params1.items():
        if k not in params2:
            diffs.append(f'Parameter {k} removed')
        elif params2[k] != v:
            diffs.append(f'Parameter {k} changed: {v} -> {params2[k]}')

    for k, v in params2.items():
        if k not in params1:
            diffs.append(f'Parameter {k} added: {v}')

    # Compare credentials
    creds1 = node1.get('credentials', {})
    creds2 = node2.get('credentials', {})
    if creds1 != creds2:
        diffs.append(f'Credentials changed: {creds1} -> {creds2}')

    return diffs

if __name__ == '__main__':
    w1 = load_workflow(sys.argv[1])
    w2 = load_workflow(sys.argv[2])

    nodes1 = get_nodes_map(w1)
    nodes2 = get_nodes_map(w2)

    changes = []

    for name, node in nodes1.items():
        if name not in nodes2:
            changes.append(f'Node removed: {name}')
        else:
            diffs = compare_nodes(node, nodes2[name])
            if diffs:
                changes.append(f'Node {name} modified:\n  ' + '\n  '.join(diffs))

    for name in nodes2:
        if name not in nodes1:
            changes.append(f'Node added: {name}')

    if not changes:
        print('No significant changes found in nodes.')
    else:
        print('\n'.join(changes))
