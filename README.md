
# Sum 10 Game Bot

A Python-based automated game bot that uses computer vision and mouse automation to play grid-based games.

## Overview

This project contains a game bot that can automatically play games by analyzing screenshots and controlling mouse movements. The bot is designed to work with both web-based games and mobile applications (WeChat).

## Project Structure

- `game_bot.py` - Main bot implementation
- `solver.py` - Game logic and solving algorithms
- `utils.py` - Utility functions for image processing
- `mouse_motion_controller.py` - Mouse automation controller
- `config.py` - Configuration settings for different display resolutions
- `Pipfile` - Python dependencies

## Features

- **Computer Vision**: Uses OpenCV for image processing and game state analysis
- **Mouse Automation**: Automated mouse movements using PyAutoGUI
- **Multi-Resolution Support**: Configurable for different screen resolutions (webpage and WeChat mobile)
- **Grid-Based Game Support**: Designed for games with cell-based grids

## Configuration

The `config.py` file contains display-specific settings:

### Web Version
- Cell center start position: (510, 292)
- Board start position: (485, 271)
- Cell width: 54 pixels

### WeChat Version (2304×972 resolution)
- Cell center start position: (50, 255)
- Board start position: (30, 233)
- Cell width: 41 pixels

## Requirements

- Python 3.10+
- OpenCV (`cv2`)
- PyAutoGUI
- Conda/Pipenv for package management

## Installation

1. Clone the repository
2. Install dependencies using pipenv:
   ```bash
   pipenv install
   ```
3. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

## Usage

1. Configure the display settings in `config.py` based on your target platform
2. Run the game bot:
   ```bash
   python game_bot.py
   ```

## Configuration Options

- `display_img`: Toggle image display for debugging
- Adjust coordinate values based on your screen resolution and game position
- Modify cell dimensions to match your specific game layout

## Notes

- Make sure the game window is visible and positioned correctly before running the bot
- The bot uses screenshot analysis, so ensure good contrast and visibility
- Test with `display_img = True` first to verify proper detection

## Contributing

Feel free to submit issues and enhancement requests!
