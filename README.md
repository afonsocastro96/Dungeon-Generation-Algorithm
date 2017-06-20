# Dungeon-Generation-Algorithm
The initial implementation of the Dungeon Generation Algorithm we use in Earthborn. The algorithm generates an entire floor for a procedural-generated dungeon.

## Run

`python dungeon.py FLOOR_HEIGHT FLOOR_WIDTH MIN_SECTOR_SIZE MIN_ROOM_HEIGHT MIN_ROOM_WIDTH STRICTNESS STAIRS_GENERATION_TIMEOUT`

All arguments are optional. The default values are as follows:

* FLOOR_HEIGHT - 40
* FLOOR_WIDTH - 40
* MIN_SECTOR_SIZE - 10
* MIN_ROOM_HEIGHT - 4
* MIN_ROOM_WIDTH - 2
* STRICTNESS - 0.3 (must be a value between 0 and 0.4)
* STAIRS_GENERATION_TIMEOUT - 10000

## Example output

https://pastebin.com/raw/jU9FmA4D

https://pastebin.com/raw/fYSx0hCs
