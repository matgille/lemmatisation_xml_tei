# Lemmatisation XML


Ce script permet l'annotation grammaticale d'une source XML conforme TEI tout en conservant l'encodage de celle-ci.

## Fonctionnement

`python3 lemmatisation.py fichier langue`

Seuls le latin et le castillan sont supportés pour le moment. 

## Projets similaires
Ce projet est fortement inspiré d'une partie du projet [Falcon](https://github.com/CondorCompPhil/falcon) qui vise déjà
 à lemmatiser en utilisant pie ou Freeling. 



## Crédits et réferences
Le modèle de lemmatisation présent sur le dépôt est celui entraîné par Thibault Clérice (ÉnC) sur les données du LASLA 
([ici](https://github.com/chartes/deucalion-model-lasla)):
*   Thibault Clérice. (2019, February 1). chartes/deucalion-model-lasla: LASLA Latin Lemmatizer - Alpha (Version 0.0.1). 
Zenodo. http://doi.org/10.5281/zenodo.2554847 _Check the latest version here:_[Zenodo DOI](https://doi.org/10.5281/zenodo.2554846)


## Licence

Sauf indication contraire, les fichiers sont publiés [sous licence NPOSL-3.0](https://opensource.org/licenses/NPOSL-3.0). 

Le modèle de lemmatisation `modele.tar` ainsi que la version de saxon présente sur le dépôt sont distribués sous licence [Mozilla Public License version 2.0](https://www.mozilla.org/en-US/MPL/2.0/).