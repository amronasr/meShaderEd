#
# ui_settings.py
#
import sys

CHECK_WIDTH = 20
if ( sys.platform == 'darwin' ) : 
  CHECK_WIDTH = 25
BROWSE_WIDTH = 24
LABEL_WIDTH = 140
NODE_LABEL_WIDTH = 80
EDIT_WIDTH = 160
FIELD_WIDTH = 50
COLOR_WIDTH = 60

SPACING = 4
HEIGHT = 20

COMBO_WIDTH = 120
COMBO_HEIGHT = HEIGHT
if ( sys.platform == 'darwin' ) : 
  COMBO_HEIGHT = 24
MAX = 16777215
LT_SPACE = CHECK_WIDTH
