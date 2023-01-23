import pyautogui, time, os, subprocess, cv2, pyperclip, pytesseract

# using th clipper app on android (it must be opened)
# adb shell am broadcast -a clipper.get 
# adb shell am broadcast -a clipper.set -e text 'mytext'
# start the clipper app : 

def open_wireless_adb():
    ip_adress = str(input("what is the Ip adress or your android device ?"))
    print("connection")

    result = subprocess.run(['adb', 'connect', ip_adress+':5555'])

    if not result.returncode == 0:
        print("Command failed with error code: ", result.returncode)
        exit()

    print("entering adb shell, type 'exit' to exit")

def open_and_get_clipboard():
    # open the app in background
    result = subprocess.run(["adb", "shell", "am", "startservice", "ca.zgrs.clipper/.ClipboardService"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # open the app in the foreground
    result = subprocess.run(["adb", "shell", "monkey", "-p", "ca.zgrs.clipper", "-c", "android.intent.category.LAUNCHER", "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(result.stdout)
    # get the clipboard
    result = subprocess.run(["adb", "shell", "am", "broadcast", "-a", "clipper.get"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(result.stdout)
    output_list = result.stdout.split(b'data=')
    link = output_list[1].strip()
    linkk = str(link)
    linkk = linkk[1:]
    linkk = linkk.replace('\"', '').replace('\'', '')
    return linkk



def open_spotify():
    result = subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LAUNCHER", "-n", "com.spotify.music/.MainActivity"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if(result.stderr.decode() == ""):
        print("spotify opened successfully")
    else:
        print(result.stderr.decode())

def click_on_actual_playing_song():
    subprocess.run(["adb", "shell", "input", "tap", '140', '2150'])

def click_next_song():
    subprocess.run(["adb", "shell", "input", "tap", '480', '1880'])


def enter_likedSongs():
    subprocess.run(["adb", "shell", "input", "tap", '530', '2325'])
    time.sleep(.5)
    subprocess.run(["adb", "shell", "input", "tap", '530', '440'])
    time.sleep(1)
    subprocess.run(["adb", "shell", "input", "text", "Liked"])
    subprocess.run(["adb", "shell", "input", "keyevent", "62"]) # Space key
    subprocess.run(["adb", "shell", "input", "text", "songs"])
    time.sleep(.2)
    subprocess.run(["adb", "shell", "input", "tap", '500', '550'])

def swipe_one_music():
    subprocess.run(["adb", "shell", "input", "swipe", "500", "1187", "500", "1000", "500"])

def press_upper_music():
    subprocess.run(["adb", "shell", "input", "swipe", "460", "340", "460", "340", "1000"])

def click_share_button():
    subprocess.run(["adb", "shell", "input", "tap", "260", "2220"])

def click_copy_link():
    subprocess.run(["adb", "shell", "input", "tap", "180", "2270"])

## before launching this function, be sure to be inside the spotify loop with random play OFF
def save_from_playWindow(nb_titles):
    with open("downloaded_titles.txt", "w") as dt:
        for i in range(nb_titles):
            # click_right_share_button
            subprocess.run(["adb", "shell", "input", "tap", "980", "1750"])
            time.sleep(3)# wait for share screen to appear
            #click on copylink button
            subprocess.run(["adb", "shell", "input", "tap", "180", "2270"])
            # get the copied text
            time.sleep(.5)
            dt.write(open_and_get_clipboard())
            dt.write("\n")
            time.sleep(.5)
            #re-open spotify
            open_spotify()
            time.sleep(.5)
            click_on_actual_playing_song()
            time.sleep(.2)
            click_next_song()


save_from_playWindow(3)

#click_on_actual_playing_song()
#time.sleep(.2)
#click_next_song()
