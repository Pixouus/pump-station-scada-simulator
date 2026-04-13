# 🏭 Pump Station SCADA Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Interface-Tkinter-orange)
![Matplotlib](https://img.shields.io/badge/Graphique-Matplotlib-green)
![Status](https://img.shields.io/badge/Status-En%20développement%20actif-brightgreen)
![LinkedIn](https://img.shields.io/badge/LinkedIn-HAMDI%20Sid--Ahmed-0077B5?logo=linkedin)

---

## 📌 Présentation

Application de supervision industrielle simulant une **station de pompage** avec interface graphique de type **SCADA (IHM)**, développée entièrement en Python.

Ce projet démontre des compétences en :
- 🔧 **Automatisme** — logique de fonctionnement, états système, interverrouillages
- 🖥️ **Supervision industrielle** — interface homme-machine (IHM), alarmes, voyants
- 🐍 **Programmation Python** — Tkinter, Matplotlib, cycle automatique

---

## 📸 Aperçu

| État normal | Alarme niveau bas | Alarme critique |
|---|---|---|
| ![Normal](screenshots/etat_normal.png) | ![Orange](screenshots/alarme_orange.png) | ![Critique](screenshots/alarme_critique.png) |


| Historique normal | Historique critique |
|---|---|
| ![h1](screenshots/historique_normal.png) | ![h2](screenshots/historique_critique.png) |
---

## ⚙️ Fonctionnalités

### 🔹 Simulation du process
- Cuve avec niveau de **0% à 100%**
- Pompe **ON / OFF** avec cycle automatique toutes les secondes
- Pompe ON → niveau **diminue** (-2%/s)
- Pompe OFF → niveau **augmente** (+1%/s)

### 🔹 Interface graphique (IHM)
- Affichage de l'état du système (en attente / pompe ouverte / fermée)
- Affichage du niveau en temps réel
- **Barre de niveau visuelle** colorée (vert / orange / rouge)
- **Graphique historique** du niveau (20 derniers points)
- **Historique des événements** horodaté avec anti-doublons (insert en haut)

### 🔹 Système d'alarmes
| Seuil | Voyant | Description |
|-------|--------|-------------|
| 20% ≤ niveau ≤ 80% | 🟢 Vert fixe | Aucune alarme |
| niveau ≥ 80% | 🟠 Orange clignotant | Alarme niveau haut |
| niveau ≤ 20% | 🟡 Jaune clignotant | Alarme niveau bas |
| niveau = 100% ou 0% | 🔴 Rouge clignotant | **CRITIQUE — Arrêt automatique** |

### 🔹 Logique industrielle
- **Interverrouillage** : impossible de vider si pompe fermée, impossible de remplir si pompe ouverte
- **Arrêt automatique** aux seuils critiques (0% et 100%)
- **État système** : blocage au démarrage jusqu'à action utilisateur
- **Fermeture propre** de l'application (annulation des boucles `after()`)

---

## 🛠️ Technologies utilisées

| Technologie | Usage |
|-------------|-------|
| Python 3.x | Langage principal |
| Tkinter | Interface graphique (IHM / SCADA) |
| Matplotlib | Graphique historique du niveau |

---

## 🚀 Lancement

### Prérequis
```bash
pip install matplotlib
```

### Démarrage
```bash
python main.py
```

---

## 🗂️ Structure du projet

```
pump-station-scada-simulator-python/
│
├── main.py                  # Application principale
├── .gitignore               # Fichiers exclus de Git
├── README.md                # Documentation du projet
│
└── screenshots/             # Captures d'écran de l'interface
    ├── etat_normal.png
    ├── alarme_orange.png
    ├── alarme_critique.png
    └── graphique.png
```

---

## 🧠 Concepts d'automatisme appliqués

- **Cycle automate** — simulation d'un cycle PLC avec `after(1000ms)`
- **États système** — attente / marche / arrêt automatique
- **Interverrouillages** — conditions de sécurité réalistes
- **Gestion des alarmes** — seuils bas / haut / critique
- **IHM SCADA** — voyants, barres de niveau, historique graphique

---

## 🔮 Évolutions prévues

- [ ] Mode **Automatique / Manuel**
- [X] **Historique des événements** horodaté
- [ ] Restructuration en plusieurs fichiers (`logique.py`, `interface.py`)
- [ ] Communication **Modbus TCP**
- [ ] Connexion **TIA Portal / PLCSIM** (Siemens)

---

## 👤 Auteur

**HAMDI Sid-Ahmed**  
Technicien en Automatisme & Supervision Industrielle  
🔗 [Mon profil LinkedIn](https://www.linkedin.com/in/hamdi-sid-ahmed)

---

> 💡 *Projet réalisé dans le cadre d'un apprentissage autonome en automatisme industriel et supervision Python.*
