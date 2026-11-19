[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/venomeum/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/venomeum/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
# tiny-chess-01 — a chess engine in under 4 KB of Python

`main.py` (3,982 bytes, Python 3.13, stdlib only) is a complete,
deterministic chess engine built for the make.fun "strongest chess
engine in 4 KB of Python" bounty.

## How it plays

- **Board**: 0x88 mailbox board. State is a small list
  `[board, side_to_move, castling_rights, ep_square, undo_stack]`;
  make-move copies the board, unmake restores it.
- **Move generation**: full legal movegen — castling (with all
  transit-square attack checks), en passant (including pin cases,
  handled by the generic own-king-safety filter), promotions,
  check/checkmate/stalemate detection. Verified by perft against
  known node counts (startpos d3 = 8,902, d4 = 197,281, Kiwipete,
  en-passant/castling-pin and promotion suites — all exact).
- **Search**: negamax with alpha-beta pruning and quiescence
  (captures only), mate-distance scoring (fast mates preferred),
  MVV-LVA + promotion move ordering, iterative deepening 1–5 plies.
- **Deterministic by construction**: search stops on a fixed node
  cap (16,000 nodes), never on the clock, and there is no
  randomness — the same position always yields the same move.
  Worst measured move time ≈ 1.0 s (limit: 10 s/move).
- **Evaluation**: material plus pawn advancement and a compact
  centrality formula (knights ×2, bishops/rooks/queens ×½) —
  piece-square-table flavour with zero table bytes.

## Interface

Primary (the graded protocol): when run as a script, the engine
talks HTTP to the URL in the `MAKEFUN_ENV_URL` environment
variable — `POST /game` to get `{status, game, fen, legal_moves}`,
then `POST /move` with a UCI move string while the status is
`your_move`. The only network it touches is that official env URL.

It also exposes `choose_move(board, history, time_left, color)`,
which takes a FEN string and returns a UCI move string, for
harnesses that call the engine as a function.

## Tests

Perft suites all exact; 5/5 mate-in-1 puzzles solved via
`choose_move`; self-play completes legally (103 plies, checkmate);
exhibition matches at a reduced node cap: 10–0 vs a random mover
and 10–0 vs a greedy 1-ply material mover.

## License

MIT — see `LICENSE`.

## Round 3 — what changed after the first practice grade

The first graded practice run scored 0: the program asked the env
server for a new game only once, then kept moving in a finished game
until the server refused it and the process died. This version asks
for a fresh game after every finish, survives refused requests, and
checks the server's legal-move list before replying. The search also
grew real piece-square tables, quiescence that answers checks with
evasions instead of standing pat, and a repetition guard — the
combination that lifted the practice replica from 0.5/6 to 3.0/6.
