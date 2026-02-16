# The Legend of Zelda

This project is a python/pygame port of the original Legend of Zelda.


<img width="513" alt="Screen Shot 2024-08-05 at 9 21 56 AM" src="https://github.com/user-attachments/assets/be16a9bc-9f1e-49b8-a439-5784d1b7ef47">

### Features

- Link can walk in every direction with animation
- Link cannot pass through solid objects (tile-based collision)
- The entire overworld is rendered and traversable
- Sliding room-to-room transitions
- Pixel-perfect collision detection on sprite borders

### Project Structure

```
├── zelda.py         # Main game loop
├── player.py        # Player (Link) sprite and movement
├── tilemap.py      # Tile map rendering
├── tileset.py      # Sprite sheet loader
├── utils.py        # Map parsing and utilities
├── assets/         # Sprites, sounds, map data
├── levels/         # Level definitions
├── tests/          # Unit tests
└── requirements.txt
```

### Running the Game

```bash
# Create virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python zelda.py
```

### Controls

- **Arrow Keys**: Move Link

### Testing

```bash
pytest tests/
```

### Architecture

- **Game class**: Main loop, rendering, room transitions
- **Player class**: Movement, animation
- **Tilemap class**: Room rendering, collision detection
- **Tileset class**: Sprite sheet loading and tile extraction
