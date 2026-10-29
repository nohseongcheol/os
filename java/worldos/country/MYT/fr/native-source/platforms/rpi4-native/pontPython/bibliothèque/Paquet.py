"""interne 커널용 제한형 pip. PyPI의 작은 순수 Python 소스를 Hôte 중계로 설치한다."""
import sys
import json
import hashlib
import gc
import jkoros as SystèmeExploitation

cheminListe = "/lib/.pip.json"


def valeurEmpreinte(Données):
    return "".join("%02x" % valeur for valeur in hashlib.sha256(Données).digest())


def lireListe():
    if SystèmeExploitation.path_kind(cheminListe) == 0:
        return {}
    return json.loads(SystèmeExploitation.read(cheminListe).decode("utf-8"))


def écrireJournal(chemin, Données):
    if SystèmeExploitation.write(chemin, Données) != len(Données):
        raise OSError(28)


def contrôlerChemin(chemin):
    if not isinstance(chemin, str) or not chemin.endswith(".py"):
        raise ValueError("Python 소스만 설치할 nombre 있습니다.")
    if any(valeurSousPartie in ("", ".", "..") or valeurSousPartie.startswith(".") for valeurSousPartie in chemin.split("/")):
        raise ValueError("허용하지 않는 Paquet chemin")
    if "\\" in chemin or any(ord(valeurCaractère) < 32 or ord(valeurCaractère) == 127 for valeurCaractère in chemin):
        raise ValueError("잘못된 chemin Caractères")
    résultat = "/lib/" + chemin
    if len(résultat.encode("utf-8")) > 63 or chemin in ("français.py", "Paquet.py"):
        raise ValueError("Paquet 경로가 너무 길거나 valeurDéfaut 라이브러리와 겹칩니다.")
    return résultat


class recevoirFlux:
    def __init__(valeurSoi, extrémité):
        valeurSoi.extrémité = extrémité
        valeurSoi.donnéesRestant = b""
        valeurSoi.lancer = SystèmeExploitation.ticks_ms()

    def lireExactement(valeurSoi, longueur):
        Données = bytearray()
        while len(Données) < longueur:
            if SystèmeExploitation.ticks_ms() - valeurSoi.lancer > 90000:
                raise ValueError("Paquet relayerValeur réponse valeurTemps 초과")
            if not valeurSoi.donnéesRestant:
                try:
                    valeurSoi.donnéesRestant = SystèmeExploitation.tcp_read(valeurSoi.extrémité, 512)
                except OSError as erreur:
                    if erreur.args[0] != 11:
                        raise
                    SystèmeExploitation.sleep_ms(10)
                    continue
                if not valeurSoi.donnéesRestant:
                    raise ValueError("Paquet 전송이 중간에 끝났습니다.")
            nombreÉlémentsÉlémentListe = min(longueur - len(Données), len(valeurSoi.donnéesRestant))
            Données.extend(valeurSoi.donnéesRestant[:nombreÉlémentsÉlémentListe])
            valeurSoi.donnéesRestant = valeurSoi.donnéesRestant[nombreÉlémentsÉlémentListe:]
            SystèmeExploitation.sleep_ms(0)
        return bytes(Données)


def télécharger(requête, numéroPort):
    if len(requête) > 96 or any(valeurCaractère not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-=" for valeurCaractère in requête):
        raise ValueError("사용법: pip install nom 또는 nom==버전")
    extrémité = SystèmeExploitation.tcp_open()
    try:
        lancer = SystèmeExploitation.ticks_ms()
        while True:
            try:
                SystèmeExploitation.tcp_connect(extrémité, "10.0.2.2", numéroPort)
                break
            except OSError as erreur:
                if erreur.args[0] not in (11, 115) or SystèmeExploitation.ticks_ms() - lancer > 5000:
                    raise ValueError("Paquet relayerValeur connecter valeurÉchec: 호스트에서 --network --pip로 실행하십시오.")
                SystèmeExploitation.sleep_ms(10)
        Données = (requête + "\n").encode()
        while Données:
            try:
                nombreÉlémentsÉlémentListe = SystèmeExploitation.tcp_write(extrémité, Données)
                if not nombreÉlémentsÉlémentListe:
                    raise ValueError("Paquet requête valeurTransfert valeurÉchec")
                Données = Données[nombreÉlémentsÉlémentListe:]
            except OSError as erreur:
                if erreur.args[0] != 11:
                    raise
                SystèmeExploitation.sleep_ms(10)
                if SystèmeExploitation.ticks_ms() - lancer > 10000:
                    raise ValueError("Paquet requête valeurTransfert valeurTemps 초과")
        valeurFlux = recevoirFlux(extrémité)
        valeurTête = valeurFlux.lireExactement(8)
        if valeurTête[:4] != b"JKP1":
            raise ValueError("Paquet valeurTransfert valeurContrat 불일치")
        longueur = (valeurTête[4] << 24) | (valeurTête[5] << 16) | (valeurTête[6] << 8) | valeurTête[7]
        if longueur > 8192:
            raise ValueError("Paquet 명세가 너무 큽니다.")
        spécification = json.loads(valeurFlux.lireExactement(longueur).decode())
        if "error" in spécification:
            raise ValueError(spécification["error"])
        if not 1 <= len(spécification["files"]) <= 16:
            raise ValueError("꾸러미당 arbreSource 파일은 1~16개여야 합니다.")
        if sum(valeurEntréeÉlément["size"] for valeurEntréeÉlément in spécification["files"]) > 65536:
            raise ValueError("Paquet arbreSource 합계는 64 KiB 이하여야 합니다.")
        entréesListeFichier = {}
        for valeurEntréeÉlément in spécification["files"]:
            chemin = contrôlerChemin(valeurEntréeÉlément["path"])
            if chemin in entréesListeFichier or not 0 <= valeurEntréeÉlément["size"] <= 16384:
                raise ValueError("중복 chemin 또는 Fichier taille 초과")
            Données = valeurFlux.lireExactement(valeurEntréeÉlément["size"])
            if valeurEmpreinte(Données) != valeurEntréeÉlément["sha256"]:
                raise ValueError("Paquet Fichier SHA-256 불일치")
            # 실행하지 않고 élémentListeActuel MicroPython의 문법으로 먼저 검사한다.
            compile(Données.decode("utf-8"), chemin, "exec")
            entréesListeFichier[chemin] = Données
            gc.collect()
        return spécification, entréesListeFichier
    finally:
        SystèmeExploitation.udp_close(extrémité)


def installerValeur(requête, numéroPort):
    print("Paquet télécharger:", requête)
    spécification, entréesListeFichier = télécharger(requête, numéroPort)
    listeEntréeÉlément = lireListe()
    nom = spécification["name"]
    if nom in listeEntréeÉlément:
        if listeEntréeÉlément[nom]["version"] == spécification["version"]:
            for chemin, donnéesEmpreinte in listeEntréeÉlément[nom]["files"].items():
                if SystèmeExploitation.path_kind(chemin) != 1 or valeurEmpreinte(SystèmeExploitation.read(chemin)) != donnéesEmpreinte:
                    raise ValueError("설치된 Paquet 파일이 달라졌습니다: " + chemin)
            print("이미 설치됨:", nom, spécification["version"])
            return
        raise ValueError("다른 버전이 있습니다. pip uninstall로 제거한 valeurRetourArrièreCôté 설치하십시오.")
    for chemin in entréesListeFichier:
        if SystèmeExploitation.path_kind(chemin):
            raise ValueError("기존 파일을 덮어쓰지 않습니다: " + chemin)
    listeEntréeÉlément[nom] = {"version": spécification["version"], "files": {chemin: valeurEmpreinte(Données) for chemin, Données in entréesListeFichier.items()}}
    listeNouveau = json.dumps(listeEntréeÉlément).encode()
    if len(listeNouveau) > 16384:
        raise ValueError("Paquet listeEntréeÉlément taille 초과")
    listePrécédentÉlément = SystèmeExploitation.read(cheminListe) if SystèmeExploitation.path_kind(cheminListe) else None
    fichierCréé = []
    répertoireCréé = []
    try:
        for chemin, Données in entréesListeFichier.items():
            parties = chemin.split("/")
            for nombre in range(2, len(parties)):
                valeurRépertoire = "/".join(parties[:nombre])
                valeurGenre = SystèmeExploitation.path_kind(valeurRépertoire)
                if valeurGenre == 0:
                    SystèmeExploitation.mkdir(valeurRépertoire)
                    répertoireCréé.append(valeurRépertoire)
                elif valeurGenre != 2:
                    raise ValueError("valeurRépertoire 경로에 파일이 있습니다: " + valeurRépertoire)
            fichierCréé.append(chemin)
            écrireJournal(chemin, Données)
        écrireJournal(cheminListe, listeNouveau)
    except Exception:
        for chemin in fichierCréé:
            if SystèmeExploitation.path_kind(chemin):
                SystèmeExploitation.remove(chemin)
        for valeurRépertoire in reversed(répertoireCréé):
            SystèmeExploitation.rmdir(valeurRépertoire)
        if listePrécédentÉlément is not None:
            écrireJournal(cheminListe, listePrécédentÉlément)
        elif SystèmeExploitation.path_kind(cheminListe):
            SystèmeExploitation.remove(cheminListe)
        raise
    print("installerValeur estTerminé:", nom, spécification["version"], "→ /lib (RAM)")


def supprimerEntréeÉlément(nom):
    listeEntréeÉlément = lireListe()
    if nom not in listeEntréeÉlément:
        raise ValueError("설치되지 않은 꾸러미입니다: " + nom)
    for chemin, donnéesEmpreinte in listeEntréeÉlément[nom]["files"].items():
        if SystèmeExploitation.path_kind(chemin) != 1 or valeurEmpreinte(SystèmeExploitation.read(chemin)) != donnéesEmpreinte:
            raise ValueError("사용자가 바꾼 파일을 보존합니다: " + chemin)
    for chemin in listeEntréeÉlément[nom]["files"]:
        SystèmeExploitation.remove(chemin)
    del listeEntréeÉlément[nom]
    écrireJournal(cheminListe, json.dumps(listeEntréeÉlément).encode())
    print("supprimerEntréeÉlément estTerminé:", nom)


def lancer(arguments):
    numéroPort = 8027
    if len(arguments) >= 2 and arguments[-2] == "--port":
        numéroPort = int(arguments[-1])
        arguments = arguments[:-2]
    if arguments == ["list"]:
        for nom, informationSystème in lireListe().items():
            print(nom, informationSystème["version"])
    elif len(arguments) == 2 and arguments[0] == "install":
        installerValeur(arguments[1], numéroPort)
    elif len(arguments) == 2 and arguments[0] == "uninstall":
        supprimerEntréeÉlément(arguments[1])
    elif not arguments or arguments in (["--help"], ["--version"]):
        print("jkoros pip 1 / MicroPython arbreSource 설치기 (PyPA pip 전체가 아님)")
        print("pip install nom[==버전] [--port 8027] | pip list | pip uninstall nom")
        print("Hôte: Outils/exécuterCommande.py --network --pip; /lib는 재부팅 때 사라지는 RAM입니다.")
    else:
        raise ValueError("pip --help로 사용법을 확인하십시오.")


if __name__ == "__main__":
    try:
        lancer(sys.argv[1:])
    except Exception as erreur:
        print("Paquet erreur:", erreur)
        sys.exit(1)
