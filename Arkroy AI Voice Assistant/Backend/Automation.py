from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g","qv3Wpe", "kno-rdesc","SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a Developer and you likes to code and develope software, I'm a very accurate and advanced AI chatbot named {os.environ['Assistantname']} which also has real-time up-to-date information from the internet."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(file_path):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, file_path])

    def ContectWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=False
        )

        Answer = completion.choices[0].message.content  
        messages.append({"role": "system", "content": Answer})
        return Answer

    Topic = Topic.replace("Content", "").strip()
    ContentByAI = ContectWriterAI(Topic)

    file_path = rf"Data\{Topic.lower().replace(' ', '')}.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    print(f"Content saved in {file_path}")  

    # 🔥 Yeh line add ki hai notepad kholne ke liye
    OpenNotepad(file_path)

    return True



def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYouTube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.Session()):
    try:
        print(f"Opening {app}...")
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except:
        print(f"{app} not found on system, searching online...")

        search_url = f"https://www.google.com/search?q={app}+site+official"
        headers = {'User-Agent': useragent}

        try:
            response = sess.get(search_url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find all 'a' tags that contain links
                links = soup.find_all('a', href=True)

                for link in links:
                    href = link['href']
                    
                    if "/url?q=" in href:
                        actual_url = unquote(href.split("/url?q=")[1].split("&")[0])  # Decode URL

                        if actual_url.startswith("http"):
                            print(f"Opening {actual_url} 🚀")
                            webbrowser.open(actual_url)
                            return True

                print("No valid links found, opening Google search page...")
                webbrowser.open(search_url)

            else:
                print("Google search request failed, opening search page...")
                webbrowser.open(search_url)

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}, opening Google search page...")
            webbrowser.open(search_url)

        return True

def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closet = True, output = True, throw_error = True)
            return True

        except:
            return False

def System(command):

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        command = command.lower()  # ✅ Convert command to lowercase

        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        
        else:
            print(f"No Function Found For: {command}")  # ✅ Better Debugging

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        print(result)

if __name__ == "__main__":
    asyncio.run(Automation(["Open Facebook", "Open Instagram", "Play Venom Song", "Content song for me"]))