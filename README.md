# Artificial Intelligence - Problem Solving Assignment

This repository contains the implementations for two Artificial Intelligence problems selected from the assignment list. The solutions are built using **Python** (with the Flask framework for the backend) and feature interactive **HTML/CSS/JS** GUIs.

## Problems Selected

### 1. Problem 1: Interactive Game AI (Tic-Tac-Toe System)
An interactive web-based Tic-Tac-Toe game where the user plays against an AI opponent. The AI utilizes Adversarial Search techniques to determine its moves.

**Algorithms Used:**
*   **Minimax Algorithm:** A decision-making algorithm that explores the entire game tree to find the optimal move, assuming the opponent plays perfectly.
*   **Alpha-Beta Pruning:** An optimized version of Minimax that prunes branches of the game tree that don't need to be explored, significantly reducing the number of nodes evaluated and improving execution time.

**Key Features:**
*   The AI will never lose; it plays perfectly.
*   Real-time comparison of the execution time and the number of nodes explored between Minimax and Alpha-Beta Pruning.

---

### 2. Problem 8: Smart Navigation System
A dynamic graph-based navigation system where a user can construct a map (adding nodes and edges) and find paths between a start node and a goal node.

**Algorithms Used:**
*   **Breadth-First Search (BFS):** Explores the graph level by level. It guarantees the shortest path (in terms of the number of edges) in an unweighted graph.
*   **Depth-First Search (DFS):** Explores as far down a branch as possible before backtracking. It does not guarantee the shortest path but is memory efficient.

**Key Features:**
*   Interactive UI to add nodes and connect them with edges.
*   Visual comparison of the paths found, nodes explored, and path lengths between BFS and DFS.

## Execution Steps

Follow these instructions to run the project locally or deploy it to a server.

1.  **Prerequisites:** Ensure you have Python 3.x installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/shanmukha2006-byte/AI_ProblemSolving_-RA2411026050088-.git
    cd AI_ProblemSolving_-RA2411026050088-
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Unified App
1.  Start the Flask server from the root directory:
    ```bash
    python app.py
    ```
2.  Open your web browser and go to `http://127.0.0.1:5000`.
3.  Use the main menu to navigate between the **Tic-Tac-Toe** and **Smart Navigation** interfaces.

### Deployment Instructions (Render.com / Heroku)
This application is fully configured for deployment on platforms like Render or Heroku:
1. Connect this GitHub repository to your Render/Heroku account.
2. Select **Web Service** and choose Python as the environment.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app` (or it will automatically detect the `Procfile`).

## Sample Outputs

*   **Tic-Tac-Toe:** The user interface shows a 3x3 grid. Upon making a move, the AI instantly responds. The status panel updates to show "Nodes Explored: 54994" for Minimax versus "Nodes Explored: 2321" for Alpha-Beta pruning, with execution time dropping from ~60ms to ~3ms.
*   **Smart Navigation:** After adding edges `A-B`, `A-C`, `B-D`, `C-D`, `D-E` and searching from `A` to `E`, BFS finds the path `A → B → D → E` exploring 4 nodes. DFS finds `A → C → D → E` exploring similar nodes but taking a different route.
