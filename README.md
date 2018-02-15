# winhop
End of Alt Tab: Cursor based window switcher for Windows.

![winhop_demo](https://user-images.githubusercontent.com/23325839/36252776-11c264ba-1289-11e8-8465-539f7018864e.gif)

<!-- toc -->
- [winhop](#winhop)
  - [Overview](#overview)
  - [How to use](#how-to-use)
  - [Usage](#usage)
  - [Usecase](#usecase)
    - [Window Filtering](#window-filtering)
    - [practical AHK setting](#practical-ahk-setting)
  - [Development](#development)
    - [Requirement](#requirement)
    - [How to build](#how-to-build)
    - [How to debug](#how-to-debug)
  - [License](#license)
  - [Author](#author)

## Overview
With winhop, you can switch to the next right window by pressing, for example, `Win + Right`.

## How to use
- Install the hotkey software. (Bacause **winhop is a NON-RESIDENT tool yet.**)
  - e.g. [AutoHotkey](https://autohotkey.com/)
- Place `winhop.exe` to your directory and memo the path.
- Write the hotkey setting.
  - e.g. See below
- Press the hotkey.

```ahk
; Assign Win + Right to 'Switching to the next right window'.
#Right::
  run, D:\bin\winhop.exe --right --warp
Return
```

## Usage

```
$ python winhop.py -h
usage: winhop.py [-h] [-w] [-a AREA] [-t [TITLE [TITLE ...]]]
                 [-c [CLASSNAME [CLASSNAME ...]]] [--no-empty-caption]
                 [--no-desktop] [--left] [--right] [--up] [--down]
                 [--debug-print]

End of Altab -- Cursor based window switcher.

optional arguments:
  -h, --help            show this help message and exit
  -w, --warp            Use edge warp. (default: False)
  -a AREA, --area AREA  Use window target exclusion with the lower
                        area(height*width) limit. (default: 10000)
  -t [TITLE [TITLE ...]], --title [TITLE [TITLE ...]]
                        Use window target exclusion with partial match of
                        Caption. (default: [])
  -c [CLASSNAME [CLASSNAME ...]], --classname [CLASSNAME [CLASSNAME ...]]
                        Use window target exclusion with partial match of
                        Classname. (default: [])
  --no-empty-caption    Disable window target exclusion with empty caption
                        name. (default: False)
  --no-desktop          Disable exclusion of desktop as a window target.
                        (default: False)
  --left                Switch to the left window and exit. (default: False)
  --right               Switch to the right window and exit. (default: False)
  --up                  Switch to the up window and exit. (default: False)
  --down                Switch to the down window and exit. (default: False)
  --debug-print         [DEBUG] Print window information. Only works from .PY,
                        **not .EXE** (default: False)
```

About `winhop.exe`, you cannot use below options.

- `--h`
- `--debug-print`

## Usecase

### Window Filtering
Exclude web browser windows with caption matching.

- `winhop.exe -t "mozilla firefox" "internet explorer" "google chrome"`

Exclude cmd windows and explorer windows with class name matching.

- `winhop.exe -c "ConsoleWindowClass" "CabinetWClass"`

Exclude small windows with area filter(under `500x500` windows).

- `winhop.exe -a 250000`

### practical AHK setting
`Win + Cursor` based switching.

My AHK setting on Windows10, like this:

```ahk
winhop_vars(){
  global winhop_bin
  global winhop_prm
  winhop_bin = D:\bin\winhop\winhop.exe
  winhop_prm = --warp --area 250000 -c "Windows.UI" -t "visual c++ runtime lib"
}
#Left::
  winhop_vars()
  run, %winhop_bin% %winhop_prm% --left
Return
#Right::
  winhop_vars()
  run, %winhop_bin% %winhop_prm% --right
Return
#Up::
  winhop_vars()
  run, %winhop_bin% %winhop_prm% --up
Return
#Down::
  winhop_vars()
  run, %winhop_bin% %winhop_prm% --down
Return
```

## Development

### Requirement
- Windows 7+
- Python 3.6+
- Python Libraries
  - See [requirements.txt](requirements.txt)

### How to build
Execute [build.bat](build.bat) from the command prompt or double click in the explorer.

The cx_Freeze build script is [build.py](build.py).

### How to debug
Execute `python winhop.py --debug_print`.

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
