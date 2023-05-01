Poker Ripper :
Poker Ripper est une application de bureau écrite en Python qui aide les joueurs de poker à évaluer la force de leurs mains et à décider s'ils doivent jouer, miser ou passer. L'application utilise une interface graphique basée sur Tkinter et évalue la force des mains en utilisant la bibliothèque Treys.

Fonctionnalités:
- Évalue la force de la main de départ.
- Calcule la force de la main en fonction des cartes sur la table.
- Simule des milliers de mains pour estimer le taux de victoires.
- Fournit des conseils sur la façon de jouer la main en fonction de la force et du taux de victoires.

Prérequis:
- Python 3.10
- Tkinter (inclus dans Python standard)
- Treys

Installation :
- Assurez-vous d'avoir Docker installé sur votre système.
- Naviguez jusqu'au répertoire du projet :
- cd poker-ripper
- docker build -t poker-ripper .
- installer x11-xserver-utils
- xhost +local:docker
- docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  poker-ripper

L'application Poker Ripper devrait maintenant être en cours d'exécution dans un conteneur Docker. L'interface utilisateur de l'application s'affiche et vous pouvez commencer à l'utiliser.
