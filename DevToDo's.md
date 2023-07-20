1. Cut in stead of copy from downloads-folder to src-folders. Downloads-folder gets crammed.? (Risk of loosing files)
2. Try-Exceptions blocks in the different pieces of code for easier bugfinding.
3. Make executable that can self-run from KC-computer (pyinstaller? - maybe with simple user-interface?)
    - Send mail or make other form of contact to me, when errors occure, script doesn't suceed
4. Setup device .118 to make logs.
5. Refactor so that get_player_info_from_file can be called from everywhere.
6. Change all absolute paths to relative paths, so folder kan be moved around
7. get exports to have date in name, 
8. CONFIG OR EXCEL TO STORE SEARCHWORDS IN?

9. Make one universal device-class, that downloads, moves and analyzes data, according to the arguments passed in.
    - Alternatively, make a class for each device, that inherits from a universal device-class.
    - Alternatively make three classes. One for each functionality. 