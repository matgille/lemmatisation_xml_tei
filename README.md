# Lemmatisation XML


Ce script permet l'annotation grammaticale d'une source XML conforme TEI tout en conservant l'encodage de celle-ci.


## Fonctionnement

`python3 lemmatisation.py fichier --langue`

Le latin médiéval (avec Pie), le latin classique (CLTK) et le castillan médiéval (Freeling) sont supportés pour le moment. 



## Test
Le script peut être testé à l'aide du fichier présent dans test/. Il s'agit d'une partie du *De Regimine Principum* (III,3), un texte latin médiéval (d'une édition de 
1605):
`python3 lemmatisation.py test/Rome_W.xml --latin-classique` 

## *Caveat*

La tokénisation est ici propre au castillan médiéval, et fonctionne avec le latin; pour d'autres langues, il faudra probablement 
écrire des règles différentes. En ce qui concerne les éléments à prendre en compte lors de cette tokénisation (tei:hi qui peuvent être à cheval sur un token par exemple, ou tei:pb), les règles portent
sur mon propre corpus et devront aussi être modifiées. Ces règles n'affectent pas le fonctionnement du script sur
un encodage purement structurel.

## Projets similaires
Ce projet est fortement inspiré du projet [Falcon](https://github.com/CondorCompPhil/falcon) (Jean-Baptiste Camps, Lucence Ing et Elena Spadini), notamment pour la possibilité
de lemmatiser avec plusieurs outils, freeling ou pie. 


## Remerciements, crédits et réferences
Merci à Jean-Baptiste Camps de m'avoir fait découvrir Freeling; merci à Thibault Clérice pour son aide sur pie. 

Le modèle de lemmatisation présent sur le dépôt est celui entraîné par Thibault Clérice (ÉnC) sur les données du LASLA
([ici](https://github.com/chartes/deucalion-model-lasla)):
*   Thibault Clérice. (2019, February 1). chartes/deucalion-model-lasla: LASLA Latin Lemmatizer - Alpha (Version 0.0.1). 
Zenodo. http://doi.org/10.5281/zenodo.2554847 _Check the latest version here:_[Zenodo DOI](https://doi.org/10.5281/zenodo.2554846)

Pour Freeling ([site](http://nlp.lsi.upc.edu/freeling/)): 
* Lluís Padró and Evgeny Stanilovsky. *FreeLing 3.0: Towards Wider Multilinguality*. Proceedings of the Language Resources and Evaluation Conference (LREC 2012) ELRA. Istanbul, Turkey. May, 2012.

Pour CLTK: 
* Kyle P. Johnson et al.. (2014-2019). CLTK: The Classical Language Toolkit. DOI 10.5281/zenodo.<v0.1.111>


## Licence

Sauf indication contraire, les fichiers sont publiés [sous licence NPOSL-3.0](https://opensource.org/licenses/NPOSL-3.0). 

Le modèle de lemmatisation `modele.tar` ainsi que la version de saxon présente sur le dépôt sont distribués sous licence
 [Mozilla Public License version 2.0](https://www.mozilla.org/en-US/MPL/2.0/).
