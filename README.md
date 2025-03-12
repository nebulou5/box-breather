# Box Breather

A Python script that animates a circle moving around a box with customizable parameters, built using Pygame. Suitable for box breathing or other breathing exercises where you breathe, hold, exhale, hold for set durations. Includes an optional timer that displays the total duration and allows restarting or quitting when complete.

![Alt text](box_breather.png)

## Installation

1. **Clone the Repository**

   Use `git clone https://github.com/nebulou5/box-breather.git` to clone the repository, then `cd box-breather` to enter the directory.

2. **Install Dependencies**

   Run `pip install pygame` to install Pygame. Ensure you have Python 3 installed before running this command.

## Running the Script

The script can be run with command-line arguments or a config file. The circle moves in a box, growing in size along the top horizontal leg, staying large on vertical legs, and shrinking along the bottom horizontal leg. An optional timer can be set to run the animation for a specific duration, displayed at the top of the window.

### Command-Line Options

1. **Single Duration**

   All legs use the same duration (in seconds): run `python box_breather.py 2`.

2. **Horizontal and Vertical Durations**

   First number for horizontal legs, second for vertical: run `python box_breather.py 2 3`.

3. **Individual Leg Durations**

   Four numbers for each leg (top-left to top-right, top-right to bottom-right, bottom-right to bottom-left, bottom-left to top-left): run `python box_breather.py 1 2 3 4`.

4. **Using a Config File**

   Specify a config file with `--config`: run `python box_breather.py --config=config.txt`.

### Config File Usage

![Alt text](box_breather_style.png)

Create a text file (e.g., `config.txt`) with one option per line in `key=value` format. Example:

`leg1_time=1`  
`leg2_time=2`  
`leg3_time=3`  
`leg4_time=4`  
`background_color=255,255,255`  
`box_color=0,0,0`  
`circle_color=255,0,0`  
`box_width_percent=0.5`  
`box_height_percent=0.5`  
`box_thickness=2`  
`circle_start_radius=20.0`  
`circle_end_radius=60.0`  
`display_text=true` 
`timer_duration=5:30` 
`timer_color=0,0,0` 

Run with: `python box_breather.py --config=config.txt`.

#### Configuration Parameters

- `leg1_time`: Duration (seconds) for top-left to top-right
- `leg2_time`: Duration (seconds) for top-right to bottom-right
- `leg3_time`: Duration (seconds) for bottom-right to bottom-left
- `leg4_time`: Duration (seconds) for bottom-left to top-left
- `background_color`: RGB tuple (e.g., `255,255,255` for white)
- `box_color`: RGB tuple (e.g., `0,0,0` for black)
- `circle_color`: RGB tuple (e.g., `255,0,0` for red)
- `box_width_percent`: Box width as a percentage of window width (0.0 to 1.0)
- `box_height_percent`: Box height as a percentage of window height (0.0 to 1.0)
- `box_thickness`: Box outline thickness in pixels
- `circle_start_radius`: Initial circle radius (float)
- `circle_end_radius`: Maximum circle radius (float)
- `display_text:` Controls the display of remaining duration text inside the circle.
  - Set to `false` (or omit) for no text (default behavior).
  - Set to `true` to display the remaining time in seconds using the box color.
  - Alternatively, set to an RGB tuple (e.g., `0,255,0`) to use a custom color for the text.
- `timer_duration`: Total duration of the animation in `mm:ss` format (e.g., `5:30` for 5 minutes and 30 seconds). Defaults to `5:00` if not specified.
- `timer_color`: RGB tuple for the timer text color (e.g., `0,0,0` for black). Defaults to black.

### Notes

- If no arguments or config file is provided, defaults to 2 seconds per leg with standard colors and sizes, and a 5-minute timer.
- Window is resizable; box and circle adjust smoothly.
- Press ESC or close the window to exit at any time.
- When the timer reaches zero, the animation stops, and a message appears: "Timer complete! Press 'R' to restart or 'Q' to quit." Press 'R' to restart the timer, or 'Q' to exit the program.
