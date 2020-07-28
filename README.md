![i18n](https://github.com/M-y/auto-brightness/workflows/i18n/badge.svg)
![unittest](https://github.com/M-y/auto-brightness/workflows/unittest/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=M-y_auto-brightness&metric=alert_status)](https://sonarcloud.io/dashboard?id=M-y_auto-brightness)
![release](https://github.com/M-y/auto-brightness/workflows/release/badge.svg)

Auto change screen brightness using webcam on pc's that don't have ambient light sensor.

# Installation

Head on to the [latest release](https://github.com/M-y/auto-brightness/releases/latest) and download an asset of your choice.

## deb
Type `dpkg -i autobrightness*.deb`

## windows
Unzip and put autobrightness.exe file to somewhere of your choice.

## macos 
   unzip

## standalone
You have a unix executable in zip file.

## source
Unzip the file and goto directory where setup.py is. Type `pip install .`

> Note that also you have to add executable to your window manager startup.

# Usage
 
 Type `autobrightness` to run. The tray icon will appear and you will see settings window.

 ![settings window](https://ben.muhammed.im/image/autobrightness.png)

## Command line arguments
```
usage: autobrightness [-h] [-v] [--start | --set] [--config CONFIG]

Auto change screen brightness using webcam.

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  --start          Start the daemon
  --set            Set brightness and exit
  --config CONFIG  Use alternative config file instead of .autobrightness in
                   home directory.
```

## Settings explanation
### Language
Application language.

### Backend
Technology to reach screen brightness.
* __sysfs__: Default backend for *nix systems. You have to select correct interface.
* __powercfg__: Default backend for Windows. You have to select GUID of Display Brightness.

### Gain
Adds the value you selected from here to calculated brightness. For example; if you select 5%, brightness of your screen will be 5% more.

### Camera
Camera number or path. If you have 1 camera only, just type 0.

### Interval
If you select 30 seconds from here, your screen brightness will be adjusted every 30 seconds.

### Shortcut
Keycode(ex: 123), key name(ex: f12) or key combination(ex: ctrl+f12).

### Max brightness on full screen
Sets brightness to maximum value when a full screen application(video, game...) on the screen.

### Set brightness on startup
Calculate and set brightness one time on application startup.
