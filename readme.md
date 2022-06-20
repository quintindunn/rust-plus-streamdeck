## Download/Install:
1. Install [python3.10+](https://www.python.org/downloads/)
### **Execute the following in command prompt**
3. Install pyinstaller `py -m pip install pyinstaller` (or) `python -m pip install pyinstaller`
4. Install rustplus `py -m pip install rustplus` (or) `python -m pip install rustplus`
5. Install websocket-client `py -m pip install websocket-client` (or) `python -m pip install websocket-client`
6. Install rel `py -m pip install rel` (or) `python -m pip rel`

3. Download and install:
   * Manual:
     1. Make a folder named `com.t1ps.rustplus.sdPlugin` in your Elgato Streamdeck plugins folder, (usually located at `%appdata%\Elgato\StreamDeck\Plugins`)
     2. Download [main.py](https://raw.githubusercontent.com/quintindunn/rust-plus-streamdeck/main/main.py) and put it in the folder.
     3. Download [images.py](https://github.com/quintindunn/rust-plus-streamdeck/blob/main/images.py) and put it in the folder.
     4. Download [manifest.json](https://github.com/quintindunn/rust-plus-streamdeck/blob/main/manifest.json) and put it in the folder.
     5. Open command prompt and `cd` to the `com.t1ps.rustplus.sdPlugin` directory.
     6. Run the command `py -m pyinstaller --onefile main.py` (or) `python -m pyinstaller --onefile main.py`
     7. Move the `main.exe` file from the `dist` folder to the root folder (`com.t1ps.rustplus.sdPlugin`)
     8. Delete the `dist` and `build` folders.
   * Automatic **Only works for StreamDeck installs at default location**:
     1. Run: `mkdir %appdata%\Elgato\StreamDeck\Plugins\com.t1ps.rustplus.sdPlugin && cd %appdata%\Elgato\StreamDeck\Plugins\com.t1ps.rustplus.sdPlugin && mkdir PI && curl https://raw.githubusercontent.com/quintindunn/rust-plus-streamdeck/main/main.py >> main.py && curl https://raw.githubusercontent.com/quintindunn/rust-plus-streamdeck/main/images.py >> images.py && curl https://raw.githubusercontent.com/quintindunn/rust-plus-streamdeck/main/manifest.json >> manifest.json && pyinstaller --onefile main.py && move %appdata%\Elgato\StreamDeck\Plugins\com.t1ps.rustplus.sdPlugin\dist\main.exe %appdata%\Elgato\StreamDeck\Plugins\com.t1ps.rustplus.sdPlugin\main.exe && rd /s /q dist && rd /s /q build && cd PI && curl https://raw.githubusercontent.com/quintindunn/rust-plus-streamdeck/main/PI/PI.html >> PI.html && curl https://raw.githubusercontent.com/quintindunn/rust-plus-streamdeck/main/PI/sdpi.css >> sdpi.css`
4. Fully close the `StreamDeck` program using `taskkill /f /im streamdeck.exe`
5. Relaunch the StreamDeck program.

## Setup:
1. Drag the `RustPlusToggle` action from the sidebar onto a slot on the buttons grid.
2. Add the [Rustplus.py Link Companion](https://chrome.google.com/webstore/detail/rustpluspy-link-companion/gojhnmnggbnflhdcpcemeahejhcimnlf?hl=en) extension to Chrome.
3. Open the extension.
4. Click `LOGIN TO RUSTPLUS.PY` button and login.
5. Click on `Listen for notifications`
6. Go to Rust, take out a wiring tool and hold the interact button on a `Smart Switch`, click `pair`
7. Copy the data from the FCM Listener page to the StreamDeck plugin. **Hit `Enter` for each one!**
   * `ip` &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-> `Server IP`
   * `playerToken` -> `Player Token`
   * `playerID` &ensp;&ensp;&ensp;-> `Steam64`
   * `port` &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-> `Port`
   * `entityId` &ensp;&ensp;&ensp;-> `Entity ID`

## Thing to note:
* Only one server is supported at a time, if you've already added the server, on future buttons you only need to put the `entityId`
* This may break in the future, if it breaks you can create an issue on GitHub or message me on discord at `Tips#4933`
* The `main.exe` file may be flagged as a virus depending on the antivirus you have, if you upload it to virustotal you'll see only 2 (as of 6/20/22) will detect it as a virus. This is due to the program being written in Python, an interpreted language but needing binary code. To do this I used the library `pyinstaller` which if you google `pyinstaller identified as virus` you'll see numerous reports of this happening when it's clean. If you still don't trust me you can take a quick look in the `.py` files (the files with the code) and even without much coding knowledge you should be able to tell it's not malicious. 

## Credits:
I wouldn't have attempted, nor been able to create this without the [RustPlus python library](https://pypi.org/project/rustplus/) created by [olijeffers0n](https://github.com/olijeffers0n/rustplus) he's insanely talented and very consistent on keeping his library up to date.
