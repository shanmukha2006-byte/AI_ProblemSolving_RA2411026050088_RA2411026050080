document.addEventListener('DOMContentLoaded', () => {
    const nodeAInput = document.getElementById('node-a');
    const nodeBInput = document.getElementById('node-b');
    const addEdgeBtn = document.getElementById('add-edge-btn');
    const edgeList = document.getElementById('edge-list');
    
    const startNodeInput = document.getElementById('start-node');
    const goalNodeInput = document.getElementById('goal-node');
    const findPathBtn = document.getElementById('find-path-btn');
    const clearBtn = document.getElementById('clear-btn');

    let graph = {};

    function addEdge(u, v) {
        if (!graph[u]) graph[u] = [];
        if (!graph[v]) graph[v] = [];
        
        if (!graph[u].includes(v)) graph[u].push(v);
        if (!graph[v].includes(u)) graph[v].push(u); // Undirected graph
    }

    function updateEdgeList() {
        edgeList.innerHTML = '';
        const printed = new Set();
        
        for (const [node, neighbors] of Object.entries(graph)) {
            for (const neighbor of neighbors) {
                const edgeKey1 = `${node}-${neighbor}`;
                const edgeKey2 = `${neighbor}-${node}`;
                if (!printed.has(edgeKey1) && !printed.has(edgeKey2)) {
                    const li = document.createElement('li');
                    li.textContent = `${node} ↔ ${neighbor}`;
                    edgeList.appendChild(li);
                    printed.add(edgeKey1);
                }
            }
        }
    }

    addEdgeBtn.addEventListener('click', () => {
        const u = nodeAInput.value.trim().toUpperCase();
        const v = nodeBInput.value.trim().toUpperCase();
        
        if (u && v && u !== v) {
            addEdge(u, v);
            updateEdgeList();
            nodeAInput.value = '';
            nodeBInput.value = '';
            nodeAInput.focus();
        }
    });

    clearBtn.addEventListener('click', () => {
        graph = {};
        updateEdgeList();
        document.querySelectorAll('.path, .explored, .length').forEach(el => el.textContent = '-');
        startNodeInput.value = '';
        goalNodeInput.value = '';
    });

    findPathBtn.addEventListener('click', async () => {
        const start = startNodeInput.value.trim().toUpperCase();
        const goal = goalNodeInput.value.trim().toUpperCase();

        if (!start || !goal || Object.keys(graph).length === 0) {
            alert("Please build the graph and specify start and goal nodes.");
            return;
        }

        try {
            const res = await fetch('/find_path', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ graph, start, goal })
            });
            const data = await res.json();
            
            // Update BFS
            const bfs = data.bfs;
            document.querySelector('#bfs-result .path').textContent = bfs.path.length > 0 ? bfs.path.join(' → ') : 'No path found';
            document.querySelector('#bfs-result .explored').textContent = bfs.explored.join(', ');
            document.querySelector('#bfs-result .length').textContent = bfs.length;

            // Update DFS
            const dfs = data.dfs;
            document.querySelector('#dfs-result .path').textContent = dfs.path.length > 0 ? dfs.path.join(' → ') : 'No path found';
            document.querySelector('#dfs-result .explored').textContent = dfs.explored.join(', ');
            document.querySelector('#dfs-result .length').textContent = dfs.length;

        } catch (e) {
            console.error(e);
            alert("Error connecting to server.");
        }
    });
});
