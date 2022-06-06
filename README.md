# About <a href="https://www.python.org/"><img align="right" src="https://img.shields.io/badge/Python-3-F7DF1E?logo=Python" alt="Python3" /></a>

This is a tool that dumps info about games, such as what engines/libraries/frameworks they use.

vd supports quite a few game engines. However, it focuses on [visual novel engines](https://en.wikipedia.org/wiki/List_of_visual_novel_engines).
The name itself reflects this (vd -> Visual novel Dump).

The tool uses heuristics (strategies) to determine which game engine is being used. It's accurate in most cases,
but it can detect the wrong engine in special circumstances. If you observe such behavior, please open an issue.

It's worth noting that, while the tool itself is cross-platform, some engine detection strategies
only work with Windows games. That is, they look for EXE and DLL files. However, the detection itself
works on other platforms, and doesn't rely on Windows specific code (such as Win32 API calls). Therefore, you can run this tool on Windows/Linux/whatever
and use it on games built for Windows.

# Usage

As simple as it gets.

```sh
python vd <path_to_game_dir>
```

Note that vd takes the path to the game *dir*, not to the game executable.

Example:

```sh
python vd stuff/Game

# You can also pass multiple games at a time
python vd stuff/Game /another/game ...
```

# Supported engines

vd can detect these engines:

- [Unity](https://unity.com/)
- [Ren'Py](https://www.renpy.org/)
- [KiriKiri](https://en.wikipedia.org/wiki/List_of_visual_novel_engines#KiriKiri) (KiriKiri/KAG, KiriKiri2/KAG3, KiriKiriZ/KAG3)
- [RealLive](http://www.rlvm.net/) (+ Siglus): originally used by [Key](https://en.wikipedia.org/wiki/Key_(company))
- [GameMaker](https://gamemaker.io/)
- [NScripter](https://en.wikipedia.org/wiki/List_of_visual_novel_engines#NScripter) (+ [ONScripter](http://nscripter.insani.org/) and [Ponscripter](https://kaisernet.fka.cx/onscripter/#ponscripter))
- [BGI/Ethornell](https://github.com/arcusmaximus/EthornellTools) - used in some VNs
- [Monogame](https://www.monogame.net/) (+ [Microsoft XNA](https://en.wikipedia.org/wiki/Microsoft_XNA))
- [Unreal](https://www.unrealengine.com/)
- [OpenFL](https://www.openfl.org/)
- [GlyphX](https://grey-goo.fandom.com/wiki/GlyphX_engine): used by [Petroglyph Games](https://petroglyphgames.com/)

> Some engines don't have official websites (like RealLive and Ethornell); in those cases, relevant articles or projects regarding those engines are linked instead.
>
> The author does not endorse those projects in any way, and they are linked only to serve as a starting point for information regarding the engines.

# Supported libraries/frameworks

vd can also detect if games use any the following:

- [SDL](https://www.libsdl.org) (versions 1 and 2)
- [ANTLR](https://www.antlr.org/) (.Net runtime, versions 3 and 4)
- [curl](https://curl.se/)
- [Lua](https://www.lua.org/)
- [Tale](https://github.com/deprimus/Tale)
- [Naninovel](https://naninovel.com/)

# Disclaimer

This tool only detects engines via heuristics and does not reverse engineer the original game code in any way.
The heuristics used by the tool can be very well performed by humans (*e.g. Does a file named X.dll exist? If so, it's that particular engine*, etc).

Do not use this tool on games which forbid you from using it. The author cannot be held responsible for your actions.

# License <a href="https://github.com/UnexomWid/vd/blob/master/LICENSE"><img align="right" src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT" /></a>

This project is licensed under the [MIT license](https://github.com/UnexomWid/vd/blob/master/LICENSE).

# References

Resources that inspired some detection strategies:

- [UABE](https://github.com/SeriousCache/UABE) - Unity version detection
- [this thread about Ren'Py](https://lemmasoft.renai.us/forums/viewtopic.php?t=50438) - Ren'Py version detection