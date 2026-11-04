# F1 Flags RGB

F1 MultiViewer flags display on LED devices via SignalRGB.

Your keyboard, fans, strips and other RGB gear change colour to match the current F1 track status (green, yellow, red, safety car and virtual safety car), using live data from [MultiViewer for F1](https://multiviewer.app/). It can also show a driver's three sector times as coloured bars along the bottom of the canvas.

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Version](https://img.shields.io/badge/version-1.1.0-green.svg)

## Table of Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
- [Sector display](#sector-display)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Live flag colours: green (all clear), yellow, red, safety car and virtual safety car
- Safety car and VSC can flash yellow/black, or show a solid colour of your choice
- Adjustable flashing speed and idle colour
- Sector display: a driver's three sector times shown as purple, green or yellow bars
- Choose which driver to follow
- Works with any device SignalRGB supports

| Track status | Colour |
| --- | --- |
| All clear | Green |
| Yellow flag | Yellow |
| Safety car / Virtual safety car | Flashing yellow/black, or your chosen solid colour |
| Red flag | Red |
| No flag data | Default colour (black unless you change it) |

## How it works


```
MultiViewer  ->  multiviewer.py  ->  SignalRGB effect  ->  your lights
```

1. The script checks MultiViewer's local API twice a second for the track status and for one driver's sector times.
2. When either changes, the script sends it to SignalRGB.
3. The "Multiviewer Flags" effect picks it up and updates the colours.

## Requirements

- Windows 10 or 11
- [SignalRGB](https://www.signalrgb.com/) with your devices already set up
- [MultiViewer for F1](https://multiviewer.app/)
- [Python](https://www.python.org/downloads/) 3.8 or newer (tick **Add python.exe to PATH** in the installer)

## Installation

1. Download this repository: click **Code > Download ZIP** on GitHub and extract it, or clone it:

   ```bash
   git clone https://github.com/mrbiscuit921/Multiviewer-Flags.git
   cd Multiviewer-Flags
   ```

2. Copy the `Multiviewer-Flags-main` folder into your SignalRGB effects folder:

   ```
   C:\Users\YourName\Documents\WhirlwindFX\Effects
   ```

3. In SignalRGB, open the **Installed** effects and apply **Multiviewer Flags**. If it doesn't show up, restart SignalRGB.

4. Install the Python dependency. Open a terminal in the repository folder and run:

   ```bash
   pip install -r requirements.txt
   ```

   If `pip` isn't recognised, use `py -m pip install -r requirements.txt` instead.

## Usage

1. Open MultiViewer and start a session.
2. Make sure **Multiviewer Flags** is the active effect in SignalRGB.
3. In a terminal in the repository folder, run:

   ```bash
   python multiviewer.py
   ```

4. Leave that window open while you watch. Your lights will follow the track status. Close the window to stop.

**Optional:** to start it automatically when Windows boots, press `Win + R`, type `shell:startup`, and put a shortcut to `multiviewer.py` in that folder.

## Settings

Change these in SignalRGB under the effect's settings.

| Setting | What it does | Default |
| --- | --- | --- |
| Flashing Enabled | Flash yellow/black for safety car and VSC instead of a solid colour | Off |
| Safety Car Colour | Solid colour used for safety car and VSC when flashing is off | Orange (`#ffa500`) |
| Flashing Speed | How fast the safety car and VSC flash (1 to 10) | 1 |
| Default Colour | Colour shown when there is no flag data | Black (`#000000`) |

## Sector display

Three bars along the bottom of the canvas show the three sector times for one driver:

| Colour | Meaning |
| --- | --- |
| Purple | Overall fastest sector in the session |
| Green | The driver's personal best |
| Yellow | No Improvement |

SignalRGB maps your devices onto a canvas, and the bars sit along the bottom edge of it, so only devices placed there will show them.

**Choosing a driver**

Open `multiviewer.py` and change `DRIVERNUMBER` near the top to the racing number of the driver you want to follow. Keep the quotes:

```python
DRIVERNUMBER = "12"
```

Restart the script after changing it.

## Troubleshooting

**Lights stay on the default colour**

- Check that **Multiviewer Flags** is the effect currently applied in SignalRGB.
- Check that the script is running, and that MultiViewer is open with a session started and Live Timing is open.
- Run the test below to find out whether the problem is the effect or the script.

**Test the effect without MultiViewer**

With the effect applied, run this in a terminal (`curl.exe` also works in PowerShell):

```bash
curl.exe -X POST "http://localhost:16034/canvas/event?sender=F1_Multiviewer&event=redFlag"
```

If your lights turn red, the effect works and the problem is the script or MultiViewer. If nothing happens, the effect isn't applied or SignalRGB isn't running.

Other events you can test: `allClear`, `yellowFlag`, `safetyCarDeployed`, `virtualSafetyCarDeployed`.

To test the sector bars, send `sector_` followed by the three sector colours (`Fastest`, `Personal` or `None`), separated by underscores:

```bash
curl.exe -X POST "http://localhost:16034/canvas/event?sender=F1_Multiviewer&event=sector_Fastest_Personal_None"
```

**Sector bars don't appear**

- Check that the devices you want to light are placed along the bottom of the canvas in SignalRGB.
- Check `DRIVERNUMBER` in `multiviewer.py`. If the script prints `Sectors failed: ...`, that number probably isn't in the current session.
- Run the sector test above to check whether the effect or the script is at fault.


## Disclaimer

This is an unofficial fan project. It is not affiliated with or endorsed by Formula 1, MultiViewer or SignalRGB. F1, FORMULA 1 and related marks are trademarks of Formula One Licensing BV.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤ by [mrbiscuit921](https://github.com/mrbiscuit921)