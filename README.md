[Catan Universe](https://catanuniverse.com/) (web or app) watcher/stats for City & Knigths games

# INSTRUCTIONS:
Made for a 1920x1080 resolution on main screen, Chrome browser with 2 lines of tools and extanded to screen borders

# LIMITATION:
will miss 2 dice in a row if they look exactly the same (sames dices and color)

# REQUIREMENTS:
- web server with PHP
- python environment

# INSTALLATION:
(todo)

# START for windows:
cd workspace/python/livecatan					# adjsut to match your directory
source ../pyscreenshot/venv/Scripts/activate	# adjsut to match your directory
python -m main

# TODO:
## WEB:
  - no last dice unsel on color change (?)
  - show total duration / show last date modif date
  - save in cookie
  - start/stop python (doable?)
  - proportionnal bars on the left

## PYTHON:
  - Desired usage: python -m livecapture pos_x pos_y delay
  - or -m livecapture -mode=catan
  - or list windows and choose one
  - to avoid useless captures, scan for top dice black border inner position
  - check for special color dice positions too!
  - take into account if same dice but different background (miss-click case)
