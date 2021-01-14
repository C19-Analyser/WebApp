from app import mail, app

from flask_mail import Message

from flask import copy_current_request_context

import magic
import threading

defaultUser = {'nom': 'NOM', 'prenom': 'PRENOM', 'mail': 'MAIL'}


def create_message(subject, user=defaultUser, filename="FILENAME", result="RESULT", modelType="MODEL TYPE"):

    msg = Message('Alert C19 web App', sender='c19.analyser@gmail.com',
                  recipients=['hugo.guillaume44@gmail.com'])

    if subject == 'inscription':
        msg.body = "Un nouvel utilisateur s'est inscrit.\nNom :" + \
            user['nom'] + "\nPrénom :" + \
            user['prenom'] + "\nMail :" + user['mail']
        print('Mail create')
        return msg
    elif subject == 'prediction':
        msg.body = "L'utilisateur " + user['nom'] + " " + user['prenom'] + " a soumis le fichier " + \
            filename + ".\nRésultat : " + result + ".\nModel utilisé :" + modelType + "."
        with app.open_resource("uploads/" + filename) as fp:
            msg.attach("uploads/" + filename,
                       magic.from_file('uploads/' + filename, mime=True), fp.read())
        print('Mail create')
        return msg
    elif subject == 'rapport':
        pass
    else:
        print('Error invalid parameter in mail.py')


def send_async(subject, user=defaultUser, filename="FILENAME", result="RESULT", modelType="MODEL TYPE"):

    message = create_message(subject, user=user, filename=filename)

    @copy_current_request_context
    def send_message(message):
        mail.send(message)
        print("MAIL")

    sender = threading.Thread(
        name='mail_sender', target=send_message, args=(message,))
    sender.start()
