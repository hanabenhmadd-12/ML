"""Script de génération automatique du diaporama PowerPoint (presentation_trustjob.pptx)
Prérequis : pip install python-pptx
Exécution : python generer_powerpoint.py
"""

from pathlib import Path
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
except ImportError:
    print("[!] Le module 'python-pptx' n'est pas installé.")
    print("[*] Installez-le avec : pip install python-pptx")
    print("[*] Puis relancez : python generer_powerpoint.py")
    sys.exit(1)

OUTPUT_FILE = Path(__file__).resolve().parent / "presentation_trustjob.pptx"

# Couleurs de la charte
C_NAVY = RGBColor(15, 23, 42)      # #0F172A
C_BLUE = RGBColor(37, 99, 235)     # #2563EB
C_MUTED = RGBColor(100, 116, 139)  # #64748B
C_WHITE = RGBColor(255, 255, 255)
C_LIGHT = RGBColor(248, 250, 252)

prs = Presentation()
prs.slide_width = Inches(13.333)  # Format 16:9 moderne
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, title_text, category_text="PROJET MACHINE LEARNING • LSI 3"):
    # Bandeau catégorie
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.5), Inches(0.4))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category_text.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = C_BLUE

    # Titre de la slide
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.8))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_NAVY

SLIDES_DATA = [
    {
        "is_cover": True,
        "title": "Détection Intelligente de Fausses Offres d’Emploi",
        "subtitle": "De la donnée textuelle brute à l'inférence en production (Projet TrustJob AI)",
        "meta": "Projet Machine Learning • LSI 3 (2026-2027)\nPrésenté par : [Noms des membres du groupe]\nJeu de données : EMSCAD (18 000 annonces)"
    },
    {
        "cat": "PARTIE 1 • INTRODUCTION & PROBLÉMATIQUE (≈ 1 MIN)",
        "title": "Contexte, Problématique & Présentation du Jeu de Données",
        "bullets": [
            "Contexte socio-économique : Multiplication des escroqueries au recrutement en ligne (extorsion financière, vols de données personnelles, délit de mule bancaire).",
            "Problématique scientifique : « Peut-on prédire avec fiabilité si une offre d'emploi est frauduleuse à partir de son descriptif textuel et de ses métadonnées techniques ? »",
            "Jeu de données retenu : Dataset EMSCAD (17 880 annonces, 18 variables descriptives, cible binaire 'fraudulent').",
            "Le Piège caché du jeu : Fort déséquilibre des classes (95,1% d'annonces légitimes / 4,9% frauduleuses). L'accuracy seule est trompeuse, le F1-score est indispensable.",
            "Objectif du projet : Comparer 4 architectures de classification, optimiser par validation croisée stratifiée et déployer un pipeline en production."
        ]
    },
    {
        "cat": "PARTIE 2 • ÉTAT DE L'ART (≈ 1 MIN)",
        "title": "Travaux Existants & Benchmarks Académiques sur EMSCAD",
        "bullets": [
            "Vidros et al. (2017) [Créateurs d'EMSCAD] : Random Forest & Naive Bayes avec sac de mots (BoW) -> Score F1 = 0,78 (Accuracy 97,2%).",
            "Habiba et al. (IEEE, 2021) : SVM Linéaire avec TF-IDF pondéré -> Score F1 = 0,81 (Accuracy 98,1%).",
            "Communauté Kaggle (2023) : Modèles ensemblistes (XGBoost, Logistic Regression) -> F1-score moyen entre 0,80 et 0,84.",
            "Constat clé de l'état de l'art : Les classifieurs linéaires à marge maximale (SVM) sont historiquement les plus performants face à des espaces textuels creux de haute dimension."
        ]
    },
    {
        "cat": "PARTIE 3 • MÉTHODES PROPOSÉES (≈ 3,5 MIN)",
        "title": "Pipeline Méthodologique de Traitement (Étapes 1 à 7)",
        "bullets": [
            "Étape 1-3 : Exploration, analyse des types, traitement des valeurs manquantes et gestion des valeurs aberrantes.",
            "Étape 4 : Prétraitement vectoriel (concaténation textuelle, TF-IDF unigrammes/bigrammes et encodage des indicateurs booléens).",
            "Étape 5 : Sélection statistique des 5 000 caractéristiques les plus discriminantes via SelectKBest (Chi-deux).",
            "Étape 6 : Modélisation comparative (Régression Logistique, KNN, SVM Linéaire, Random Forest).",
            "Étape 7 : Optimisation des hyperparamètres par GridSearchCV avec 4 plis stratifiés et métrique F1.",
            "Règle d'or anti-fuite : Ajustement (fit) du TF-IDF et du SelectKBest exclusivement sur le jeu d'apprentissage."
        ]
    },
    {
        "cat": "PARTIE 3 • PRÉPARATION DES DONNÉES",
        "title": "Exploration, Visualisation & Valeurs Aberrantes (Étapes 1 à 3)",
        "bullets": [
            "Exploration (shape, info) : 12 000 offres d'entraînement et 2 400 offres de validation interne holdout.",
            "Visualisation du déséquilibre : 95,1% légitimes vs 4,9% frauduleuses -> Obligation d'utiliser 'class_weight=balanced'.",
            "Corrélations clés observées : L'absence de logo d'entreprise (has_company_logo=0) et l'absence de questionnaire (has_questions=0) sont fortement corrélées à la fraude.",
            "Traitement des valeurs aberrantes & manquantes : Remplacement des champs manquants par des chaînes vides consolidées. L'absence d'information constitue un signal prédictif en soi."
        ]
    },
    {
        "cat": "PARTIE 3 • PRÉTRAITEMENT & SÉLECTION",
        "title": "Ingénierie des Caractéristiques Textuelles (Étapes 4 & 5)",
        "bullets": [
            "Concaténation textuelle : Regroupement de 13 champs (titre, entreprise, description, compétences, etc.) en un corpus unique.",
            "Vectorisation TF-IDF : Pondération par fréquence de terme et fréquence inverse de document avec n-grammes (1, 2) et suppression des stopwords.",
            "Sélection par SelectKBest (Chi2) : Réduction de 45 000 descripteurs à 5 000 caractéristiques essentielles.",
            "Impact direct : Gain de 80% sur le temps de calcul, élimination du bruit lexical et focalisation sur les termes hautement discriminants (wire transfer, upfront fee, clerk...)."
        ]
    },
    {
        "cat": "PARTIE 3 • DESCRIPTION DU MODÈLE 1",
        "title": "Modèle 1 : Machine à Vecteurs de Support (LinearSVC)",
        "bullets": [
            "Principe théorique : Recherche de l'hyperplan optimal maximisant la marge géométrique de séparation 2/||w|| entre les deux classes.",
            "Algorithme pas à pas : Projection des 5 000 attributs TF-IDF -> Optimisation sous contrainte de marge souple (paramètre de pénalité C) -> Classification basée sur le signe de w^T x + b.",
            "Hyperparamètres réglés au GridSearchCV : model__C dans [0.5, 2.0] avec class_weight='balanced'.",
            "Justification : Mathématiquement le modèle le plus robuste contre le surapprentissage sur des données textuelles creuses de très haute dimension."
        ]
    },
    {
        "cat": "PARTIE 3 • DESCRIPTION DU MODÈLE 2",
        "title": "Modèle 2 : Forêt Aléatoire (Random Forest)",
        "bullets": [
            "Principe théorique : Modèle d'ensemble combinant 50 arbres de décision décorrélés entraînés par bagging (Bootstrap Aggregating).",
            "Algorithme pas à pas : Échantillonnage aléatoire avec remise -> Construction d'arbres avec sélection aléatoire de variables à chaque nœud -> Vote majoritaire final.",
            "Hyperparamètres réglés au GridSearchCV : model__max_depth dans [20, None] et model__n_estimators = 50 avec class_weight='balanced'.",
            "Justification : Capacité à capturer des interactions non-linéaires entre les mots-clés et les métadonnées de l'annonce."
        ]
    },
    {
        "cat": "PARTIE 3 • PROTOCOLE D'OPTIMISATION",
        "title": "Optimisation des Hyperparamètres : GridSearchCV (cv = 4)",
        "bullets": [
            "Protocole de validation : StratifiedKFold à 4 plis (chaque pli conserve rigoureusement le ratio de 4,9% de fraudes).",
            "Métrique de scoring : scoring='f1' (optimise le compromis entre précision et rappel au lieu de l'exactitude brute).",
            "Reproductibilité totale : random_state=42 fixé à chaque étape d'échantillonnage.",
            "Résultats de l'optimisation : Paramètre optimal C = 2.0 pour le SVM et la Régression Logistique ; Profondeur complète pour Random Forest."
        ]
    },
    {
        "cat": "PARTIE 4 • EXPÉRIMENTATIONS (≈ 3,5 MIN)",
        "title": "Tableau Récapitulatif des Performances Comparées",
        "table": True
    },
    {
        "cat": "PARTIE 4 • ANALYSE DÉTAILLÉE DES MATRICES DE CONFUSION",
        "title": "Interprétation des Matrices de Confusion sur le Jeu de Test (2 400 offres)",
        "bullets": [
            "Composition du test holdout : 2 282 annonces légitimes (95,1%) et 118 frauduleuses (4,9%).",
            "Matrice du SVM Linéaire (Meilleur modèle) : 2 264 Vrais Négatifs, 18 Faux Positifs, 20 Faux Négatifs, 98 Vrais Positifs.",
            "Interprétation du rappel (83,1%) : Le SVM intercepte 98 fraudes sur 118, laissant passer seulement 20 arnaques.",
            "Comparaison Random Forest : Random Forest fait moins de faux positifs (7 FP) mais laisse passer 32 fraudes (rappel de 72,9%).",
            "Arbitrage de sécurité : En détection de fraude, un faux négatif (arnaque manquée) est critique. Le SVM est nettement supérieur pour protéger les candidats."
        ]
    },
    {
        "cat": "PARTIE 4 • VALIDATION & DÉPLOIEMENT",
        "title": "Positionnement face à l'État de l'Art & Application Web TrustJob AI",
        "bullets": [
            "Gain face à l'état de l'art : Score F1 de 83,76% (TrustJob AI) vs 78,0% (Vidros et al.) et 81,0% (IEEE 2021) -> +2,7 points de performance.",
            "Pipeline autonome : Modèle et sélecteur exportés dans outputs/trustjob_pipeline.joblib pour l'inférence temps réel.",
            "Application web interactive (app.py) : Développée en Python pur (sans framework lourd), offrant une jauge de risque dynamique et une analyse en temps réel (< 10 ms).",
            "Double mode d'analyse : Saisie détaillée par champs ou analyse express par copier-coller de texte brut d'annonces réelles."
        ]
    },
    {
        "cat": "PARTIE 5 • CONCLUSION & PERSPECTIVES (≈ 1 MIN)",
        "title": "Bilan du Projet, Limites & Pistes d'Amélioration",
        "bullets": [
            "Rappel de l'objectif : Détection automatisée des fausses annonces d'emploi par NLP et Machine Learning.",
            "Meilleur modèle retenu : SVM Linéaire (F1 = 83,8%, Précision = 84,5%, Rappel = 83,1%, Exactitude = 98,4%).",
            "Limites identifiées : Ancienneté du corpus d'entraînement (2012-2014) et dépendance linguistique (corpus latin, pas de traitement de l'arabe/derja sans module dédié).",
            "Piste 1 (Modèles de Langage) : Expérimenter des Transformers pré-entraînés (RoBERTa / CamemBERT) pour capturer les nuances sémantiques plus subtiles.",
            "Piste 2 (Vérification Externe) : Interfacer le pipeline avec les registres officiels d'entreprises (API SIRENE en France, RNE en Tunisie) pour valider l'existence légale de l'employeur."
        ]
    }
]

for idx, data in enumerate(SLIDES_DATA):
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background(slide, C_WHITE)

    if data.get("is_cover"):
        # Fond sombre pour la couverture
        set_slide_background(slide, C_NAVY)
        
        # Titre
        t_box = slide.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(2.0))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = data["title"]
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        # Sous-titre
        p2 = tf.add_paragraph()
        p2.text = data["subtitle"]
        p2.font.size = Pt(18)
        p2.font.color.rgb = RGBColor(147, 197, 253) # Bleu clair
        p2.space_before = Pt(16)

        # Métadonnées
        m_box = slide.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.0))
        tf_m = m_box.text_frame
        tf_m.word_wrap = True
        for line in data["meta"].split("\n"):
            pm = tf_m.add_paragraph()
            pm.text = line
            pm.font.size = Pt(13)
            pm.font.color.rgb = RGBColor(203, 213, 225)
            pm.space_before = Pt(6)
        continue

    # Diapositives standards
    add_header(slide, data["title"], data.get("cat", ""))

    if data.get("table"):
        # Affichage du tableau récapitulatif
        rows_data = [
            ["Modèle", "Meilleurs Paramètres", "F1 (CV 4 plis)", "Accuracy", "Précision", "Rappel", "F1 (Test)"],
            ["Règle traditionnelle", "Liste mots-clés", "—", "89,92 %", "0,79 %", "0,85 %", "0,82 %"],
            ["Régression Logistique", "C = 2.0", "66,75 %", "95,92 %", "55,38 %", "87,29 %", "67,76 %"],
            ["KNN (k=3)", "weights=distance", "71,32 %", "98,12 %", "98,67 %", "62,71 %", "76,68 %"],
            ["Random Forest", "max_depth=None", "75,41 %", "98,38 %", "92,47 %", "72,88 %", "81,52 %"],
            ["SVM Linéaire 🏆", "C = 2.0", "82,88 %", "98,42 %", "84,48 %", "83,05 %", "83,76 %"]
        ]
        table_shape = slide.shapes.add_table(6, 7, Inches(0.8), Inches(2.0), Inches(11.7), Inches(3.2))
        table = table_shape.table
        
        for r_idx, row in enumerate(rows_data):
            for c_idx, val in enumerate(row):
                cell = table.cell(r_idx, c_idx)
                cell.text = val
                p = cell.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                p.font.size = Pt(11)
                if r_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = C_WHITE
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = C_BLUE
                elif r_idx == 5:
                    p.font.bold = True
                    p.font.color.rgb = C_NAVY
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(220, 252, 231) # Vert clair
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(241, 245, 249) if r_idx % 2 == 1 else C_WHITE

        # Note de lecture
        comm_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2))
        tf_comm = comm_box.text_frame
        tf_comm.word_wrap = True
        p_c1 = tf_comm.paragraphs[0]
        p_c1.text = "• Lecture du tableau : Le SVM Linéaire est le grand vainqueur avec un F1-score de 83,76% et 98,42% d'exactitude."
        p_c1.font.size = Pt(12)
        p_c1.font.bold = True
        p_c1.font.color.rgb = C_BLUE
        
        p_c2 = tf_comm.add_paragraph()
        p_c2.text = "• Prise en compte du déséquilibre : L'accuracy seule de 98% peut être trompeuse (le KNN a 98% d'accuracy mais un rappel médiocre de 62%). Le SVM assure l'équilibre optimal entre précision (84,5%) et rappel (83,1%)."
        p_c2.font.size = Pt(11)
        p_c2.font.color.rgb = C_MUTED
        p_c2.space_before = Pt(4)
        continue

    # Contenu en puces
    content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf = content_box.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(data.get("bullets", [])):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = f"•  {bullet}"
        p.font.size = Pt(13)
        p.font.color.rgb = C_NAVY
        p.space_before = Pt(14)

prs.save(str(OUTPUT_FILE))
print(f"[+] Présentation générée avec succès : {OUTPUT_FILE}")
