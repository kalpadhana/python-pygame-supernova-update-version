# 🌟 SuperNova

A thrilling 2D vertical scrolling space shooter game built with Python and Pygame. Navigate through space, battle enemies, dodge meteors, and face challenging boss encounters in this action-packed arcade experience!

## 🎮 Game Preview







## ✨ Features

### 🚀 Core Gameplay
- **Vertical scrolling space shooter** with smooth 60 FPS gameplay
- **Roguelite Level-Up System** with modular perks (Speed, Health, Drones, Fire Rate)
- **Time-Bending Ultimate Ability** - Charge your meter through combat to slow down enemies and bullets
- **Progressive difficulty system** that dynamically scales enemy and boss health
- **Resource management** - manage modern health bars and limited ammunition strategically
- **Multiple control options** - keyboard, mouse clicks, and gamepad/joystick support
- **Dynamic backgrounds** that change as you progress through different sectors

### 🎯 Combat System
- **Player-controlled spacecraft** with multi-directional movement and an Invincibility Dash
- **Floating Damage Numbers** to clearly display RPG-style hits on enemies and yourself
- **Bullet-based combat** facing enemies that dynamically spawn their own targeting projectiles
- **Three types of advanced enemies** that track you, repel off each other, and shoot back
- **Epic boss battles** featuring three distinct encounters with complex bullet-hell mechanics
- **Companion Drones** - automated helpers that orbit your ship and shoot nearby threats

### 🎁 Power-ups & Collectibles
- **Health Refills** - Restore your spacecraft's modern UI health bar
- **Bullet Refills** - Replenish ammunition supplies
- **Double Refills** - Special power-ups for enhanced capabilities
- **Extra Score** - Bonus points to boost your permanent Leaderboard rankings

### 🌌 Environmental Hazards
- **Meteor showers** with varying sizes, speeds, and explosion radii
- **Black holes** that exert gravitational pulls and pose intense navigation challenges
- **Dynamic background transitions** at score milestones (3K, 10K, 15K points)

### 🎵 Audio Experience
- **Spatial Background music** with dynamic volume-controlled audio mixing
- **Sound Event Bus** managing dedicated sound effects for explosions, ultimate abilities, and dash moves

## 🎮 Controls

### Keyboard & Mouse Controls
- **Arrow Keys** - Move your spacecraft (supports diagonal movement)
- **Spacebar** - Shoot bullets (hold for continuous fire)
- **Left Shift / Right Shift** - Perform an evasive Dash with Invincibility Frames
- **Enter (Return)** - Trigger Ultimate Ability ("Bullet Time") when fully charged
- **Mouse Click / Arrow Keys** - Select your Roguelite level-up perk
- **P / Pause** - Open modern pause menu
- **Escape** - Exit the game

### Gamepad/Joystick Controls
- **Left Stick** - Move spacecraft in all directions
- **Button 0 (A)** - Shoot bullets / Select Perks
- **Button 3 (Y)** - Trigger Ultimate Ability
- **Button 4 / 5 (Bumpers)** - Perform evasive Dash
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
├── main.py                 # Main game loop and core logic
├── menu.py                 # Main menu system with navigation
├── advanced_menus.py       # Modern UI pause and settings menus
├── controls.py             # Player input handling (keyboard/gamepad)
├── functions.py            # Utility functions (audio, game over screen)
├── modern_features.py      # Dash, Ultimate, Drones, & Roguelite Leveling managers
├── modern_ui.py            # High-fidelity health bar & UI overlays
├── achievements.py         # In-game trophy and achievement tracker
├── enemy_types.py          # AI behaviors & advanced entity logic
├── game_difficulty.py      # Dynamic difficulty scaling architecture
├── game_modes.py           # Alternate modes & game state tracking
├── leaderboard.py          # High score storage system
├── particle_effects.py     # Modern rendering visual particles
├── powerups.py             # Dynamic logic for spawning multi-tier powerups
├── sound_manager.py        # Centralized audio event bus system
├── visual_effects.py       # Screen shake and hit-flash renderer
├── weapons.py              # Expandable armory & bullet patterning
├── requirements.txt        # Project dependencies
├── json/ (auto-generated)  # Local storage for stats, leaderboards & achievements
├── classes/                # Classic entity module classes
│   ├── player.py           # Core spacecraft logic
│   ├── bullets.py          # Base bullet projectile classes
│   ├── enemies.py          # Standard enemy mechanics
│   ├── bosses.py           # Boss encounter scripting
│   ├── meteors.py          # Environmental hazards
│   ├── refill.py           # Pickup item classes
│   ├── explosions.py       # Standard visual collision effects
│   └── constants.py        # Display and FPS definitions
├── images/                 # Sprite assets and graphics
└── game_sounds/            # Audio files and music
```

## 🎯 Advanced Gameplay Mechanics

### Roguelite Metaprogression
- **XP Orbs** drop on enemy and boss kills
- **Leveling Up** completely pauses the game and prompts a random choice of 3 permanent upgrades
- **Upgrades Include:** Increasing max HP, decreasing firing delay, increasing movement speed, or summoning orbital Drones.

### Bullet Time Ultimate
- Hitting enemies charges a secondary meter on the screen
- Once optimally charged, pressing **Enter/Y** drastically slows down enemy speed and bullet logic
- Gives the player precious seconds to thread through dense bullet-hells

### Scoring & Achievements
- **Enemy defeats** contribute to your real-time score
- **Boss victories** act as massive milestones
- **Achievement Unlocks** visually appear for milestones like passing 10k points or surviving 3 boss encounters
- **Persistent Leaderboard** securely stores your highest ranks across multiple application sessions
- **Boss victories** provide substantial score bonuses
- **Collectible items** offer additional points
- **High score tracking** across game sessions

### Difficulty Progression & Levels
The game features a dynamic difficulty system that scales with your score and survival time:

- **Sector 1 (0 - 3,000 points):** Initial difficulty. Introduces basic tracker enemies and meteor fields. 
- **Sector 2 (3,000 - 10,000 points):** Background warp. Introduces aggressive shooting enemies and increased spawn rates.
- **Sector 3 (10,000+ points):** Hostile territory. Introduces complex enemy formations and bullet-hell mechanics.
- **Boss Encounters:** At specific milestones, regular enemy spawns halt, and you must defeat colossal Boss ships with unique attack patterns to proceed.
- **Dynamic Scaling:** Powered by the new difficulty architecture, enemy health, bullet speed, and fire rates dynamically increase as your score climbs.

### Player Character Levels & Perks
- **Experience (XP):** Defeating enemies and bosses drops XP.
- **Roguelite Level-Up:** Filling the XP bar pauses the game and provides a choice of 3 randomized permanent upgrades.
- **Build Variety:** Stack perks like Orbital Drones, Fire Rate enhancements, Max HP buffs, and Movement Speed boosts to adapt to the rising difficulty.

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

