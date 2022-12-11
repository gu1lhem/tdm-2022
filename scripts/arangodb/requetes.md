oc# Point de vue Utilisateur standard
    1. Les dix villes où il y a le plus d'inscrits
    ```aql
    FOR c in communes SORT c.inscrits DESC LIMIT 10 RETURN c
    ```
    2. Quel score a fait Emmanuel Macron à Paris
    ```aql
    FOR c IN communes
        FILTER c.libelle_commune == "Paris"
        FOR e IN elit
            FILTER e._from == c._id
            FILTER e._to == "candidats/EM"
            RETURN e.score
    ```
    3. Pour chaque candidat, la ville où il a fait le meilleur résultat
    ```aql
    FOR candidat IN candidats
    LET best = (
        FOR commune IN communes
            LET score = (
                FOR edge IN elit
                    FILTER edge._from == commune._id
                    FILTER edge._to == candidat._id
                    RETURN edge.score
            )[0]
            RETURN {commune: commune, score: score}
    )
    LET best_commune = (
        FOR commune IN best
            FILTER commune.score == MAX(best[*].score)
            RETURN commune.commune
    )[0]
    RETURN {candidat: candidat.full_name, meilleur_resultat: best_commune.libelle_commune}
    ```
    candidat 	meilleur_resultat
    Emmanuel Macron 	Bigorno
    Marine Le Pen 	Brachay
    Nicolas Dupont-Aignan 	Baulny
    Jean-Luc Mélenchon 	Quirbajou
    Francois Fillon 	Guargualé
    Benoît Hamon 	Hienghène
    Nathalie Arthaud 	Rainfreville
    Philippe Poutou 	Lichans-Sunhar
    Francois Asselineau 	Sougraigne
    Jacques Cheminade 	Escots
    Jean Lassalle 	Lourdios-Ichère
    4. Les résultats des communes dans laquelle l'abstention est supérieure à 50%
    ```aql
    FOR commune IN communes
    FILTER commune.abstentions > 50
    LET results = (
        FOR edge IN elit
            FILTER edge._from == commune._id
            LET candidat = DOCUMENT(edge._to)
            RETURN {candidat: candidat.full_name, score: edge.score}
    )
    RETURN {commune: commune.libelle_commune, results: results}
    ```
# Point de vue Analyste de données
    1. Obtenir les gagnants dans chaque département
    2. Transformer le pourcentage exprimés pour chaque candidat par rappoort aux nombres d'inscrits et non plus d'exprimés
