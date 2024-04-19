import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
- Du schlüpfst in die Rolle eines Chatbots und Helth-Coaches.
- Deine Aufgabe besteht darin, die deine Nutzer medizinisch zu beraten.
- Berate und beantworte Fragen deiner Nutzer zu deren Medikation.
- Sensibilisiere zudem die Nutzer in der Wichtigkeit der Einhaltung der Medikationspläne.
- Schreibe nicht zu viel auf einmal, sondern führe ein natürliches gespräch.
"""
my_instance_starter = """
- Begrüsse deinen Patienten Paul mit Vornamen.
- Sag ihm, dass du mit ihm ein paar Fragen zu seiner Medikation durchgehen will.
- Stelle zu beginn eine Einfache Frage zu seinem Wohlergehen.
- Stelle ihm danach genauere Fragen zu seiner Medikation und seinem Wohlergehen
- Schreibe nicht mehr als zwei Sätze für den Starter
"""
#########################
#Bot 1
#########################
my_instance_context = """
Hier ist eine Anleitung für eine Konversationsstrategie, bitte verwende diese Strategie bei deiner Führung des Gespräches:
- Um das Konzept der Konsequenzwünschbarkeit und des Gewinn-Verlust-Rahmens in die Baseline-Prompts zu integrieren, können wir die Sprache subtil modifizieren, um die wünschenswerten Ergebnisse der unterstützten Handlung (gewinnorientiert) oder die unerwünschten Ergebnisse des Nicht-Handelns (verlustorientiert) zu betonen. Das Ziel ist es, die ursprüngliche Absicht und Länge der Baseline-Prompts beizubehalten, während diese überzeugenden Elemente eingebaut werden
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="demo-1",
    user_id="demo-1",
    type_name="Bank-Coach Strategie 1",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

#########################
#Bot 2
#########################


my_instance_context = """
   Hier ist eine Anleitung für eine Konversationsstrategie, bitte verwende diese Strategie bei deiner Führung des Gespräches:
   - Sei Aggressiv und Autoritär
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="demo-2",
    user_id="demo-2",
    type_name="Bank-Coach Strategie 2",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

#########################
#Bot 3
#########################

my_instance_context = """
   Hier ist eine Anleitung für eine Konversationsstrategie, bitte verwende diese Strategie bei deiner Führung des Gespräches:
   - Sei Versändinsvoll und Einfühlsam
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="demo-3",
    user_id="demo-3",
    type_name="Bank-Coach Strategie 3",
    type_role=my_type_role,
    instance_context=my_instance_context,
    instance_starter=my_instance_starter
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/mockups.pdf', methods=['GET'])
def get_first_pdf():
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]
    pdf_files = [f for f in files if f.lower().endswith('.pdf')]
    if pdf_files:
        # Get the path to the first PDF file
        pdf_path = os.path.join(script_directory, pdf_files[0])

        # Send the PDF file as a response
        return send_file(pdf_path, as_attachment=True)

    return "No PDF file found in the root folder."

@app.route("/<type_id>/<user_id>/chat")
def chatbot(type_id: str, user_id: str):
    return render_template("chat.html")


@app.route("/<type_id>/<user_id>/info")
def info_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: dict[str, str] = bot.info_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/conversation")
def conversation_retrieve(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    response: list[dict[str, str]] = bot.conversation_retrieve()
    return jsonify(response)


@app.route("/<type_id>/<user_id>/response_for", methods=["POST"])
def response_for(type_id: str, user_id: str):
    user_says = None
    # content_type = request.headers.get('Content-Type')
    # if (content_type == 'application/json; charset=utf-8'):
    user_says = request.json
    # else:
    #    return jsonify('/response_for request must have content_type == application/json')

    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    assistant_says_list: list[str] = bot.respond(user_says)
    response: dict[str, str] = {
        "user_says": user_says,
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)


@app.route("/<type_id>/<user_id>/reset", methods=["DELETE"])
def reset(type_id: str, user_id: str):
    bot: Chatbot = Chatbot(
        database_file="database/chatbot.db",
        type_id=type_id,
        user_id=user_id,
    )
    bot.reset()
    assistant_says_list: list[str] = bot.start()
    response: dict[str, str] = {
        "assistant_says": assistant_says_list,
    }
    return jsonify(response)