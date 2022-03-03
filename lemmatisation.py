import subprocess
import sys
import string
import re
import random

from lxml import etree
import xml.etree.ElementTree as ET
import os
import tqdm


def principal(fichier, argument):
    nom_fichier = os.path.basename(fichier)
    moteur_xslt = "saxon9he.jar"
    if argument == "latin":
        langue = "latin"
    else:
        langue = "castillan"
    tokenisation(moteur_xslt, nom_fichier)
    lemmatisation(nom_fichier, moteur_xslt, langue)


def tokenisation(moteur_xslt, nom_fichier):
    """
    La régularisation signifie la suppression des noeuds non textuels à l'intérieur des tei:w (pb, cb, etc)
    et l'impression des noeuds textuels à l'intérieurs d'éléments (hi, etc)
    :param moteur_xslt: chemin vers saxon
    :param nom_fichier: le nom du fichier seul.
    :return: un fichier régularisé document.xml tokénisé et le fichier original tokénisé.
    """
    print("Tokénisation et régularisation du fichier...")
    param = "nom_fichier=%s" % nom_fichier
    subprocess.run(["java", "-jar", moteur_xslt, "-xi:on", fichier,
                    "xsl/tokenisation.xsl", param])
    fichier_tokenise = "fichier_tokenise/%s" % nom_fichier
    print("Tokénisation réussie.")
    ajout_xml_id(fichier_tokenise)
    subprocess.run(["java", "-jar", moteur_xslt, "-xi:on", fichier_tokenise,
                    "xsl/regularisation.xsl"])
    print("Régularisation réussie")


def generateur_lettre_initiale(size=1, chars=string.ascii_lowercase):  # éviter les nombres en premier caractère de
    # l'@xml:id (interdit)
    return ''.join(random.choice(chars) for _ in range(size))


def generateur_id(size=6, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return generateur_lettre_initiale() + ''.join(random.choice(chars) for _ in range(size))


def ajout_xml_id(fichier):
    """
    Création des xml:id pour chaque token.
    :param fichier_entree: le fichier à xmlidiser
    :return: un fichier où chaque token a un @xml:id
    """
    tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
    f = etree.parse(fichier)
    root = f.getroot()
    tokens = root.xpath("//tei:w", namespaces=tei)
    for w in tokens:
        w.set("{http://www.w3.org/XML/1998/namespace}id", generateur_id())
    sortie_xml = open(fichier, "w+")
    string = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf8')
    sortie_xml.write(str(string))
    sortie_xml.close()


def lemmatisation(fichier, moteur_xslt, langue):
    """
    Lemmatisation du fichier XML et réinjection dans le document xml originel.
    :param fichier: le fichier à lemmatiser
    :param moteur_xslt: le moteur de transformation à utiliser
    :param langue: la langue du fichier
    :return: retourne un fichier lemmatisé
    """
    fichier_sans_extension = os.path.splitext(fichier)[0]
    fichier_xsl = "xsl/transformation_pre_lemmatisation.xsl"
    chemin_vers_fichier = "fichier_tokenise_regularise/" + str(fichier)
    fichier_entree_txt = 'fichier_tokenise_regularise/txt/' + fichier_sans_extension + '.txt'
    param_sortie = "sortie=" + fichier_entree_txt
    subprocess.run(["java", "-jar", moteur_xslt, chemin_vers_fichier, fichier_xsl, param_sortie])
    print("Tokénisation et régularisation du fichier ✓\nLemmatisation...")
    if langue == "castillan":
        fichier_lemmatise = 'fichier_tokenise_regularise/txt/' + fichier_sans_extension + '_lemmatise' + '.txt'
        cmd_sh = ["sh", "analyze.sh", fichier_entree_txt,
                  fichier_lemmatise]  # je dois passer par un script externe car un subprocess tourne dans le vide,
        # pas trouvé pourquoi
        subprocess.run(cmd_sh)  # analyze est dans /usr/bin
        maliste = txt_to_liste(fichier_lemmatise)
        parser = etree.XMLParser(load_dtd=True,
                                 resolve_entities=True)  # inutile car les entités ont déjà été résolues
        # auparavant normalement, mais au cas où.
        fichier_tokenise = "fichier_tokenise_regularise/" + fichier
        f = etree.parse(fichier_tokenise, parser=parser)
        root = f.getroot()
        tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
        groupe_words = "//tei:w"
        tokens = root.xpath(groupe_words, namespaces=tei)
        fichier_lemmatise = fichier_tokenise
        n = 1
        for mot in tokens:
            nombre_mots_precedents = int(mot.xpath("count(preceding::tei:w) + 1", namespaces=tei))
            nombre_ponctuation_precedente = int(mot.xpath("count(preceding::tei:pc) + 1", namespaces=tei))
            position_absolue_element = nombre_mots_precedents + nombre_ponctuation_precedente  # attention à
            liste_correcte = maliste[position_absolue_element - 2]  # Ça marche bien si la lemmatisation se fait
            # sans retokenisation. Pour l'instant, ça bloque avec les chiffre (ochenta mill est fusionné). Voir
            # avec les devs de Freeling.
            n += 1
            try:
                lemme_position = liste_correcte[1]
                pos_position = liste_correcte[2]
            except:
                print("Index error")
                print(liste_correcte)
                print(f"Position: {n}")
                exit(0)
            mot.set("lemma", lemme_position)
            mot.set("pos", pos_position)

    elif langue == "latin":
        modele_latin = "model.tar"
        device = "cuda:0"
        batch_size = 32
        cmd = f"pie tag --device {device} --batch_size {batch_size} <{modele_latin},lemma,pos,Person,Numb,Tense,Case,Mood> {fichier_entree_txt}"
        # subprocess.run(cmd.split())
        print("Lemmatisation du fichier ✓")
        fichier_seul = os.path.splitext(fichier_entree_txt)[0]
        fichier_lemmatise = f"{fichier_seul}-pie.txt"
        liste_lemmatisee = txt_to_liste(fichier_lemmatise)
        # Nettoyage de la liste
        liste_lemmatisee.pop(0)  # on supprime les titres de colonnes

        parser = etree.XMLParser(load_dtd=True,
                                 resolve_entities=True)  # inutile car les entités ont déjà été résolues
        # auparavant normalement, mais au cas où.
        fichier_tokenise = "fichier_tokenise/" + fichier
        f = etree.parse(fichier_tokenise, parser=parser)
        root = f.getroot()
        tei = {'tei': 'http://www.tei-c.org/ns/1.0'}
        groupe_words = "//tei:w"
        tokens = root.xpath(groupe_words, namespaces=tei)
        puncts_and_tokens = [element.tag.replace("{http://www.tei-c.org/ns/1.0}", "") for element
                             in root.xpath('//node()[self::tei:pc or self::tei:w]', namespaces=tei)]

        number_of_previous_items_per_w = []
        n = 0
        # On va indiquer pour chaque index le nombre de ponctuation précédent.
        # Permet de gagner beaucoup de temps en n'utilisant pas lxml
        for index, word_type in enumerate(puncts_and_tokens):
            if word_type == 'pc':
                pass
            else:
                number_of_previous_items_per_w.append(index)

        fichier_lemmatise = fichier_tokenise
        for index, mot in enumerate(tqdm.tqdm(tokens)):
            position_absolue_element = number_of_previous_items_per_w[index]
            try:
                liste_correcte = liste_lemmatisee[position_absolue_element]
            except IndexError as e:
                print("Error")
                print(position_absolue_element)
                exit(0)
            cas, mode, number, person, temps, lemme, pos = liste_correcte[1], liste_correcte[2], liste_correcte[3], liste_correcte[4], liste_correcte[5], liste_correcte[6], liste_correcte[7]
            # on nettoie la morphologie pour supprimer les entrées vides
            morph = "CAS=%s|MODE=%s|NOMB.=%s|PERS.=%s|TEMPS=%s" % (cas, mode, number, person, temps)
            morph = re.sub("((?!\|).)*?_(?=\|)", "", morph)  # on supprime les traits non renseignés du milieu
            morph = re.sub("^\|*", "", morph)  # on supprime les pipes qui commencent la valeur
            morph = re.sub("(\|)+", "|", morph)  # on supprime les pipes suivis
            morph = re.sub("\|((?!\|).)*?_$", "", morph)  # on supprime les traits non renseignés de fin
            morph = re.sub("(?!\|).*_(?!\|)", "", morph)  # on supprime les traits non renseignés uniques
            mot.set("lemma", lemme)
            mot.set("pos", pos)
            if morph:
                mot.set("morph", morph)

    with open(fichier_lemmatise, "w+") as sortie_xml:
        print(fichier_lemmatise)
        a_ecrire = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True).decode(
            'utf8')
        print("Saving file.")
        sortie_xml.write(str(a_ecrire))


def txt_to_liste(filename):
    """
    Transforme le fichier txt produit par Freeling ou pie en liste de listes pour processage ultérieur.
    :param filename: le nom du fichier txt à transformer
    :return: une liste de listes: pour chaque forme, les différentes analyses
    """
    maliste = []
    fichier = open(filename, 'r')
    for line in fichier.readlines():
        if not re.match(r'^\s*$',
                        line):  # https://stackoverflow.com/a/3711884 élimination des lignes vides (séparateur de phrase)
            resultat = re.split(r'\s+', line)
            maliste.append(resultat)
    return maliste



def clear():
    os.system('clear')


if __name__ == "__main__":
    fichier = sys.argv[1]
    langue = sys.argv[2]
    principal(fichier, langue)
