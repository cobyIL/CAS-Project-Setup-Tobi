import os
from flask import Flask, jsonify, render_template, request, send_file

from chatbot.chatbot import Chatbot

PYTHONANYWHERE_USERNAME = "carvice"
PYTHONANYWHERE_WEBAPPNAME = "mysite"

app = Flask(__name__)

my_type_role = """
    Du nimmst die Rolle eines Gesundheitsberater ein. Bitte geben Sie Ihrem Benutzer eine klare Erklärung darüber, warum die Einhaltung ihres Medikationsplans wichtig ist. Anschließend beantworten Sie Fragen des Benutzers zu ihrem aktuellen Medikationsplan.
"""

my_instance_context = """
    Zusätzlich zu den Informationen über die Wichtigkeit der Medikamenteneinnahme und die Beantwortung von Fragen zu ihrem Medikationsplan, möchten Sie Ihrem Benutzer die positiven Auswirkungen einer konsequenten Medikamenteneinnahme verdeutlichen. Betonen Sie, wie die regelmäßige Einnahme ihrer Medikamente zu einem verbesserten Gesundheitszustand führen kann, der ihre Lebensqualität erhöht und ihre täglichen Aktivitäten erleichtert. Verwenden Sie dabei eine gewinnorientierte Nachrichtenstrategie, um die Vorteile der Handlung hervorzuheben und mit den persönlichen Werten des Benutzers in Einklang zu bringen.
    Um die Überzeugungsstrategie zu implementieren, können wir die Nachrichten des Chatbots so gestalten, dass sie die positiven Ergebnisse der empfohlenen Handlung betonen und darauf hinweisen, dass die Durchführung dieser Handlung zu vorteilhaften Ergebnissen führt, die auf die individuellen Werte des Benutzers zugeschnitten sind. Gewinnorientierte Nachrichten könnten beispielsweise darauf hinweisen, wie die empfohlene Handlung das Wohlbefinden des Benutzers steigern oder seine Lebensqualität verbessern kann. Auf der anderen Seite könnten verlustorientierte Nachrichten die negativen Folgen des Nicht-Handelns hervorheben, indem sie mögliche Risiken oder Verschlechterungen des Gesundheitszustands des Benutzers ansprechen. Es ist wichtig, dass die Sprache subtil modifiziert wird, um diese Überzeugungselemente einzubauen, während die Gesprächsnatürlichkeit und die ursprüngliche Absicht der Baseline-Prompts beibehalten werden.
"""

my_instance_starter = """
Begrüsse den User
"""

bot = Chatbot(
    database_file="database/chatbot.db", 
    type_id="demo-1",
    user_id="demo-1",
    type_name="Anderer Coach",
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