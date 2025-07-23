"""Configuration settings for the game bot."""

from dataclasses import dataclass
from enum import Enum


class Platform(Enum):
    """Supported platforms."""
    WEBPAGE = "webpage"
    WECHAT = "wechat"


@dataclass
class DisplayConfig:
    """Display configuration for different platforms."""
    cell_center_start_x: int
    cell_center_start_y: int
    board_start_x: int
    board_start_y: int
    cell_width: int


class Config:
    """Central configuration manager."""
    
    # Debug settings
    DISPLAY_IMG = False
    
    # Platform configurations
    CONFIGS = {
        Platform.WEBPAGE: DisplayConfig(
            cell_center_start_x=510,
            cell_center_start_y=292,
            board_start_x=485,
            board_start_y=271,
            cell_width=54
        ),
        Platform.WECHAT: DisplayConfig(
            cell_center_start_x=42,
            cell_center_start_y=197,
            board_start_x=20,
            board_start_y=178,
            cell_width=49
        )
    }
    
    # Game constants
    BOARD_ROWS = 16
    BOARD_COLS = 10
    TARGET_SUM = 10
    
    @classmethod
    def get_config(cls, platform: Platform = Platform.WEBPAGE) -> DisplayConfig:
        """Get configuration for specified platform."""
        return cls.CONFIGS[platform]


# Current active configuration (can be changed as needed)
CURRENT_PLATFORM = Platform.WECHAT
current_config = Config.get_config(CURRENT_PLATFORM)

display_img = Config.DISPLAY_IMG