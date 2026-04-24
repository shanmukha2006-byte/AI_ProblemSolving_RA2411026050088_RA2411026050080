document.addEventListener('DOMContentLoaded', () => {
    const cells = document.querySelectorAll('.cell');
    const resetBtn = document.getElementById('reset-btn');
    const algoSelect = document.getElementById('algo');
    const statusText = document.getElementById('status-text');
    const nodesVal = document.getElementById('nodes-val');
    const timeVal = document.getElementById('time-val');

    let board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ];
    let isGameOver = false;

    function renderBoard() {
        cells.forEach(cell => {
            const r = cell.dataset.row;
            const c = cell.dataset.col;
            cell.textContent = board[r][c];
            cell.className = 'cell';
            if (board[r][c] === 'X') cell.classList.add('x');
            if (board[r][c] === 'O') cell.classList.add('o');
        });
    }

    function resetGame() {
        board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ];
        isGameOver = false;
        statusText.textContent = "Your turn!";
        nodesVal.textContent = "-";
        timeVal.textContent = "-";
        renderBoard();
    }

    async function makeAiMove() {
        statusText.textContent = "AI is thinking...";
        try {
            const res = await fetch('/make_move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ board, algo: algoSelect.value })
            });
            const data = await res.json();
            
            board = data.board;
            nodesVal.textContent = data.nodes_explored || "-";
            if (data.execution_time_ms !== undefined) {
                timeVal.textContent = data.execution_time_ms.toFixed(2) + " ms";
            }
            renderBoard();

            if (data.status === 'game_over') {
                isGameOver = true;
                if (data.winner === 'Tie') statusText.textContent = "It's a Tie!";
                else statusText.textContent = `${data.winner} Wins!`;
            } else {
                statusText.textContent = "Your turn!";
            }
        } catch (e) {
            console.error(e);
            statusText.textContent = "Error connecting to AI";
        }
    }

    cells.forEach(cell => {
        cell.addEventListener('click', async () => {
            if (isGameOver) return;
            const r = cell.dataset.row;
            const c = cell.dataset.col;
            
            if (board[r][c] !== '') return;

            board[r][c] = 'X';
            renderBoard();
            
            // Check if X won (rare without AI move, but user could win if playing custom logic)
            // The backend checks state before AI moves.
            await makeAiMove();
        });
    });

    resetBtn.addEventListener('click', resetGame);
});
