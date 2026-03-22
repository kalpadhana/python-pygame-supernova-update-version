# 🌟 SuperNova

A thrilling 2D vertical scrolling space shooter game built with Python and Pygame. Navigate through space, battle enemies, dodge meteors, and face challenging boss encounters in this action-packed arcade experience!

## 🎮 Game Preview







## ✨ Features

### 🚀 Core Gameplay
- **Vertical scrolling space shooter** with smooth 60 FPS gameplay
- **Progressive difficulty system** that adapts based on your score
- **Resource management** - manage health and ammunition strategically
- **Multiple control options** - keyboard and gamepad/joystick support
- **Dynamic backgrounds** that change as you progress through the game

### 🎯 Combat System
- **Player-controlled spacecraft** with multi-directional movement
- **Bullet-based combat** with limited ammunition requiring strategic use
- **Three types of enemies** with unique behaviors and attack patterns
- **Epic boss battles** featuring three distinct boss encounters
- **Collision detection** with visual explosion effects

### 🎁 Power-ups & Collectibles
- **Health Refills** - Restore your spacecraft's health
- **Bullet Refills** - Replenish ammunition supplies
- **Double Refills** - Special power-ups for enhanced capabilities
- **Extra Score** - Bonus points to boost your high score

### 🌌 Environmental Hazards
- **Meteor showers** with varying sizes and speeds
- **Black holes** that pose additional navigation challenges
- **Dynamic background transitions** at score milestones (3K, 10K, 15K points)

### 🎵 Audio Experience
- **Background music** with volume-controlled audio mixing
- **Sound effects** for explosions, power-ups, and game events
- **Game state audio** including win/lose soundtracks

## 🎮 Controls

### Keyboard Controls
- **Arrow Keys** - Move your spacecraft (supports diagonal movement)
- **Spacebar** - Shoot bullets (hold for continuous fire)
- **P / Pause** - Pause/unpause the game
- **Escape** - Exit the game

### Gamepad/Joystick Controls
- **Left Stick** - Move spacecraft in all directions
- **Button 0** - Shoot bullets
- **D-pad** - Navigate menus

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/SuperNova.git
   cd SuperNova
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install Pygame directly:
   ```bash
   pip install pygame
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
SuperNova/
├── main.py              # Main game loop and core logic
├── menu.py              # Main menu system with navigation
├── controls.py          # Player input handling (keyboard/gamepad)
├── functions.py         # Utility functions (audio, game over screen)
├── requirements.txt     # Project dependencies
├── classes/             # Game entity classes
│   ├── player.py        # Player spacecraft class
│   ├── bullets.py       # Bullet projectile system
│   ├── enemies.py       # Enemy types and behaviors
│   ├── bosses.py        # Boss encounter mechanics
│   ├── meteors.py       # Environmental hazards
│   ├── refill.py        # Power-up and collectible items
│   ├── explosions.py    # Visual explosion effects
│   └── constants.py     # Game configuration constants
├── images/              # Sprite assets and graphics
├── game_sounds/         # Audio files and music
└── SuperNova.mp4        # Game preview video
```

## 🎯 Gameplay Mechanics

### Scoring System
- **Enemy defeats** contribute to your score
- **Boss victories** provide substantial score bonuses
- **Collectible items** offer additional points
- **High score tracking** across game sessions

### Difficulty Progression
The game features a dynamic difficulty system that scales with your performance:

- **0-3,000 points**: Initial difficulty with basic enemies
- **3,000+ points**: Background changes, increased enemy spawn rates
- **10,000+ points**: New background, faster enemy movement
- **15,000+ points**: Final background, maximum difficulty with all enemy types

### Health & Ammunition System
- **Player Health**: 200 HP starting health, decreases with collisions
- **Ammunition**: 200 bullets starting supply, manage wisely
- **Refill Items**: Collect power-ups to restore health and ammo

## 🛠️ Technical Details

### Built With
- **Python 3.x** - Core programming language
- **Pygame** - Game development library for graphics, audio, and input


### Architecture
- **Event-driven architecture** with centralized game loop
- **Modular design** separating concerns across multiple files
- **Object-oriented entities** using Pygame sprite classes
- **Input abstraction** supporting multiple control methods

## 🎨 Assets

The game includes custom graphics and audio:
- **Spacecraft sprites** with animation frames
- **Enemy and boss designs** with unique visual styles
- **Environmental backgrounds** that change with progression
- **Explosion animations** with multiple visual effects
- **Power-up icons** and collectible graphics
- **Background music** and sound effect library

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help improve SuperNova:

1. **Report bugs** or suggest new features
2. **Add new enemy types** or boss encounters
3. **Create additional power-ups** or gameplay mechanics
4. **Improve graphics** or audio assets
5. **Optimize performance** or add new features

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the amazing [Pygame](https://pygame.org) library
- Inspired by classic arcade space shooters
- Thanks to the Python gaming community for resources and inspiration

## 🎮 Have Fun!

Enjoy playing SuperNova! Challenge yourself to achieve the highest score and master all the boss encounters. Good luck, space pilot! 🚀

---

