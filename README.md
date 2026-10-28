# PROJET: Faire un projet de générateur de mots de passe en PYSide6

Le projet se divise en deux parties dont la première est de concevoir un moteur de générateur de mots de passe fonctionnel et testable en ligne de commande et la deuxième est de trasnformer la logique de l aprtie 1 en une application complète avec une interface utilisateur(UI) ergonomique.

## Partie1: 
Dans cette première remise, la partie est la plus essentielle:

- Il faut d'abord construire l'interface de base de l'application pour pouvoir mieux se répérer.
- Il faut créer la class **PasswordGenerator** qui supporte la définition de la longueur du mot de passe, la sélection  des types de caractèresm( miniscules,majuscules, chiffres, symboles) et l'option de validation: activée si le mot de passe contient au moins un caractère de chaque type sélectionné. 

## Partie2:
## Utilisation
Ajouter : saisir un e-mail et un mot de passe ou ouvrir Generer,
puis choisir Utiliser et Enregistrer. Modifier et Supprimer agissent
sur leur propre ligne, meme apres tri. Double-clic ou clic droit sur la
ligne pour reveler pendant cinq secondes. Les donnees sont chargees au
demarrage et les changements sauvegardes a la fermeture normale.
Sans modification, le fichier n est pas reecrit. Une fermeture brutale
peut perdre les changements non encore sauvegardes.
Si le JSON est corrompu, un message est affiche et aucune ecriture n est
autorisee pendant cette session : corriger le fichier ou changer de chemin.
Si la sauvegarde echoue, la fenetre reste ouverte.
Les dossiers parents d un chemin personnalise doivent deja exister.
L adresse e-mail est obligatoire mais sa validite/rejoignabilite n est pas verifiee.

