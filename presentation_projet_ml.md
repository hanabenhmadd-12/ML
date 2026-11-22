# PRÉSENTATION DE PROJET MACHINE LEARNING (LSI 3 • 2026-2027)
## Sujet : Détection Automatisée de Fausses Offres d’Emploi (TrustJob AI)
**Durée de la soutenance : 10 minutes**  
**Nombre de diapositives : 13 diapositives (conforme à la consigne de 12 à 15 diapositives)**

---

## DIAPOSITIVE 1 : Titre & Introduction de l'Équipe
* **Titre principal :** Détection Intelligente de Fausses Offres d'Emploi par Machine Learning
* **Sous-titre :** De la donnée textuelle brute à l'inférence en production (Projet TrustJob AI)
* **Cadre :** Projet Machine Learning — LSI 3 (Année universitaire 2026-2027)
* **Membres du groupe :** [Vos Noms et Prénoms]
* **Jeu de données retenu :** EMSCAD (Employment Scam Aegean Dataset) — 18 000 annonces

> **🎤 Discours oral (30 secondes) :**  
> *"Bonjour à tous. Nous vous présentons aujourd'hui notre projet de Machine Learning intitulé TrustJob AI, dédié à la détection automatisée des fausses offres d'emploi sur internet. Nous allons vous présenter la démarche complète que nous avons suivie, depuis le nettoyage des données textuelles jusqu'au déploiement du modèle sélectionné."*

---

## DIAPOSITIVE 2 : PARTIE 1 • Introduction & Problématique (≈ 1 min)
* **1. Contexte :**  
  * Explosion des annonces frauduleuses sur LinkedIn, Indeed et les réseaux sociaux.  
  * Conséquences graves pour les candidats : extorsion financière (*frais de dossier*), vol d'identité et délit de « mule bancaire ».
* **2. Problématique précise :**  
  * *« Peut-on prédire avec fiabilité si une offre d'emploi est frauduleuse à partir de son descriptif textuel et de ses métadonnées techniques ? »*
* **3. Le Jeu de Données (EMSCAD) :**  
  * **Source :** Kaggle / University of the Aegean (plateforme Workable).  
  * **Volume :** 17 880 offres d'emploi (12 000 train + 2 400 holdout de validation interne + 5 599 test externe).  
  * **Variables :** 18 colonnes (titre, description, exigences, profil entreprise, salaire, localisation, télétravail, logo...).  
  * **Cible ($y$) :** `fraudulent` (Binaire : 0 = Légitime, 1 = Frauduleuse).
* **4. Le Piège caché du jeu :**  
  * **Déséquilibre sévère des classes :** 95,1 % d'annonces légitimes contre seulement 4,9 % d'annonces frauduleuses. Un modèle naïf prédisant toujours « 0 » atteindrait 95 % d'accuracy sans rien détecter !
* **5. Objectif :**  
  * Comparer 4 algorithmes d'apprentissage supervisé, optimiser le score F1 (et le rappel) par validation croisée à 4 plis, et concevoir une interface d'évaluation en temps réel.

> **🎤 Discours oral (1 minute) :**  
> *"Les arnaques à l'emploi constituent un fléau croissant. Notre objectif est de répondre à cette question : peut-on classifier automatiquement une offre dès sa parution ? Nous avons travaillé sur le dataset international EMSCAD de près de 18 000 annonces. Le piège majeur de ce jeu réside dans son fort déséquilibre : moins de 5 % des offres sont frauduleuses. L'accuracy seule ne servira donc à rien : notre métrique phare sera le score F1. Voici le plan imposé que nous suivrons : état de l'art, méthodes, expérimentations, puis conclusion."*

---

## DIAPOSITIVE 3 : PARTIE 2 • État de l'Art (≈ 1 min)
* **Travaux académiques et benchmarks de référence sur le jeu EMSCAD :**

| Référence | Modèle utilisé | Approche / Représentation | Score rapporté |
| :--- | :--- | :--- | :--- |
| **Vidros et al. (2017)** *(Créateurs du dataset EMSCAD)* | Random Forest / Naive Bayes | Sac de mots (BoW) + Métadonnées | **F1-score = 0.78** (Accuracy ~97.2%) |
| **Habiba et al. (IEEE, 2021)** | SVM Linéaire | TF-IDF (unigrammes et bigrammes) | **F1-score = 0.81** (Accuracy ~98.1%) |
| **Benchmark Kaggle Community (2023)** | Logistic Regression / XGBoost | TF-IDF pondéré + Encodage One-Hot | **F1-score = 0.80 à 0.84** |

* **Constat clé issu de la littérature :**
  1. Les modèles simples linéaires (SVM) rivalisent avec les modèles d'ensemble complexes car la vectorisation textuelle crée un espace de haute dimension creux (*sparse matrix*).
  2. Le prétraitement du texte (nettoyage, n-grammes) est l'élément le plus déterminant de la performance finale.

> **🎤 Discours oral (1 minute) :**  
> *"Dans la littérature scientifique, les créateurs originaux du dataset, Vidros et al., avaient obtenu un F1-score de 0,78 avec Random Forest. Des publications plus récentes sur IEEE ont démontré que le SVM linéaire avec TF-IDF parvenait à atteindre un F1 de 0,81. Ces résultats constituent notre jalon de comparaison pour évaluer nos propres architectures."*

---

## DIAPOSITIVE 4 : PARTIE 3 • Le Pipeline Global de Traitement
* **Architecture pas à pas du pipeline Machine Learning (Étapes 1 à 7) :**

```
[ Données Brutes (18 colonnes) ]
           │
           ▼
[ Étape 1-3 : Exploration, Traitement des Valeurs Manquantes & Aberrantes ]
           │
           ▼
[ Étape 4 : Concaténation Textuelle + TF-IDF (1-2 n-grammes) + Binarisation des Flags ]
           │
           ▼
[ Étape 5 : Sélection de Caractéristiques (SelectKBest, chi2, k=5 000) ]
           │
           ▼
[ Étape 6 : Modélisation (4 Algorithmes : LR, KNN, SVM, Random Forest) ]
           │
           ▼
[ Étape 7 : Optimisation par Validation Croisée (GridSearchCV, cv = 4, Scoring F1) ]
```

* **Garantie méthodologique :**  
  * Utilisation d'un `Pipeline` Scikit-Learn strict : le `fit` des transformations (TF-IDF, sélection de variables) est appliqué **uniquement sur le train set** afin d'éviter toute fuite de données (*Data Leakage*).

> **🎤 Discours oral (30 secondes) :**  
> *"Pour aborder la Partie 3, voici notre pipeline d'ingénierie. Il relie l'ingestion brute à la classification finale en veillant scrupuleusement à isoler le jeu d'apprentissage du jeu de test à chaque étape de transformation vectorielle."*

---

## DIAPOSITIVE 5 : PARTIE 3 • Exploration, Nettoyage & Valeurs Aberrantes (Étapes 1 à 3)
* **Étape 1 : Exploration (`shape`, `info`, `describe`)**
  * Train interne : 12 000 lignes ; Validation holdout : 2 400 lignes.
  * 13 champs textuels (description, exigences, etc.) et 3 indicateurs booléens (`has_company_logo`, `telecommuting`, `has_questions`).
* **Étape 2 : Visualisation des distributions**
  * *Figure 1 (Déséquilibre des classes)* : 11 412 offres légitimes (95,1 %) contre 588 frauduleuses (4,9 %).
  * *Figure 2 (Corrélations & Métadonnées)* : Forte corrélation négative entre `has_company_logo` et la fraude : **les fausses offres n'ont pas de logo dans plus de 75 % des cas**.
* **Étape 3 : Traitement des valeurs aberrantes et manquantes**
  * Des champs comme `salary_range` ou `department` présentent plus de 60 % de valeurs manquantes.
  * **Décision justifiée :** Plutôt que de supprimer ces lignes, l'absence d'information est traitée comme un signal en soi. Les champs textuels manquants sont imputés par une chaîne vide `""` puis fusionnés dans un corpus textuel consolidé.

> **🎤 Discours oral (45 secondes) :**  
> *"L'exploration révèle deux faits marquants : un déséquilibre extrême des classes et un grand nombre de valeurs manquantes dans les métadonnées. Plutôt que de supprimer des lignes et de perdre des exemples précieux de fraudes, nous avons transformé cette absence en information : un profil sans logo ou sans questions préalables augmente statistiquement la suspicion."*

---

## DIAPOSITIVE 6 : PARTIE 3 • Prétraitement & Sélection de Caractéristiques (Étapes 4 & 5)
* **Étape 4 : Prétraitement vectoriel (NLP)**
  * **Agrégation textuelle :** Concaténation de l'ensemble des champs descriptifs en un seul bloc textuel par annonce.
  * **Vectorisation TF-IDF :** Extraction des unigrammes et bigrammes (`ngram_range=(1, 2)`), filtrage des termes trop rares (`min_df=2`) et suppression des mots vides (*stopwords*).
  * **Indicateurs catégoriels :** Conservation des flags binaires (`telecommuting`, `has_company_logo`, `has_questions`).
* **Étape 5 : Sélection des caractéristiques (`SelectKBest`)**
  * La vectorisation initiale génère plus de 45 000 termes distincts.
  * Application du test statistique du $\chi^2$ (*Chi-deux*) via `SelectKBest(k=5000)`.
  * **Justification :** Réduction drastique du temps de calcul (-80%), élimination du bruit lexical, et focalisation sur les termes à fort pouvoir discriminant (ex. *wire transfer*, *processing fee*, *clerk*, *unlimited earnings*).

> **🎤 Discours oral (45 secondes) :**  
> *"À l'étape de prétraitement, le défi est la très grande dimensionnalité : plus de 45 000 caractéristiques textuelles. Grâce au test du Chi-deux avec SelectKBest, nous conservons les 5 000 n-grammes les plus informatifs. Cela accélère l'apprentissage tout en supprimant le bruit des mots anecdotiques."*

---

## DIAPOSITIVE 7 : PARTIE 3 • Modèle 1 : Machine à Vecteurs de Support (LinearSVC)
* **Définition :**  
  Classifieur linéaire cherchant l'hyperplan optimal qui maximise la marge géométrique de séparation entre les annonces légitimes et frauduleuses.
* **Représentation géométrique :**
  ```
          Classes Légitimes (o)       |       Classes Frauduleuses (x)
             o     o                  |               x      x
                o     o    [ Marge ]  |  [ Marge ]       x
          -------------------( Vecteurs Supports )-------------------
                                [ Hyperplan ]
  ```
* **Fonctionnement pas à pas :**
  1. Projection des 5 000 caractéristiques TF-IDF dans l'espace euclidien.
  2. Résolution du problème d'optimisation quadratique pour maximiser la marge $\frac{2}{\|\mathbf{w}\|}$.
  3. Gestion des erreurs de classification via une pénalité $C$.
* **Hyperparamètres optimisés (GridSearchCV) :**
  * `model__C` : $[0.5, 2.0]$ (compromis entre largeur de marge et tolérance d'erreur).
  * Pondération : `class_weight='balanced'` pour compenser le ratio 95/5.
* **Justification du choix :** Idéal pour les données textuelles creuses de haute dimension ; convergence rapide et faible risque de surapprentissage.

> **🎤 Discours oral (45 secondes) :**  
> *"Notre premier modèle est le SVM Linéaire. Son principe fondamental est de trouver l'hyperplan qui sépare les deux classes avec la plus grande marge possible. C'est le standard de référence en classification de texte grâce à sa robustesse mathématique face à des milliers de variables creuses."*

---

## DIAPOSITIVE 8 : PARTIE 3 • Modèle 2 : Forêt Aléatoire (Random Forest)
* **Définition :**  
  Méthode d'ensemble combinant plusieurs arbres de décision indépendants entraînés sur des sous-échantillons aléatoires (*Bagging* + sélection aléatoire de variables).
* **Représentation du modèle d'ensemble :**
  ```
                       [ Offre d'emploi (X) ]
                         /        |        \
                   [Arbre 1]  [Arbre 2]  [Arbre 50]
                      ↓          ↓          ↓
                   [Fraude]   [Légitime] [Fraude]
                         \        |        /
                     [ Vote Majoritaire : Fraude ]
  ```
* **Fonctionnement pas à pas :**
  1. Génération de 50 sous-jeux par rééchantillonnage avec remise (*bootstrap*).
  2. Construction de chaque arbre en choisissant le meilleur découpage parmi un sous-ensemble aléatoire de variables.
  3. Agrégation finale par vote majoritaire de tous les arbres.
* **Hyperparamètres optimisés (GridSearchCV) :**
  * `model__n_estimators` : 50 arbres.
  * `model__max_depth` : $[20, \text{None}]$ (profondeur limitée vs arbres complets).
  * Pondération : `class_weight='balanced'`.
* **Justification du choix :** Capacité à capturer les interactions non linéaires complexes entre mots-clés et métadonnées.

> **🎤 Discours oral (45 secondes) :**  
> *"Notre deuxième modèle est le Random Forest. Il construit un comité de 50 arbres de décision votant démocratiquement. Nous l'avons retenu pour sa capacité à déceler des relations non linéaires que des modèles linéaires stricts pourraient ignorer."*

---

## DIAPOSITIVE 9 : PARTIE 3 • Optimisation par Validation Croisée (Étape 7)
* **Protocole expérimental : `StratifiedKFold` avec $K = 4$ plis**
* **Schéma du découpage :**
  * *Itération 1 :* [ Test (Pli 1) ] [ Train (Pli 2) ] [ Train (Pli 3) ] [ Train (Pli 4) ]
  * *Itération 2 :* [ Train (Pli 1) ] [ Test (Pli 2) ] [ Train (Pli 3) ] [ Train (Pli 4) ]
  * *Itération 3 :* [ Train (Pli 1) ] [ Train (Pli 2) ] [ Test (Pli 3) ] [ Train (Pli 4) ]
  * *Itération 4 :* [ Train (Pli 1) ] [ Train (Pli 2) ] [ Train (Pli 3) ] [ Test (Pli 4) ]
* **Points méthodologiques majeurs :**
  * **Stratification :** Préservation exacte du ratio 4,9 % de fraudes dans chaque pli.
  * **Critère d'optimisation :** `scoring='f1'` (privilégie l'équilibre Précision/Rappel plutôt que la simple exactitude globale).
  * Reproductibilité garantie par la fixation stricte de la graine aléatoire (`random_state=42`).

> **🎤 Discours oral (30 secondes) :**  
> *"Pour régler nos hyperparamètres, nous avons appliqué une validation croisée stratifiée à 4 plis avec GridSearchCV. La stratification est indispensable pour s'assurer que chaque pli contienne exactement la même proportion d'annonces frauduleuses."*

---

## DIAPOSITIVE 10 : PARTIE 4 • Expérimentations : Tableau Récapitulatif Global
* **Tableau récapitulatif officiel des performances (Évaluation sur le jeu de test holdout de 2 400 offres) :**

| Modèle | Meilleurs Paramètres | F1 (CV 4 plis) | Accuracy | Précision | Rappel | F1-Score (Test) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Règle traditionnelle** | Liste fixe de mots-clés | — | 89,92 % | 0,79 % | 0,85 % | 0,82 % |
| **Régression Logistique** | `{'model__C': 2.0}` | 66,75 % | 95,92 % | 55,38 % | **87,29 %** | 67,76 % |
| **KNN (k=3)** | `{'weights': 'distance'}` | 71,32 % | 98,12 % | **98,67 %** | 62,71 % | 76,68 % |
| **Random Forest** | `{'max_depth': None}` | 75,41 % | 98,38 % | 92,47 % | 72,88 % | 81,52 % |
| **SVM Linéaire** 🏆 | `{'model__C': 2.0}` | **82,88 %** | **98,42 %** | 84,48 % | 83,05 % | **83,76 %** |

* **Lecture immédiate du tableau :**
  1. La **règle naïve de mots-clés échoue totalement** (F1 < 1%) en raison du nombre massif de faux positifs.
  2. Le **SVM Linéaire est le grand vainqueur** : il maximise le F1-score à **83,76 %** avec un équilibre remarquable entre précision (84,5 %) et rappel (83,1 %).

> **🎤 Discours oral (1 minute) :**  
> *"Voici le tableau récapitulatif de nos résultats. La règle par mots-clés montre l'échec d'une approche non statistique. Le SVM linéaire remporte la première place avec un F1 de 83,8 % en test et une exactitude de 98,4 %. Contrairement au KNN qui est trop prudent ou à la régression logistique qui déclenche trop de fausses alertes, le SVM offre l'équilibre opérationnel parfait."*

---

## DIAPOSITIVE 11 : PARTIE 4 • Analyse Approfondie des Matrices de Confusion (Étape 8)
* **Comparaison sur le jeu de test holdout (Total = 2 400 annonces : 2 282 légitimes / 118 frauduleuses) :**

### Matrice 1 : SVM Linéaire (Meilleur Modèle)
```
                    Prédit Légitime (0)    Prédit Fraude (1)
  Réel Légitime (0)       2 264 (VN)              18 (FP)      -> Spécificité : 99,2 %
  Réel Fraude (1)            20 (FN)              98 (VP)      -> Rappel : 83,1 %
```
* *Interprétation :* Sur 118 vraies fraudes, **98 sont interceptées**, seulement 20 passent inaperçues. Seules 18 annonces saines subissent une fausse alerte sur 2 282.

### Matrice 2 : Forêt Aléatoire (Random Forest)
```
                    Prédit Légitime (0)    Prédit Fraude (1)
  Réel Légitime (0)       2 275 (VN)               7 (FP)
  Réel Fraude (1)            32 (FN)              86 (VP)      -> Rappel : 72,9 %
```
* *Interprétation :* Random Forest génère moins de fausses alertes (7 FP), mais **laisse passer 32 fraudes (contre 20 pour le SVM)**. En cybersécurité, laisser passer une arnaque coûte beaucoup plus cher qu'un contrôle manuel : le SVM est donc nettement supérieur.

> **🎤 Discours oral (1 minute) :**  
> *"Analysons les matrices de confusion. Sur 118 annonces frauduleuses réelles, le SVM en capture 98 et n'en manque que 20. Le Random Forest, quant à lui, en rate 32. Dans le domaine de la sécurité des recrutements, le coût d'un faux négatif est critique : une fraude non détectée peut ruiner un candidat. C'est pourquoi le rappel supérieur du SVM en fait le choix évident."*

---

## DIAPOSITIVE 12 : PARTIE 4 • Positionnement face à l'État de l'Art & Déploiement
* **1. Comparaison avec la littérature académique :**
  * Baseline Vidros et al. (2017) : $F_1 = 78,0\ \%$
  * Publication IEEE (2021) : $F_1 = 81,0\ \%$
  * **Notre Modèle TrustJob AI (2026-2027) : $F_1 = 83,76\ \%$** (Gain de +2,7 points par rapport à la littérature grâce au SelectKBest et à la pondération TF-IDF optimisée).
* **2. Industrialisation & Démonstration :**
  * Export du modèle final dans un pipeline autonome : `outputs/trustjob_pipeline.joblib`.
  * Déploiement d'une **interface web animée et réactive** (`app.py` + `static/index.html`) :
    * Analyse en temps réel d'offres non structurées (Mode Express).
    * Calcul dynamique de la jauge de risque en pourcentage via la fonction sigmoïde appliquée à la distance algébrique du SVM :
      $$\text{Risque}(\%) = \frac{100}{1 + e^{-\text{decision\_function}(x)}}$$
    * Export immédiat des rapports d'audit au format JSON.

> **🎤 Discours oral (45 secondes) :**  
> *"Notre pipeline dépasse les scores de la littérature avec un F1 de 83,76 %. Mais nous ne nous sommes pas arrêtés aux métriques : nous avons industrialisé le modèle dans une application web légère et animée permettant à un utilisateur d'évaluer n'importe quelle offre en temps réel avec un score de risque probabiliste."*

---

## DIAPOSITIVE 13 : PARTIE 5 • Conclusion & Perspectives (≈ 1 min)
* **1. Synthèse du projet :**  
  * Objectif validé : détection automatique et fiable de fausses offres avec un taux d'exactitude de 98,4 % et un F1-score de 83,8 %.
* **2. Modèle retenu :**  
  * **SVM Linéaire** optimisé par validation croisée 4 plis (`C = 2.0`, `class_weight='balanced'`).
* **3. Limites identifiées :**  
  * Dépendance linguistique : corpus principalement anglophone/francophone (pas de prise en charge native de l'arabe/derja sans prétraitement spécifique).
  * Évolution temporelle des fraudes : le dataset d'origine ne prend pas en compte les arnaques récentes basées sur l'IA générative.
* **4. Deux pistes d'amélioration concrètes :**  
  1. **Modèles de langage pré-entraînés (Transformers) :** Tester des modèles comme *RoBERTa* ou *CamemBERT* pour une meilleure compréhension du contexte sémantique subtil.
  2. **Connexion externe à des registres officiels :** Coupler l'analyse textuelle à une vérification d'API d'entreprises (SIRENE en France, RNE en Tunisie) pour valider l'existence légale de l'employeur.

> **🎤 Discours oral (1 minute) :**  
> *"En conclusion, TrustJob AI démontre qu'un pipeline NLP bien calibré couplé à un SVM linéaire permet de détecter plus de 83 % des fraudes tout en maintenant 98,4 % d'exactitude. Pour aller plus loin, nous envisageons d'intégrer des Transformers comme RoBERTa et d'interfacer l'outil avec des registres légaux d'entreprises comme le RNE. Nous vous remercions pour votre attention et nous sommes prêts à répondre à vos questions."*
