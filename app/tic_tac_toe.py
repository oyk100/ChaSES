"""Interactive Tic Tac Toe game served with Bokeh.

Run with:
    bokeh serve app/tic_tac_toe.py --show
"""

from typing import Optional

from bokeh.io import curdoc
from bokeh.layouts import column, gridplot, row
from bokeh.models import Button, Div

PLAYERS = ("X", "O")

# game state containers
board_state = [""] * 9
current_player = PLAYERS[0]
game_over = False


status_div = Div(text=f"<b>Player {current_player}'s turn</b>")
info_div = Div(
    text=(
        "Click an empty square to place your mark. First player to align "
        "three vertically, horizontally, or diagonally wins. Use "
        "\"Start a new game\" to reset."
    )
)


buttons = [Button(label="", width=90, height=90) for _ in range(9)]


def update_status(text: str) -> None:
    """Update the status display."""
    status_div.text = f"<b>{text}</b>"


def disable_open_squares() -> None:
    """Prevent further interaction with remaining squares."""
    for idx, btn in enumerate(buttons):
        if board_state[idx] == "":
            btn.disabled = True


def check_winner() -> Optional[str]:
    """Return the symbol of the winning player, if any."""
    winning_combos = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]

    for combo in winning_combos:
        a, b, c = combo
        if board_state[a] and board_state[a] == board_state[b] == board_state[c]:
            return board_state[a]

    return None


def handle_move(idx: int) -> None:
    """Place a mark for the current player and evaluate the board."""
    global current_player, game_over

    if game_over or board_state[idx]:
        return

    board_state[idx] = current_player
    buttons[idx].label = current_player
    buttons[idx].disabled = True

    winner = check_winner()
    if winner:
        game_over = True
        update_status(f"Player {winner} wins! 🎉")
        disable_open_squares()
        return

    if all(board_state):
        game_over = True
        update_status("It's a draw.")
        return

    current_player = PLAYERS[0] if current_player == PLAYERS[1] else PLAYERS[1]
    update_status(f"Player {current_player}'s turn")


def reset_game() -> None:
    """Clear the board for a new round."""
    global board_state, current_player, game_over

    board_state = [""] * 9
    current_player = PLAYERS[0]
    game_over = False

    for btn in buttons:
        btn.label = ""
        btn.disabled = False

    update_status(f"Player {current_player}'s turn")


for i, btn in enumerate(buttons):
    btn.on_click(lambda _, idx=i: handle_move(idx))

reset_button = Button(label="Start a new game", button_type="primary", width=200)
reset_button.on_click(reset_game)

board = gridplot(
    children=[[buttons[0], buttons[1], buttons[2]], [buttons[3], buttons[4], buttons[5]], [buttons[6], buttons[7], buttons[8]]],
    toolbar_location=None,
)

layout = column(
    Div(text="<h1>Tic Tac Toe</h1>"),
    info_div,
    board,
    row(reset_button, status_div, sizing_mode="scale_width"),
    sizing_mode="scale_width",
    margin=(10, 10, 10, 10),
)

curdoc().add_root(layout)
curdoc().title = "Tic Tac Toe"
