#!/bin/sh
path=$(find ~/Library/Developer/Xcode/DerivedData/"$3"-*/Build/Products/Debug-iphonesimulator -name "$4" | head -n 1)
echo "${path}"
echo "$1"
echo "$2"
xcrun simctl boot "$1" # Boot the simulator with identifier hold by argument var
xcrun simctl install "$1" "$path" # Install the .app file located at location hold by $path var at booted simulator with identifier hold by argument var
xcrun simctl launch "$1" "$2" # Launch .app using its bundle at simulator with identifier hold by $argument var