"""Contrat de données du jeu Bank Marketing."""  # docstring : décrit le rôle du fichier

import pandera.pandas as pa  # pandera : librairie qui vérifie qu'un DataFrame respecte des règles

OUI_NON = ["yes", "no"]  # liste réutilisée pour toutes les colonnes oui/non

bank_schema = pa.DataFrameSchema(  # le schéma = l'ensemble des règles du contrat
    {
        "age": pa.Column(int, pa.Check.in_range(18, 100)),  # entier entre 18 et 100
        "job": pa.Column(str, pa.Check.isin([  # texte, forcément dans cette liste de métiers
            "admin.", "blue-collar", "entrepreneur", "housemaid",  # attention au point de "admin."
            "management", "retired", "self-employed", "services",  # tiret dans "self-employed"
            "student", "technician", "unemployed", "unknown",  # "unknown" est autorisé
        ])),
        "marital": pa.Column(str, pa.Check.isin(["married", "single", "divorced"])),  # situation familiale
        "education": pa.Column(str, pa.Check.isin(["primary", "secondary", "tertiary", "unknown"])),  # niveau d'études
        "default": pa.Column(str, pa.Check.isin(OUI_NON)),  # défaut de crédit : yes/no
        "balance": pa.Column(int),  # solde : entier, sans borne (peut être négatif)
        "housing": pa.Column(str, pa.Check.isin(OUI_NON)),  # prêt immobilier : yes/no
        "loan": pa.Column(str, pa.Check.isin(OUI_NON)),  # prêt personnel : yes/no
        "contact": pa.Column(str, pa.Check.isin(["cellular", "telephone", "unknown"])),  # moyen de contact
        "day": pa.Column(int, pa.Check.in_range(1, 31)),  # jour du mois : 1 à 31
        "month": pa.Column(str, pa.Check.isin([  # mois en abrégé anglais
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec",
        ])),
        "duration": pa.Column(int, pa.Check.ge(0)),  # durée de l'appel en secondes : >= 0
        "campaign": pa.Column(int, pa.Check.in_range(1, 100)),  # nb de contacts pendant la campagne : >= 1
        "pdays": pa.Column(int, pa.Check.ge(-1)),  # jours depuis le dernier contact : -1 = jamais contacté
        "previous": pa.Column(int, pa.Check.ge(0)),  # nb de contacts avant la campagne : >= 0
        "poutcome": pa.Column(str, pa.Check.isin(["success", "failure", "other", "unknown"])),  # résultat de la campagne précédente
        "y": pa.Column(str, pa.Check.isin(OUI_NON)),  # la cible : le client a souscrit ? yes/no
    },
    strict=True,  # aucune colonne en plus, aucune en moins
)


def validate_bank_data(df):  # fonction appelée par load.py et par les tests
    """Vérifie le contrat. Lève une erreur qui liste TOUS les problèmes."""
    return bank_schema.validate(df, lazy=True)  # lazy=True : vérifie tout le fichier, puis liste toutes les erreurs (SchemaErrors)