# AVL Tree Car Obstacle Game - User Manual
First data structures project 2025 - II

## Authors  
- Andrés Felipe Giraldo Rojas (47424) —  Systems and Computer Engineering Student
- Miguel Ángel Cruz Betancourt () — Systems and Computer Engineering Student

## Table of Contents
1. [Game Overview](#game-overview)
2. [System Requirements](#system-requirements)
3. [Installation and Setup](#installation-and-setup)
4. [Game Configuration](#game-configuration)
5. [How to Play](#how-to-play)
6. [Game Controls](#game-controls)
7. [Game Interface](#game-interface)
8. [AVL Tree Visualization](#avl-tree-visualization)
9. [Obstacle Management](#obstacle-management)
10. [Game Mechanics](#game-mechanics)
11. [Scoring and Energy System](#scoring-and-energy-system)
12. [Troubleshooting](#troubleshooting)
13. [Tips and Strategies](#tips-and-strategies)

## Game Overview

The AVL Tree Car Obstacle Game is a 2D side-scrolling adventure where you control a car navigating through a linear road filled with dynamic obstacles. The game features an innovative obstacle management system using AVL (Adelson-Velsky and Landis) trees for efficient obstacle organization and retrieval.

### Key Features
- **Dynamic Obstacle Management**: Obstacles are stored and managed using a self-balancing AVL tree
- **Configurable Gameplay**: Customize game parameters through JSON configuration files
- **Real-time Visualization**: View the AVL tree structure during gameplay
- **Energy-based Challenge System**: Different obstacle types affect your car's energy differently
- **Responsive Controls**: Smooth vertical movement and jumping mechanics

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python Version**: Python 3.8 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB available space
- **Display**: 1024x768 resolution minimum

### Required Python Libraries
- `pygame` (game engine)
- `tkinter` (GUI components)
- `json` (configuration management)
- `math` (mathematical calculations)

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Afelipe410/avl-tree-project.git
cd avl-tree-project
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python main.py --test
```

### Step 4: Run the Game
```bash
python main.py
```

## Game Configuration

### JSON Configuration File
The game uses a `config.json` file to customize gameplay parameters:

```json
{
  "game_settings": {
    "total_distance_km": 10,
    "car_speed_ms": 200,
    "car_advance_meters": 5,
    "jump_distance": 3,
    "refresh_rate_ms": 200,
    "car_initial_color": "#FF0000",
    "car_jump_color": "#00FF00"
  },
  "road_settings": {
    "width": 1200,
    "lanes": 3,
    "lane_height": 100
  },
  "energy_settings": {
    "initial_energy": 100,
    "obstacle_damage": {
      "rock": 15,
      "pothole": 10,
      "barrier": 25,
      "spike": 20
    }
  }
}
```

### Customizable Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `total_distance_km` | Total road distance in kilometers | 10 |
| `car_speed_ms` | Time between car advances in milliseconds | 200 |
| `car_advance_meters` | Distance car moves forward per update | 5 |
| `jump_distance` | Height of car jump | 3 |
| `refresh_rate_ms` | Screen refresh rate | 200 |
| `initial_energy` | Starting energy level | 100 |

## How to Play

### Objective
Navigate your car through a linear road for the specified distance while avoiding obstacles and maintaining energy above zero.

### Game Flow
1. **Launch Game**: Start the application and load configuration
2. **Pre-Game Setup**: Add manual obstacles if desired
3. **Begin Journey**: Watch as your car automatically advances
4. **Navigate Obstacles**: Use controls to avoid collisions
5. **Monitor Energy**: Keep track of your energy level
6. **Reach Goal**: Complete the distance or run out of energy

### Winning Conditions
- **Victory**: Reach the end of the road (total distance) with energy > 0
- **Defeat**: Energy drops to 0 or below

## Game Controls

### Keyboard Controls

| Key | Action | Description |
|-----|--------|-------------|
| `↑` | Move Up | Move car to upper lane |
| `↓` | Move Down | Move car to lower lane |
| `SPACE` | Jump | Jump over obstacles (car changes color during jump) |
| `ESC` | Pause/Menu | Open pause menu |
| `V` | View Tree | Display AVL tree visualization |
| `Q` | Quit | Exit game |

### Mouse Controls
- **Click**: Navigate menus and interface elements
- **Scroll**: Zoom in/out of tree visualization (if available)

## Game Interface

### Main Game Screen

#### Top Bar
- **Distance Counter**: Shows current position vs. total distance
- **Energy Bar**: Visual representation of remaining energy
- **Speed Indicator**: Current car advancement speed

#### Game Area
- **Car**: Your controllable vehicle (left side of screen)
- **Road**: Three-lane highway with obstacles
- **Obstacles**: Various types appearing based on your position

#### Control Panel (Optional)
- **Tree View Button**: Access AVL tree visualization
- **Settings**: Adjust game parameters
- **Pause**: Temporary game suspension

### Menu System

#### Main Menu
- **New Game**: Start fresh game session
- **Load Configuration**: Choose different JSON config file
- **Add Obstacles**: Manually insert obstacles before starting
- **View Instructions**: Display this manual
- **Exit**: Close application

#### Pause Menu (ESC key)
- **Resume**: Continue current game
- **View Tree**: Show AVL tree structure
- **Settings**: Modify game parameters
- **Restart**: Begin new game with same configuration
- **Main Menu**: Return to main menu

## AVL Tree Visualization

### Understanding the Tree Structure
The AVL tree organizes obstacles based on their coordinates:

1. **Primary Sort**: X-coordinate (distance along road)
2. **Secondary Sort**: Y-coordinate (lane position) in case of X-tie
3. **No Duplicates**: Same coordinates not allowed

### Tree Display Features
- **Node Information**: Each node shows obstacle coordinates and type
- **Balance Factors**: Visual indication of tree balance
- **Traversal Options**: 
  - **Breadth-First Search (BFS)**: Level-by-level exploration
  - **Depth-First Search (DFS)**: Branch-by-branch exploration

### Accessing Tree Visualization
1. Press `V` key during gameplay
2. Select "View Tree" from pause menu
3. Choose traversal method (BFS or DFS)
4. Navigate through tree structure

## Obstacle Management

### Obstacle Types and Effects

| Type | Energy Damage | Visual | Strategy |
|------|---------------|--------|----------|
| Rock | 15 | Gray circle | Jump over or change lanes |
| Pothole | 10 | Dark rectangle | Change lanes (jumping ineffective) |
| Barrier | 25 | Red rectangle | Must jump over |
| Spike | 20 | Triangle | Jump or careful lane change |

### Adding Manual Obstacles

#### Before Game Start
1. Select "Add Obstacles" from main menu
2. Click on desired road position
3. Choose obstacle type from dropdown
4. Confirm placement
5. Repeat as needed
6. Start game when ready

#### Coordinate System
- **X-axis**: Distance along road (0 to total_distance_km)
- **Y-axis**: Lane position (0=bottom, 1=middle, 2=top)

### Dynamic Obstacle Loading
- Obstacles appear automatically based on car's X-position
- Only visible obstacles are rendered for performance
- AVL tree enables efficient range queries for visible area

## Game Mechanics

### Car Movement
- **Automatic Forward**: Car advances 5 meters every 200ms (configurable)
- **Manual Vertical**: Player controls lane changes with arrow keys
- **Jumping**: Temporary elevation to avoid obstacles

### Screen Scrolling
- Car remains at left edge of screen
- Background scrolls right to left at car's speed
- Obstacles enter from right side based on position

### Collision Detection
- **Rectangular Hit Boxes**: Each obstacle has defined collision area
- **Jump Immunity**: Car avoids ground-level collisions while jumping
- **Energy Deduction**: Contact reduces energy based on obstacle type

### Energy System
- **Starting Energy**: 100% (configurable)
- **Energy Loss**: Variable damage per obstacle type
- **No Recovery**: Energy only decreases during gameplay
- **Game Over**: Energy reaches 0

## Scoring and Energy System

### Energy Management Strategy
- **Conservative Approach**: Avoid all obstacles when possible
- **Risk Assessment**: Some obstacles cause less damage than others
- **Jump Timing**: Master jumping to avoid high-damage obstacles

### Distance Tracking
- **Progress Indicator**: Shows completed vs. remaining distance
- **Milestone Markers**: Visual indicators at regular intervals
- **Completion Goal**: Reach 100% of configured distance

## Troubleshooting

### Common Issues and Solutions

#### Game Won't Start
**Problem**: Application fails to launch
**Solutions**:
1. Verify Python version (3.8+)
2. Install required dependencies: `pip install -r requirements.txt`
3. Check file permissions
4. Run from correct directory

#### Poor Performance
**Problem**: Game runs slowly or stutters
**Solutions**:
1. Close other applications
2. Increase refresh_rate_ms in config.json
3. Reduce total_distance_km
4. Update graphics drivers

#### Configuration Not Loading
**Problem**: JSON settings not applied
**Solutions**:
1. Verify JSON syntax validity
2. Check file path and permissions
3. Ensure all required parameters present
4. Reset to default configuration

#### Controls Not Responding
**Problem**: Keyboard input ignored
**Solutions**:
1. Click on game window to ensure focus
2. Check for conflicting key bindings
3. Restart application
4. Try different keyboard

### Error Messages

#### "Invalid Obstacle Coordinates"
- **Cause**: Attempting to place obstacle at existing coordinates
- **Solution**: Choose different position or remove existing obstacle

#### "Configuration File Missing"
- **Cause**: config.json not found or corrupted
- **Solution**: Restore default configuration file

#### "Tree Visualization Error"
- **Cause**: AVL tree corruption or display issue
- **Solution**: Restart game and avoid rapid obstacle insertion

## Tips and Strategies

### Beginner Tips
1. **Practice Controls**: Familiarize yourself with lane changes and jumping
2. **Study Patterns**: Learn obstacle spacing and types
3. **Energy Conservation**: Avoid unnecessary risks
4. **Use Tree View**: Understand upcoming obstacles through visualization

### Advanced Strategies
1. **Predictive Movement**: Anticipate obstacle placement using tree traversal
2. **Energy Optimization**: Calculate minimum energy needed for completion
3. **Speed Adjustment**: Modify configuration for desired difficulty
4. **Custom Obstacles**: Create challenging custom obstacle courses

### Performance Optimization
1. **Reduce Visual Effects**: Lower graphics settings if needed
2. **Adjust Refresh Rate**: Balance smoothness with performance
3. **Limit Tree Visualization**: Use sparingly during gameplay

### Configuration Experimentation
1. **Difficulty Scaling**: Adjust damage values and car speed
2. **Course Length**: Experiment with different distances
3. **Obstacle Density**: Control challenge level through obstacle placement

## Conclusion

The AVL Tree Car Obstacle Game combines classic arcade-style gameplay with computer science education. By mastering the controls and understanding the AVL tree structure, players can develop both gaming skills and algorithmic thinking.

For technical support or advanced configuration options, please refer to the Technical Manual or contact the development team.
