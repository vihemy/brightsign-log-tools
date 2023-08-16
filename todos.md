1. Try-Exceptions blocks in the different pieces of code for easier bugfinding.
2. Make executable that can self-run from KC-computer (pyinstaller? - maybe with simple user-interface?)
    - Send mail or make other form of contact to me, when errors occure, script doesn't suceed
3. Setup device .118 to make logs.
4. Change all absolute paths to relative paths, so folder kan be moved around
5. Make so exports to have date in name, 
6. CONFIG OR EXCEL TO STORE SEARCHWORDS IN?

7. Make a universal analyze method for the player-class, that takes search words as arguments.
    - Either in form of a list, or a searchwords-class, if there is need of multipel search-word functionalities.
    - Load the searchwords from brightsign-index-file. Create new column for this data.

8. Test log_downloader when on KC network

9. Contemplate whether to use one config/player-idex file for all data or split up in a seperate player-database and config-file.

10. Rewrite log_downloader to use requests or urllib to download logs directly to appropriate folder. This makes logmove obsolete.

11. Remove https in requests.get to speed up download?