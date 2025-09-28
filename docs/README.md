# User Manual: AVL Tree Game

## Presented by:
- Andrés Felipe Giraldo Rojas — Systems and Computer Engineering Student
- Miguel Ángel Cruz Betancourt — Systems and Computer Engineering Student

## Presented to:
- Jeferson Arango López — Professor - Department of Systems and Computer Science

## What is this game?
It is a 2D game where you drive a car that automatically moves forward on a road full of obstacles. The interesting thing is that it uses the “AVL Trees” data structure to organize the obstacles in an intelligent and balanced way.

## What do you need to play it?
- Python version 3.8 or newer

### Python required. Libraries
- `tkinter` (graphical user interface components)
- `json` (configuration management)

## Installation and configuration

### Step 1: Clone the repository
git clone https://github.com/Afelipe410/avl-tree-project.git
cd avl-tree-project

### Step 2: Install dependencies
pip install -r requirements.txt

### Step 3: Verify the installation
python main.py --test

### Step 4: Run the game
python main.py

### Customizable parameters

You can change things like:
- How fast your car goes
- How far you have to travel
- The height of the jump
- Colors of the car, goal, and more

All of this is modified in a json file.

{
  “config”: {
    “game”: {
      “distance_total”: 10000,
      “speed”: 6,
      “jump_height”: 70,
      “refresh_ms”: 30,
      “car_color”: “#AAA0A0”
    }
  },
  “obstacles”: [
    {
      “id”: 1,
      “name”: “Cone”,
      “color”: “#E67E22”,
      “text_color”: “#FFFFFF”,
      “x_world”: 500,
      “lane_idx”: 1,
      “width”: 32,
      “height”: 32
    },
    {
      “id”: 2,
      “name”: “Rock”,
      “color”: “#95A5A6”,
      “text_color”: “#2C3E50”,
      “x_world”: 1200,
      “lane_idx”: 2,
      “width”: 32,
      “height”: 32
    }
  ]
}

## How to play

### The objective
Your car moves forward on its own along the road. You need to avoid crashing into obstacles so that you reach the end with enough energy. If you crash into obstacles, your energy will drop to zero and you will lose.

### Basic controls
- **Up/down arrows**: Change lanes, i.e., upper lane and lower lane
- **Space bar**: Jump (the car changes color when it jumps) and when it returns from the jump, it returns to its initial color
- **ESC**: Pause the game

### Types of obstacles (from least to most dangerous)
- **Pothole**: Takes away 1 energy point 
- **Rock**: Takes away 3 energy points
- **Spikes**: Take away 5 energy points
- **Barrier**: Takes away 7 energy points 

### Main game screen

#### Top bar
- **Energy bar**: Visual representation of remaining energy in a bar
- **Graphical representation of the AVL tree**: You can see the AVL tree while you play

## The educational part: The AVL Tree
This game teaches you how an AVL tree works while you play. Obstacles are organized in the tree according to their position on the road. You can see this structure by pressing the “V” key during the game.

## Strategies for winning
1. **At the beginning**: Practice the basic controls
2. **Study the patterns**: Learn where the obstacles appear
3. **Take care of your energy**: Avoid colliding with obstacles
4. **Use the tree view**: It helps you see what obstacles are coming

## Technical problems?
- **The game won't start**: Check that you have Python 3.8+ installed
- **It's running very slowly**: Close other programs
- **The controls aren't responding**: Click on the game window (i.e., click on the road)

## In summary
It's a fun game that combines entertainment with learning. While avoiding obstacles, you also learn about data structures. 
---
Developed by Andrés Felipe Giraldo Rojas and Miguel Ángel Cruz Betancourt for the Data Structures 2025 course.
University of Caldas, Manizales - Colombia.