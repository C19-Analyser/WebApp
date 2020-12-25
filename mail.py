from app import mail,app

from flask_mail import Message

import magic

defaultUser = {'nom': 'NOM','prenom': 'PRENOM','mail': 'MAIL'}

def sendAlert(subject,user=defaultUser,filename="FILENAME",result="RESULT",modelType="MODEL TYPE"):
    
    msg = Message('Alert C19 web App', sender = 'c19.analyser@gmail.com', recipients = ['hugo.guillaume44@gmail.com'])
    

    if subject == 'inscription' :
        msg.body = "Un nouvel utilisateur s'est inscrit.\nNom :" + user['nom'] + "\nPrénom :" + user['prenom'] + "\nMail :" + user['mail']
        mail.send(msg)
        print('Mail sending')
    elif subject == 'prediction':
        msg.body = "L'utilisateur " + user['nom'] + " " + user['prenom'] + " a soumis le fichier " + filename + ".\nRésultat : "  + result + ".\nModel utilisé :" + modelType + "."
        with app.open_resource("uploads/" + filename) as fp:  
            msg.attach("uploads/" + filename,magic.from_file('uploads/COVID19460.jpg', mime=True),fp.read())  
        mail.send(msg)
        print('Mail sending')
    elif subject == 'rapport':
        pass
    else:
        print('Error invalid parameter in mail.py')