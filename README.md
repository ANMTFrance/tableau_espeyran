# tableau_espeyran
Ce script Python prépare le tableau sous le format demandé par le Centre national du microfilm et de la numérisation d'Espeyran, dans le cadre des sauvegardes régulières. Il croise un export des entrées Ligeo Gestion et l'arborescence de nos fichiers numérisés.

Il se base sur un export CSV Ligeo Gestion depuis Collecter / Entrées avec les colonnes suivantes :
- identifiant
- Serie
- Sous-serie
- Libelle
Cette configuration est modifiable directement dans le code.

Le résultat produit est un fichier CSV séparateur ";", UTF-8, texte entre guillemets avec les colonnes suivantes :
- noms des dossiers
- détail
- nombre de dossiers
- nombre de fichiers
- poids total (Mo)
- extensions
