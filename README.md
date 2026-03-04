# Moodhoops Pattern Utils

A Python toolkit for manipulating and transforming LED light patterns. This module provides utilities to load, modify, and save pattern images with various transformation features.

## Setup Instructions

### Step 1: Install Python 3.13

1. Visit [python.org](https://www.python.org/downloads/) and download **Python 3.13**
2. Run the installer
3. **Important**: Check the box that says "Add Python to PATH" during installation
4. Click "Install Now"

### Step 2: Open the Project in VS Code

1. Download and install [Visual Studio Code](https://code.visualstudio.com/)
2. Open VS Code
3. Go to **File → Open Folder**
4. Navigate to and select the `moodhoops.pattern.utils` folder
5. Click **Select Folder**

### Step 3: Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your computer.

1. In VS Code, open the **Terminal** (View → Terminal, or press Ctrl+`)
2. Run this command:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```
     .venv\Scripts\activate.bat
     ```

You should see `(.venv)` appear at the start of your terminal prompt.

### Step 4: Install Requirements

With the virtual environment activated, run:
```
pip install -r requirements.txt
```

This installs all the libraries needed to run the pattern utilities.

### Step 5: Install Recommended Extensions

In VS Code, install these extensions for a better development experience:
1. **Python** - Provides syntax highlighting, IntelliSense, and debugging support
2. **Color Highlight** - Highlights color codes in your editor for easy visualization

To install:
1. Open the **Extensions** panel (Ctrl+Shift+X)
2. Search for each extension by name
3. Click **Install**

---

## Features

### 1. Slow Down Pattern

The **Slow Down Pattern** feature repeats rows in a pattern image to simulate slowing down animation. This is useful for creating slower-speed versions of LED patterns.

**How it works:**
- Takes a pattern image and stretches it vertically by repeating rows
- Supports fractional stretch ratios for precise control
- Example: If you want to convert a pattern from 300 RpS to 250 RpS, it will intelligently distribute extra row duplicates to maintain smooth transitions

**Parameters:**
- `canvas`: The image data (numpy array)
- `mode_speed`: Current speed of the mode the pattern is in (1-500)
- `desired_speed`: Target speed to slow down to (1-500, must be less than mode_speed)

### 2. Swap Colors

The **Swap Colors** feature replaces specific colors in a pattern with different colors.

**How it works:**
- Finds all pixels of a specific color and replaces them with a new color
- Supports multiple color swaps in one operation
- Accepts colors as hex codes (#FF5733) or RGB values (255, 87, 51)

**Parameters:**
- `canvas`: The image data (numpy array)
- `color_maps`: A list of color replacements
  - Each item has `"from"` (original color) and `"to"` (replacement color)

---

## Quick Start: Using Jupyter Notebook

The easiest way to use these tools is with a Jupyter notebook. Here's how to work with pattern images:

### 1. Create a New Notebook

1. In VS Code, press **Ctrl+Shift+P** (or Cmd+Shift+P on Mac)
2. Type "Create: New Jupyter Notebook"
3. Select it and save the file (e.g., as `pattern_demo.ipynb`)

### 2. Load and Preview an Image

Add this code to the first cell and run it:

```python
import moodhoops as mh

# Load your pattern image
image_path = "path/to/your/image.bmp"
canvas = mh.load_image(image_path)

# Display the image
from moodhoops.utils.image_io import preview_pattern
preview_pattern(canvas)
```

### 3. Apply a Feature (Slow Down)

Add a new cell:

```python
# Slow down from 300 RpS to 250 RpS
slowed_canvas = slow_down_pattern(canvas, mode_speed=300, desired_speed=250)

# Display the result
preview_pattern(slowed_canvas)
```

### 4. Apply a Feature (Swap Colors)

Add a new cell:

```python
# Define color replacements
color_maps = [
    {"from": "#FF0000", "to": "#0000FF"},  # Red → Blue
    {"from": "#00FF00", "to": "#FFFF00"}   # Green → Yellow
]

# Apply color swaps
colored_canvas = mh.swap_colors(canvas, color_maps)

# Display the result
preview_pattern(colored_canvas)
```

### 5. Save the Modified Pattern

Saved patterns will be stored in the `exports` folder of this project.
You may copy them out from there.

**WARNING** This tool will overwrite files without asking you.
Always save your work!

Add a new cell:

```python
# Save the modified pattern
save_image(slowed_canvas, "slowed_pattern")
```

---

## Complete Example Notebook

Refer to the provided `FeatureDemos.ipynb` jupyter notebook for an example.

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'moodhoops'"**
- Make sure the virtual environment is activated (you should see `(.venv)` in your terminal)
- Reinstall requirements: `pip install -r requirements.txt`

**"Image file not found"**
- Use the full path to your image or check that the file exists
- On Windows, use forward slashes or double backslashes: `"C:/path/to/image.bmp"` or `"C:\\path\\to\\image.bmp"`

**Jupyter notebook won't start**
- Ensure you're in the project folder in VS Code's terminal
- Make sure the virtual environment is activated
- Try: `pip install jupyter`

---

## Getting Help

For setup assistance or technical issues, reach out to your tech support contact.
