import cx_Freeze

executables = [cx_Freeze.Executable("snakes.py")]

cx_Freeze.setup(
    name = "Slither",
    options = {"build_exe":{"packages":["pygame"],
                            "include_files":["apple3.png",
                                             "PAC-FONT.ttf",
                                             "SnakeHead.png",
                                             "snakeicon.jpg",
                                             "intro-sound.ogg",
                                             "eat-sound.wav",
                                             "gameover-sound.ogg",
                                             "BGM.ogg"]}},
    description = "Slither Game",
    executables = executables
)