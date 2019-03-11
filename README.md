[Catan Universe](https://catanuniverse.com/) (web or app) watcher/statistics for City & Knigths games (dice and color stats)

![screenshot](https://raw.githubusercontent.com/ldeb/catan-universe-CK-stats/master/screenshot.png)

# Instructions:
Made for a 1920x1080 resolution on main screen, Chrome browser with 2 lines of tools and extanded to screen borders

# Limitation:
will miss 2 dice in a row if they look exactly the same (sames dices and color)

# Requirements:
- web server with PHP
- python environment: PIL, [pyscreenshot](https://github.com/ponty/pyscreenshot), numpy, pywinauto (unused yet)
- adjust config.py

# Installation:
(todo)

## Start: (adjust to match your directory)
```
cd workspace/python/livecatan
source ../pyscreenshot/venv/Scripts/activate
python -m main
```

**to start directly**
`python -m main start`

**to run for Catan Universe Steam application (in fullscreen)**
`python -m main app`

# TODO:
## Web:
  - no last dice unsel on color change (?)
  - show total duration / show last date modif date
  - save in cookie
  - start/stop python (doable?)
  - proportionnal bars on the left

## Python:
  - Desired usage: python -m livecapture pos_x pos_y delay
  - or -m livecapture -mode=catan
  - or list windows and choose one
  - to avoid useless captures, scan for top dice black border inner position
  - check for special color dice positions too!
  - take into account if same dice but different background (miss-click case)
