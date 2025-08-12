**Catch the Diamond — OpenGL Game in Python**
This is a simple 2D arcade-style game built with Python and OpenGL (via PyOpenGL and GLUT). The player controls a horizontal catcher at the bottom of the window, moving it left and right with arrow keys to catch a falling diamond shape.

Features:
-Custom-drawn shapes using a midpoint line drawing algorithm with zone transformations.

-Real-time user input handling for smooth catcher movement.

-Dynamic diamond that falls with increasing speed.

-Collision detection between catcher and diamond.

-Pause, restart, and exit buttons with clickable UI elements.

-Score tracking and game-over condition when the diamond is missed.

Technical Details:
-Uses low-level OpenGL primitives for rendering lines and points.

-Implements frame-rate independent movement using elapsed time (dt).

-Contains logic to restrict catcher movement within window bounds.

-Modular structure separating drawing, input handling, game state, and logic.

Usage:
-Run the script with Python. Use left/right arrow keys to move the catcher. Click UI buttons to pause, restart, or exit the game.
