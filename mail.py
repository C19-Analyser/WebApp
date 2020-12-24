from app import mail

from flask_mail import Message

def sendAlert(subject,user="USER",filename="FILENAME",result="RESULT",modelType="MODEL TYPE"):
    
    msg = Message('Alert C19 web App', sender = 'c19.analyser@gmail.com', recipients = ['hugo.guillaume44@gmail.com'])
    
    print('here')

    if subject == 'connexion' :
        msg.body = "Un nouvel utilisateur s'est connecté."
        mail.send(msg)
    elif subject == 'prediction':
        print('Here')
        msg.body = "L'utilisateur " + user + " a soumis le fichier " + filename + ".\nRésultat : "  + result + ".\nModel utilisé :" + modelType + "."
        mail.send(msg)
        print('HERE')
    else:
        print('Error invalid parameter in mail.py')