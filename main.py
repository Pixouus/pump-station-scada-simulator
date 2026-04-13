import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------------
# Variable globale (niveau cuve) pour ma part 2
# -----------------------------
niveau = 50

#   Variable de ma part 3
pompe_active = False

#   Variable de ma part 4
systeme_demarre = False

#   Variable de ma part 6
alarme_clignotante = False
voyant_allume = True
etat_alarme = "normal"

job_cycle = None
job_clignotement = None

#  Variable de ma part 7
dernier_etat_alarme = None

# -----------------------------
# Fonctions de contrôle
# -----------------------------

#def start_pompe():
#    label_etat.config(text="Pompe Ouverte", bg="green")

#def stop_pompe():
#    label_etat.config(text="Pompe fermée", bg="red")


def start_pompe():
    global pompe_active, systeme_demarre
    pompe_active = True
    systeme_demarre = True
    label_etat.config(text="Pompe ouverte", bg="green")
    ajouter_evenement("Pompe ouverte")  # Ajout d'événement à l'historique

def stop_pompe():
    global pompe_active, systeme_demarre
    pompe_active = False
    systeme_demarre = True    # Pour que le système ne commence pas automatiquement sauf si le système de démarrage est bien activé " autrement dit sans clique sur boutton le niveau ne change pas tout seul dans le début !! "
    label_etat.config(text="Pompe fermée", bg="red")
    ajouter_evenement("Pompe fermée")  

# -----------------------------
# Fonctions de ma part 2
# -----------------------------

def remplir():
    global niveau
    if pompe_active:  # Sécuriser remplir ( part 3 )
            return  # Ne rien faire si la pompe est ON

    niveau = niveau + 5
    if niveau > 100:
        niveau = 100

    afficher_niveau()

def vider():
    global niveau
    if not pompe_active:  # Sécuriser vider ( part 3 )
            return  # Ne rien faire si la pompe est OFF


    niveau = niveau - 5
    if niveau < 0:
        niveau = 0

    afficher_niveau()

def afficher_niveau():
    label_niveau.config(text=f"Niveau : {niveau}%")
    verifier_alarme()  # je dois vérifié les alarmes à chaque mise à jour du niveau

    #Barre visuelle de niveau (part 5)
    canvas.delete("all")  # pour que j'efface le contenu précédent du canvas
    largeur_barre = (niveau / 100) * 200  # Calculer la largeur de la barre en fonction du niveau
    
    if niveau >= 100 or niveau <= 0:
        couleur_barre = "red"
    elif niveau >= 80 or niveau <= 20:
        couleur_barre = "orange"
    else:
        couleur_barre = "green"
    
    canvas.create_rectangle(0, 0, largeur_barre, 30, fill=couleur_barre, outline="black")

    historique_niveau.append(niveau)  # Ajouter le niveau actuel à l'historique

    if len(historique_niveau) > 20:  # Limiter l'historique à 20 points pour éviter une surcharge
        historique_niveau.pop(0)  # Supprimer le point le plus ancien

    line.set_data(range(len(historique_niveau)), historique_niveau)
    ax.set_xlim(0, max(20, len(historique_niveau)))  # Ajuster la limite x en fonction de l'historique
    canvas_graph.draw()

# -----------------------------
# Fonctions de ma part 3
# -----------------------------
def mettre_en_attente():
    global systeme_demarre, pompe_active
    pompe_active = False
    systeme_demarre = False
    label_etat.config(text="Système en attente", bg="gray")
    ajouter_evenement("Système mis en attente")

def cycle_automatique():
    global niveau, job_cycle
    
    if systeme_demarre:
        if pompe_active:
            niveau -=  2
        else:
            niveau += 1
        
        if niveau < 0:
            niveau = 0
        if niveau > 100:
            niveau = 100

        afficher_niveau()
        verifier_alarme()  # part 4 en vérifaiant toujours l'alarme à chaque changement de niveauc

    job_cycle = fenetre.after(1000, cycle_automatique)  # Appelle cette fonction à nouveau après 1000 ms (1 seconde)

# -----------------------------
# Fonctions de ma part 7
# -----------------------------

def ajouter_evenement(message):
    from datetime import datetime
    heure = datetime.now().strftime("%H:%M:%S")
    liste_historique.insert(0, f"{heure} - {message}")

# -----------------------------
# Fonctions de ma part 4
# -----------------------------
def verifier_alarme():
    global systeme_demarre, pompe_active, etat_alarme, alarme_clignotante, voyant_allume, dernier_etat_alarme

    if niveau >= 100:
        etat_alarme = "critique"
        alarme_clignotante = True
        label_alarme.config(text="Alarme CRITIQUE !! : niveau maximum")    
        systeme_demarre = False  # Arrêter le système en cas d'alarme critique
        pompe_active = False  # Arrêter la pompe en cas d'alarme critique
        label_etat.config(text="Système en attente", bg="gray")
        if dernier_etat_alarme != etat_alarme:
            ajouter_evenement("Alarme critique : niveau maximum - Arrêt automatique")
            dernier_etat_alarme = etat_alarme # Mettre à jour le dernier état d'alarme

    elif niveau <= 0:
        etat_alarme = "critique"
        alarme_clignotante = True
        label_alarme.config(text="Alarme CRITIQUE !! : niveau minimum")    
        systeme_demarre = False  # Arrêter le système en cas d'alarme critique
        pompe_active = False  # Arrêter la pompe en cas d'alarme critique
        label_etat.config(text="Système en attente", bg="gray")
        if dernier_etat_alarme != etat_alarme:
            ajouter_evenement("Alarme critique : niveau minimum - Arrêt automatique")
            dernier_etat_alarme = etat_alarme

    elif niveau >= 80:
        etat_alarme = "élevé"
        alarme_clignotante = False
        voyant_allume = True
        dessiner_voyant("orange")
        label_alarme.config(text="Alarme : niveau élevé")
        if dernier_etat_alarme != etat_alarme:
            ajouter_evenement("Alarme : niveau élevé")
            dernier_etat_alarme = etat_alarme

    elif niveau <= 20:
        etat_alarme = "bas"
        alarme_clignotante = False
        voyant_allume = True
        dessiner_voyant("yellow")
        label_alarme.config(text="Alarme : niveau bas")
        if dernier_etat_alarme != etat_alarme:
            ajouter_evenement("Alarme : niveau bas")
            dernier_etat_alarme = etat_alarme

    else:
        etat_alarme = "normal"
        alarme_clignotante = False
        voyant_allume = True
        dessiner_voyant("green")
        label_alarme.config(text="Aucune alarme")
        if dernier_etat_alarme != etat_alarme:
            ajouter_evenement("Retour à la normale")
            dernier_etat_alarme = etat_alarme

# -----------------------------
# Fonctions de ma part 6
# -----------------------------
def dessiner_voyant(couleur):
    canvas_alarme.delete("all")  # Effacer le contenu précédent du canvas
    canvas_alarme.create_oval(5, 5, 25, 25, fill=couleur, outline="black")  # Dessiner un cercle de la couleur spécifiée


def clignoter_alarme():
    global voyant_allume, job_clignotement
    
    if alarme_clignotante:
        if voyant_allume:
            dessiner_voyant("red")
        else:
            dessiner_voyant("white")
        
        voyant_allume = not voyant_allume

    job_clignotement = fenetre.after(500, clignoter_alarme)  # Clignote toutes les 500 ms

def fermer_application():
    global job_clignotement, job_cycle

    if job_clignotement is not None:
        fenetre.after_cancel(job_clignotement)  # Arrêter le clignotement de l'alarme

    if job_cycle is not None:
        fenetre.after_cancel(job_cycle)  # Arrêter le cycle automatique

    fenetre.destroy()  # Ferme la fenêtre et termine l'application
# -----------------------------
# Fenêtre principale
# -----------------------------

fenetre = tk.Tk()  #c'est ma fenêtre pricipale et c'est exactement comme mon écran SCADA 
fenetre.title("Supervision - Station de pompage & Cuve")
fenetre.geometry("1000x650")    # L * H

frame_gauche = tk.Frame(fenetre, padx=20, pady=10)
frame_gauche.grid(row=0, column=0, sticky="nsew")

frame_droite = tk.Frame(fenetre, padx=20, pady=10)
frame_droite.grid(row=0, column=1, sticky="nsew")

# -----------------------------
# Historique des événements - part 7
# -----------------------------

Label_historique = tk.Label(
    frame_droite,
    text="Historique des événements :",
    font=("Arial", 12, "bold")
)
Label_historique.pack(pady=5)

frame_historique = tk.Frame(frame_droite)
frame_historique.pack(pady=5)

scrollbar = tk.Scrollbar(frame_historique)
scrollbar.pack(side="right", fill="y")

liste_historique = tk.Listbox(frame_historique, width=65, height=7, yscrollcommand=scrollbar.set, font=("Courier", 9))
liste_historique.pack(side="left", fill="both")

scrollbar.config(command=liste_historique.yview)

# -----------------------------
# Label état pompe
# -----------------------------

label_etat = tk.Label(
    frame_gauche,
    text=" Système en attente ",
    bg="gray",
    fg="white",
    font=("Arial", 14),
    width=15
)
label_etat.pack(pady=20) # affiche-le dans la fenêtre, sans .pack() je vois rien !! 

# -----------------------------
# Label niveau
# -----------------------------

label_niveau = tk.Label(
    frame_gauche,
    text=f"Niveau : {niveau}%",
    font=("Arial", 14)
)
label_niveau.pack(pady=20)

# -----------------------------
# Label alarme - part 4
# -----------------------------
"""
label_alarme = tk.Label(
    fenetre,
    text="Aucune alarme",
    bg="white",
    fg="black",
    font=("Arial", 25),
)
label_alarme.pack(pady=20)
"""
canvas = tk.Canvas(frame_gauche, width=200, height=30, bg="white")
canvas.pack(pady=10)

frame_alarme = tk.Frame(frame_gauche)
frame_alarme.pack(pady=20)

canvas_alarme = tk.Canvas(frame_alarme, width=30, height=30, highlightthickness=0)
canvas_alarme.pack(side="left", padx=10)

label_alarme = tk.Label(
    frame_alarme,
    text="Aucune alarme",
    font=("Arial", 25),
)
label_alarme.pack(side="left")
# -----------------------------
# Boutons
# -----------------------------

btn_start = tk.Button(    # création de mon bouton
    frame_gauche,
    text="Ouvrir",
    bg="green",
    fg="white",
    width=10,
    command=start_pompe
)
btn_start.pack(pady=5)

btn_stop = tk.Button(
    frame_gauche,
    text="Fermer",
    bg="red",
    fg="white",
    width=10,
    command=stop_pompe
)
btn_stop.pack(pady=5)

####################### Part 2 #########################

btn_remplir = tk.Button(
    frame_gauche,
    text="Remplir",
    bg="blue",
    fg="white",
    width=10,
    command=remplir
)
btn_remplir.pack(pady=5)

btn_vider = tk.Button(
    frame_gauche,
    text="Vider",
    bg="orange",
    fg="white",
    width=10,
    command=vider
)
btn_vider.pack(pady=5)

####################### Part 3 #########################

btn_attente = tk.Button(
    frame_gauche,
    text="Attente",
    bg="gray",
    fg="white",
    width=15,
    command=mettre_en_attente
)
btn_attente.pack(pady=20)

cycle_automatique()

####################### Part 4 #########################
# tout ce qui a relation avec l'alarme en haut :la fonction verifier_alarme() et le label de l'alarme 

####################### Part 6 : HISTORIQUE DE NIVEAU #########################

historique_niveau = []

fig, ax = plt.subplots(figsize=(5, 3))
line, = ax.plot([], [])

ax.set_title("Evolution du niveau")
ax.set_ylim(0, 100)

canvas_graph = FigureCanvasTkAgg(fig, master=frame_droite)
canvas_graph.get_tk_widget().pack(pady=20)


dessiner_voyant("green")  # Initialiser le voyant en vert
clignoter_alarme()  # Démarrer le clignotement de l'alarme si nécessaire
afficher_niveau()

fenetre.protocol("WM_DELETE_WINDOW", fermer_application)

# -----------------------------
# Lancer l'application
# -----------------------------

fenetre.mainloop()  # ça lance l’application sans ça la fenêtre se ferme direct ! 