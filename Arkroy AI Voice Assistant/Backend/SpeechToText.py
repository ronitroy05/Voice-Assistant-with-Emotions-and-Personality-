from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

env_vars = dotenv_values(".env")

InputLanguage = env_vars.get("InputLanguage")

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()

Link = f"{current_dir}/Data/Voice.html"

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

TempDirPath = rf"{current_dir}/Frontend/Files"

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', 'w', encoding='utf-8') as file:
        file.write(Status)


def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whom", "whose", "is", "are", "am", "was", "were", "will", "shall", "should", "would", "could", "can", "may", "might", "do", "does", "did", "have", "has", "had", "having", "been", "being", "an", "a", "the", "this", "that", "these", "those", "my", "mine", "your", "yours", "his", "her", "hers", "its", "our", "ours", "their", "theirs", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "myself", "yourself", "himself", "herself", "itself", "ourselves", "yourselves", "themselves", "what's", "who's", "where's", "when's", "why's", "which's", "whom's", "whose's", "isn't", "aren't", "amn't", "wasn't", "weren't", "won't", "shan't", "shouldn't", "wouldn't", "couldn't", "can't", "mayn't", "mightn't", "don't", "doesn't", "didn't", "haven't", "hasn't", "hadn't", "havingn't", "been't", "beingn't", "an't", "a't", "the't", "this't", "that't", "these't", "those't", "my't", "mine't", "your't", "yours't", "his't", "her't", "hers't", "its't", "our't", "ours't", "their't", "theirs't", "i't", "you't", "he't", "she't", "it't", "we't", "they't", "me't", "him't", "her't", "us't", "them't", "myself't", "yourself't", "himself't", "herself't", "itself't", "ourselves't","can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():

    driver.get("file:///" + Link)

    driver.find_element(by = By.ID, value = "start").click()

    while True:
        try:

            Text = driver.find_element(by = By.ID, value = "output").text

            if Text:

                driver.find_element(by = By.ID, value = "end").click()

                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(Text))
                
        except Exception as e:
            pass

if __name__ == "__main__":
    while True:

        Text = SpeechRecognition()
        print(Text)