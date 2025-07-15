
# Participation Tracker

This is a simple command-line tool for tracking participation points. It's designed to be used in a classroom or group setting to keep a running tally of scores for individuals. The script is interactive and saves its state between sessions.

## Features

* **Load Names:** Can initialize the list of participants from a `.rtf` or a plain `.txt` file.
* **Persistent Scores:** Saves scores to a `scores.txt` file and loads them automatically on startup.
* **Interactive Command Loop:** Provides a simple command-line interface to manage scores.
* **Fuzzy Name Matching:** You don't have to type the full, exact name; the script will find the closest match.
* **Score Adjustments:** Add or subtract points, or set a score to an absolute value.
* **Add/Remove Participants:** Easily add new people or remove existing ones.
* **Undo Functionality:** Revert the last one or more operations.
* **Random Participant Selection:** Pick a random person from the list.
* **Human-Readable Output:** Displays a nicely formatted leaderboard.

## Setup

1.  **Python:** Make sure you have Python 3 installed on your system.
2.  **Initial Names File:**
    * Create a file named `names.rtf` or `names.txt` in the same directory as the script.
    * List the full names of all participants, with one name per line.
    * The script will use this file to create the initial `scores.txt` file if one doesn't already exist.

## How to Run

Open a terminal or command prompt, navigate to the directory where `participation.py` is located, and run the script:

`python participation.py`

The script will either load existing scores from `scores.txt` or create a new one based on your names file. You will then see the current leaderboard and a `>>` prompt to enter commands.

## Commands

The script accepts the following commands:

| Command                 | Description                                                                    | Example                                         |
| ----------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------- |
| `<name>`                | Adds 1 point to the best matching name.                                        | `>> john doe`                                   |
| `<name> <Δ>`            | Adds a specific number of points (can be negative).                            | `>> jane doe 5` <br> `>> jane doe -2`            |
| `adjust <name> <score>` | Sets the score for a person to an exact value.                                 | `>> adjust john doe 10`                         |
| `add <name>`            | Adds a new person to the list with a score of 0.                               | `>> add new person`                             |
| `remove <name>`         | Deletes a person from the list.                                                | `>> remove john doe`                            |
| `delete <name>`         | Same as `remove`.                                                              | `>> delete john doe`                            |
| `undo [n]`              | Reverts the last `n` operations. If `n` is not given, it defaults to 1.        | `>> undo` <br> `>> undo 3`                      |
| `random`                | Picks and displays a random name from the list.                                | `>> random`                                     |
| `help` or `commands`    | Shows the list of available commands.                                          | `>> help`                                       |
| `exit`                  | Quits the script, saving the final scores.                                     | `>> exit`                                       |

## File Formats

### Input: `names.rtf` or `names.txt`

This is a simple text file containing one name per line. The script is designed to parse RTF files from which you might copy/paste a class roster, stripping out the formatting. A plain `.txt` file also works.

**Example `names.txt`:**

`Alice Smith`\n
`Bob Johnson`\n
`Charlie Brown`

### Output: `scores.txt`

This file is created and managed by the script. It contains two parts:

1.  **A human-readable table:** A nicely formatted leaderboard that's easy to read.
2.  **Tab-separated data:** A section that the script uses for reliably reading the scores back into memory. You should not need to edit this file manually.

## Dependencies

The script uses only standard Python libraries (`re`, `pathlib`, `difflib`, `random`), so no special installation of packages is required.
