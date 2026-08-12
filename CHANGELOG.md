# Changelog

All notable changes to the SG++ project will be documented in this file.

## [v0.6.0] - 2026-08-12

### Added
- **GUI Configuration Manager (`gui.py`)**: Built a full Tkinter/ttk interface with tabs for General Settings, Macro Keybinds, and Shortcut Messages.
- **Interactive Key Capture**: Added a `[Press Key]` button next to all keybind inputs in the GUI to record keypresses automatically without memorizing scancodes.
- **Human-Readable Key & Scancode Displays**: Displays clear key names alongside scancodes (e.g. `Numpad 1 (Scancode 79)` vs `1 (Scancode 2)`).
- **High-DPI Per-Monitor Awareness**: Enabled `ctypes.windll.shcore.SetProcessDpiAwareness(2)` for crisp rendering and accurate coordinate calculations on 4K and scaled monitors.
- **Quit Camera View Hotkey (`quit_camera_view`)**: Added a dedicated hotkey (default `X`) that clicks the camera bar exit cross and simulates a Backspace keypress.
- **Customizable Shortcut Messages System**: Replaced deprecated lettered zones A-G with default Zones 1-10 and an expandable GUI table supporting an indefinite number of custom shortcut messages.
- **Clear Settings Window vs App Exit Buttons**: Clarified GUI footer buttons (`Close Settings` vs `Exit Entire App`).

### Changed
- **Direct Rollback Toggle Behavior**: Updated `click_rollback()` to use direct signal aspect selection behavior (`click_signal("r")`) matching updated in-game SCR signal dialog keybinds, replacing the legacy side-menu navigation.

### Fixed
- **Issue #79 Fix**: Resolved `NameError: name 'label' is not defined` exception when toggling the macro with status indicator overlay disabled.
- **Screen Overlay Centering**: Fixed `move_text_pos()` to measure window dimensions dynamically and center the SG+/SG- indicator box horizontally.
