# SG++: an enhanced SCR Signalling Macro

> **Note**: This repository is an enhanced **fork** of the original [SCR-SGPlus](https://github.com/ElectricityMachine/SCR-SGPlus) project created by [ElectricityMachine](https://github.com/ElectricityMachine).

## What is it?
SG++ (SG Plus Plus) is a Python macro script for Stepford County Railway (SCR) that automates common signalling workflows. It enables signallers to open camera views, toggle rollback settings, change signal aspects, and send zone opening messages with hotkeys.

## Fork Features (v0.6.0)
- **GUI Configuration Manager**: Full graphical interface to easily edit settings, hotkeys, and shortcut messages with live apply.
- **Interactive `Press Key` Keybind Capture**: Click `Press Key` in the GUI and press any key to set keybinds automatically—no need to memorize scancodes. Clear human-readable labels display both key names and scancodes (e.g. `Numpad 1 (Scancode 79)`).
- **High-DPI Per-Monitor Awareness**: Native rendering and scaling support for 4K / High-DPI displays without screen offset bugs.
- **Zones 1-10 & Unlimited Shortcut Messages**: Legacy lettered zones (A-G) are deprecated in favor of numbered Zones 1-10. An expandable table allows adding an indefinite number of custom shortcut messages.
- **Quit Camera View Hotkey**: Dedicated hotkey (default `X`) to quit camera view by clicking the top-bar cross and simulating Backspace.
- **Horizontally Centered Status Indicator**: Cleanly centered SG+/SG- screen overlay.
- **Issue #79 Resolution**: Fixed `NameError` crash when status indicator overlay is disabled.

## Installation & Usage

### From Source
1. Download and install Python 3.12+ (ensure **Add Python to PATH** is checked).
2. Extract the repository zip.
3. Run `install.bat`.
4. Launch via `start.bat` or `python script.py`.

### Hotkeys & Usage
- Mouse over a signal:
  - Press `1`, `2`, or `3` to set signal aspects (Danger, Caution, Proceed).
  - Press `C` to view camera mode.
  - Press `X` to quit camera view (simulates X click + Backspace).
  - Press `R` to toggle signal rollback.
  - Press `F` to toggle signal side menu.
- Press `F1` to toggle macro enabled/disabled.
- Use configured shortcut message keybinds (Numpad 1-0 for Zones 1-10) to copy opening messages to clipboard.

## Configuration
All settings, keybinds, and shortcut messages can be managed via the **GUI Config Window** on launch or edited manually in `config.toml`.

##### License
Adheres to the license terms in the `LICENSE` file.
