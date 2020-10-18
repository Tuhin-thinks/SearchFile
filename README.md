# SearchFile
Search files from folder faster than any on Windows built-in explorer search.

## Use

### Run using the Following command:
**[For windows]**

`python call_file_finder.py`

**[For Linux]**

`python3 call_file_finder.py`

### Run-time instructions

- It basically searches for a substring in inside a string using the built in Python `in` functionality. So, the text your type inside file name will be the required substring.

- The code uses multiprocessing`(multiprocessing.Process)` and threading (using `QThread`), so it's performance is expected to be super fast for all type of PC's. High-end or Low-end.
- Trying to make user friendly by, adding a button at opens up to the current folder of the exe (From there you can navigate to the folder you want to search),
  - You can launch a search process by hitting **Enter-Key(Return)** on the filename `lineEdit`

## Requirements

- PyQt5

## Python version

`Python >= 3.7`

_Ideally the app window should look like as below:_

<p align="center">
  <image src="https://github.com/Tuhin-thinks/SearchFile/blob/main/image/ksnip_20201018-195641.png" width="500px" height="auto">
</p>
