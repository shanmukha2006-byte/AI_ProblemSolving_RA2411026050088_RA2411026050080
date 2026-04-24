from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

def bfs(graph, start, goal):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": [], "length": 0}
        
    explored = []
    queue = deque([[start]])
    
    if start == goal:
        return {"path": [start], "explored": [start], "length": 1}
        
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node not in explored:
            neighbors = graph.get(node, [])
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                
                if neighbor == goal:
                    explored.append(node)
                    return {"path": new_path, "explored": explored, "length": len(new_path)}
                    
            explored.append(node)
            
    return {"path": [], "explored": explored, "length": 0}

def dfs(graph, start, goal):
    if start not in graph or goal not in graph:
        return {"path": [], "explored": [], "length": 0}
        
    explored = []
    stack = [[start]]
    
    if start == goal:
        return {"path": [start], "explored": [start], "length": 1}
        
    while stack:
        path = stack.pop()
        node = path[-1]
        
        if node not in explored:
            explored.append(node)
            if node == goal:
                return {"path": path, "explored": explored, "length": len(path)}
                
            neighbors = graph.get(node, [])
            # To match common DFS behavior, we add neighbors in reverse so they are popped in order
            for neighbor in reversed(neighbors):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
                
    return {"path": [], "explored": explored, "length": 0}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.json
    graph = data.get('graph', {}) # dict like { "A": ["B", "C"], "B": ["A", "D"] }
    start = data.get('start')
    goal = data.get('goal')

    bfs_result = bfs(graph, start, goal)
    dfs_result = dfs(graph, start, goal)

    return jsonify({
        "bfs": bfs_result,
        "dfs": dfs_result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
