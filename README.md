# Trivia Trials

**Trivia Trials** is a GUI-based quiz game built with Python and Tkinter. It fetches trivia questions from the Open Trivia Database API and challenges players to answer them correctly in a multiple-choice format. The game tracks scores and stores them in a local leaderboard.

---

## Features

- 10 randomized multiple-choice questions per game  
- Questions sourced from the Open Trivia Database (category: video games)  
- User interface built using Tkinter  
- Local leaderboard saved to `leaderboard.json`  
- Real-time feedback and scoring  

## Setup Instructions

### Prerequisites

- Python 3 installed on your system
- Internet connection to fetch trivia questions

### 1. Clone the Repository
  ```bash
    git clone https://github.com/yourusername/trivia-trials.git
    cd trivia-trials
```
### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:
  ```bash
    python3 -m venv venv
    source venv/bin/activate
```
#### On Windows:
  ```bash
    python -m venv venv
    venv\Scripts\activate
```
### 3. Pip install requests
  ```bash
pip install requests
```

## How to Play

 **Launch the game**  
   Run the Python script:  
   ```bash
   python3 trivia_trials.py
   ```
## Notes
- Trivia category is currently set to Video Games (ID 15). You can change this in the QuizContent class.
- Leaderboard is saved locally in leaderboard.json. Deleting this file will reset the scores.
