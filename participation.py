from pathlib import Path
import re
from pathlib import Path
from typing import Any, Dict
import difflib
import random

_RTF_CTRL_RE = re.compile(
    r"""
        \\[a-zA-Z]+\d*\s?
      | \\['"][0-9a-fA-F]{2}
      | [{}]
    """,
    re.VERBOSE,
)

_LINE_IS_NAME = re.compile(r"[A-Za-z].*\s+.*[A-Za-z]")

HELP_TEXT = (
    "Commands:\n"
    "  • <name>                - add 1 point\n"
    "  • <name> <Δ>            - add signed integer Δ (e.g. “mia -2”, “eric 5”)\n"
    "  • adjust <name> <score> - set score exactly (overwrite)\n"
    "  • add <name>            - add a new person with 0 points\n"
    "  • remove|delete <name>  - delete that entry\n"
    "  • undo [n]              - revert the last n operations (default 1)\n"
    "  • help|commands         - show this message\n"
    "  • random                - pick a random name\n"
    "  • exit                  - quit"
)

def print_commands():
    print(HELP_TEXT)

def read_lines_to_list(path, strip_newlines=True):
    path = Path(path)

    if path.suffix.lower() == ".rtf":
        raw = path.read_text(encoding="utf-8", errors="ignore")
        raw = raw.replace(r"\par", "\n")
        text = _RTF_CTRL_RE.sub("", raw)
        text = text.replace("\\", "")

        lines = [
            ln.strip().rstrip(";,:")
            for ln in text.splitlines()
            if _LINE_IS_NAME.fullmatch(ln.strip())
        ]
        return lines
    
    with path.open(encoding="utf-8") as fh:
        return [
            line.rstrip("\n") if strip_newlines else line
            for line in fh
        ]

def load_scores(path, *, delimiter=None, value_cast=int):
    path = Path(path)
    scores: dict[str, Any] = {}

    with path.open(encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                name, raw_score = line.rstrip("\n").split(delimiter, 1)
            except ValueError as exc:
                raise ValueError(
                    f"{path}:{lineno}: expected 2 fields, got {line!r}"
                ) from exc
            scores[name.strip()] = value_cast(raw_score.strip())
    return scores

def _pretty_print(scores):
    width = max(map(len, scores), default=0) + 2
    lines = ["-" * (width + 6)]
    for name, sc in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"{name:<{width}} {sc:>3d}")
    lines.append("-" * (width + 6))
    return "\n".join(lines)

def _best_match(query, names):
    def name_parts_map(names):
        parts_map = {}
        for full_name in names:
            parts = full_name.lower().split()
            for part in parts:
                parts_map.setdefault(part, set()).add(full_name)
        return parts_map

    query_lc = query.lower()
    parts_map = name_parts_map(names)

    first_name_map = {n.lower().split()[0]: n for n in names if n.strip()}
    if query_lc in first_name_map:
        return first_name_map[query_lc]

    first_names = list(first_name_map.keys())
    first_match = difflib.get_close_matches(query_lc, first_names, n=1, cutoff=0.6)
    if first_match:
        return first_name_map[first_match[0]]

    all_parts = list(parts_map.keys())
    part_match = difflib.get_close_matches(query_lc, all_parts, n=1, cutoff=0.6)
    if part_match:
        possible_names = parts_map[part_match[0]]
        return sorted(possible_names)[0]

    full_map = {n.lower(): n for n in names}
    match = difflib.get_close_matches(query_lc, full_map.keys(), n=1, cutoff=0.0)
    return full_map[match[0]] if match else None


def _save_scores(scores, path="scores.txt"):
    path = Path(path)
    table = _pretty_print(scores)
    tsv_lines = [
        f"{name}\t{sc}"
        for name, sc in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    ]
    content = (
        "# ---- human-readable table ----\n"
        f"{table}\n\n"
        "# ---- tab-separated data ----\n"
        + "\n".join(tsv_lines)
    )
    path.write_text(content, encoding="utf-8")
    print(f"Saved to {path.resolve()}")


def adjust_score(scores):
    print(_pretty_print(scores))
    raw = input("Whose score should go up by 1? ").strip()
    if not raw:
        print("No input — nothing changed.")
        return

    name = _best_match(raw, scores.keys())
    if name is None:
        print("No similar name found.")
        return

    old = scores[name]
    scores[name] = old + 1
    print(f"\n→ {name!r}: {old} → {scores[name]}")

    if input("Type 'undo' to revert, or press Enter to keep: ").lower() == "undo":
        scores[name] = old
        print("Change reverted.")
        return
    _save_scores(scores, "scores.txt")

def load_scores(path, *, cast=int):
    path = Path(path)
    scores: Dict[str, int] = {}
    with path.open(encoding="utf-8") as fh:
        in_tsv = False
        for line in fh:
            if line.startswith("# ---- tab-separated data"):
                in_tsv = True
                continue
            if not in_tsv or not line.strip() or line.lstrip().startswith("#"):
                continue
            try:
                name, raw = line.rstrip("\n").split("\t", 1)
            except ValueError:
                raise ValueError(f"Bad line: {line!r}") from None
            scores[name] = cast(raw)
    return scores

if __name__ == "__main__":
    default_save = Path("scores.txt")

    if default_save.is_file():
        scores = load_scores(default_save)
        names  = list(scores)
        print(f"Loaded existing scores from {default_save.resolve()}")
    else:
        names   = read_lines_to_list("names.rtf")
        scores  = {name: 0 for name in names}
        print("No scores.txt found – starting fresh from names.rtf")

    print("\nCurrent leaderboard:")
    print(_pretty_print(scores))
    print_commands()

    history: list[tuple[str, int | None, bool]] = []

while True:
    raw = input("\n>> ").strip()
    if not raw:
        print("No input — nothing changed.");  continue

    tokens = raw.split()
    verb   = tokens[0].lower()

    if verb in {"help", "commands"}:
        print_commands()
        continue

    if verb == "exit":
        confirm = input("Are you sure you want to quit? [y/N] ").strip().lower()
        if confirm in {"y", "yes"}:
            print("\nFinal leaderboard:")
            print(_pretty_print(scores))
            _save_scores(scores, default_save)
            print("Goodbye!")
            break
        print("Exit cancelled — continuing.")
        continue

    if verb == "undo":
        n = 1
        if len(tokens) > 1 and tokens[1].isdigit():
            n = int(tokens[1])
        if n > len(history):
            print("Nothing to undo.");  continue

        for _ in range(n):
            name, old, was_deleted = history.pop()
            if was_deleted:
                scores[name] = old
            else:
                scores[name] = old
        print(f"Undid {n} change{'s' if n>1 else ''}.")
        print(_pretty_print(scores))
        _save_scores(scores, default_save)
        continue

    if verb in {"remove", "delete"} and len(tokens) >= 2:
        query = " ".join(tokens[1:])
        match = _best_match(query, scores.keys())
        if match is None:
            print("No similar name found.");  continue
        old_score = scores.pop(match)
        history.append((match, old_score, True))
        print(f"Deleted {match!r}.")
        print(_pretty_print(scores))
        _save_scores(scores, default_save)
        continue

    if verb == "adjust" and len(tokens) >= 3:
        query     = " ".join(tokens[1:-1])
        try:
            new_value = int(tokens[-1])
        except ValueError:
            print("Score must be an integer.");  continue
        op_type   = "set"

    if verb == "random":
        if not scores:
            print("No names available.")
            continue
        chosen = random.choice(list(scores.keys()))
        print(f"🎲 Randomly selected: {chosen}")
        continue

    if verb == "add" and len(tokens) >= 2:
        name = " ".join(tokens[1:])
        if name in scores:
            print(f"{name!r} already exists.")
            continue
        scores[name] = 0
        history.append((name, None, True))
        print(f"Added {name!r} with 0 points.")
        print(_pretty_print(scores))
        _save_scores(scores, default_save)
        continue
    
    else:
        if len(tokens) >= 2 and tokens[-1].lstrip("+-").isdigit():
            query  = " ".join(tokens[:-1])
            delta  = int(tokens[-1])
        else:
            query  = raw
            delta  = 1
        op_type   = "delta"

    match = _best_match(query, scores.keys())
    if match is None:
        print("No similar name found.");  continue

    old_score = scores[match]
    if op_type == "set":
        scores[match] = new_value
        note = f"→ {scores[match]} (set)"
    else:
        scores[match] = old_score + delta
        note = f"→ {scores[match]} ({delta:+d})"

    history.append((match, old_score, False))
    print(f"→ {match!r}: {old_score} {note}")
    print(_pretty_print(scores))
    _save_scores(scores, default_save)
    
