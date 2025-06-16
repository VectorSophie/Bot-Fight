function loadMatch(id) {
    fetch(`/match/${id}`)
        .then(res => res.json())
        .then(data => {
            const boardDiv = document.getElementById("board");
            let i = 0;
            function render() {
                if (i >= data.history.length) return;
                const state = data.history[i];
                boardDiv.innerHTML = `<pre>${state.board.map(row => row.map(c => c || ".").join(" ")).join("\n")}</pre>
                <p>Turn: ${state.turn} — Move: (${state.move})</p>`;
                i++;
                setTimeout(render, 1000);
            }
            render();
        });
}
