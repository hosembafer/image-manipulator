sh clean.sh

# pyinstaller --onefile image_manipulator.py --noconsole --target-arch universal2
if [ "$1" == "win" ]; then
    pyinstaller -n "Image Manipulator" --clean --onefile --noconsole image_manipulator.py
else
    pyinstaller -n "Image Manipulator" --clean --onefile --noconsole image_manipulator.py
fi
