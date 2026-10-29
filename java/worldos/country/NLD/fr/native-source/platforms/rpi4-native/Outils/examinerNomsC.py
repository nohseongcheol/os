#!/usr/bin/env python3
"""libclang Déclarations·référence 위치를 수집한다. valeurExtérieur 헤더의 멤버는 변환하지 않는다."""
import ctypes as sourceC
import hashlib
import json
from pathlib import Path

racineProjet = Path(__file__).resolve().parents[1]
réalisation = sourceC.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class Chaîne(sourceC.Structure): _fields_ = [('Données',sourceC.c_void_p),('afficherValeur',sourceC.c_uint)]
class valeurCurseur(sourceC.Structure): _fields_ = [('valeurGenre',sourceC.c_uint),('valeurAuxiliaire',sourceC.c_int),('Données',sourceC.c_void_p*3)]
class position(sourceC.Structure): _fields_ = [('Données',sourceC.c_void_p*2),('valeurDécalage',sourceC.c_uint)]
def Fonction(nom, résultatRetourner, *arguments):
    valeurEntréeÉlément = getattr(réalisation, nom); valeurEntréeÉlément.restype = résultatRetourner; valeurEntréeÉlément.argtypes = list(arguments); return valeurEntréeÉlément
obtenirTexte = Fonction('clang_getCString',sourceC.c_char_p,Chaîne)
libérerTexte = Fonction('clang_disposeString',None,Chaîne)
def texte(valeur):
    résultat = (obtenirTexte(valeur) or b'').decode('utf-8'); libérerTexte(valeur); return résultat
obtenirNom = Fonction('clang_getCursorSpelling',Chaîne,valeurCurseur)
obtenirRéférence = Fonction('clang_getCursorReferenced',valeurCurseur,valeurCurseur)
obtenirPosition = Fonction('clang_getCursorLocation',position,valeurCurseur)
positionFichier = Fonction('clang_getFileLocation',None,position,sourceC.POINTER(sourceC.c_void_p),sourceC.POINTER(sourceC.c_uint),sourceC.POINTER(sourceC.c_uint),sourceC.POINTER(sourceC.c_uint))
nomEntréeÉlémentFichier = Fonction('clang_getFileName',Chaîne,sourceC.c_void_p)
nomUnique = Fonction('clang_getCursorUSR',Chaîne,valeurCurseur)
genreConnexion = Fonction('clang_getCursorLinkage',sourceC.c_uint,valeurCurseur)
typeVisité = sourceC.CFUNCTYPE(sourceC.c_uint,valeurCurseur,valeurCurseur,sourceC.c_void_p)
visiterValeur = Fonction('clang_visitChildren',sourceC.c_uint,valeurCurseur,typeVisité,sourceC.c_void_p)
générer = Fonction('clang_createIndex',sourceC.c_void_p,sourceC.c_int,sourceC.c_int)
examinerValeur = Fonction('clang_parseTranslationUnit',sourceC.c_void_p,sourceC.c_void_p,sourceC.c_char_p,sourceC.POINTER(sourceC.c_char_p),sourceC.c_int,sourceC.c_void_p,sourceC.c_uint,sourceC.c_uint)
valeurRacine = Fonction('clang_getTranslationUnitCursor',valeurCurseur,sourceC.c_void_p)
programmeTerminerSession = Fonction('clang_disposeTranslationUnit',None,sourceC.c_void_p)
nombreÉlémentsDiagnostic = Fonction('clang_getNumDiagnostics',sourceC.c_uint,sourceC.c_void_p)
obtenirDiagnostic = Fonction('clang_getDiagnostic',sourceC.c_void_p,sourceC.c_void_p,sourceC.c_uint)
valeurGravité = Fonction('clang_getDiagnosticSeverity',sourceC.c_uint,sourceC.c_void_p)
messageDiagnostic = Fonction('clang_getDiagnosticSpelling',Chaîne,sourceC.c_void_p)
libérerDiagnostic = Fonction('clang_disposeDiagnostic',None,sourceC.c_void_p)

def indicePosition(valeurEntréeÉlément):
    Fichier = sourceC.c_void_p(); ligne = sourceC.c_uint(); entréeÉlémentEmplacement = sourceC.c_uint(); valeurDécalage = sourceC.c_uint()
    positionFichier(obtenirPosition(valeurEntréeÉlément),sourceC.byref(Fichier),sourceC.byref(ligne),sourceC.byref(entréeÉlémentEmplacement),sourceC.byref(valeurDécalage))
    return (texte(nomEntréeÉlémentFichier(Fichier)) if Fichier else '', valeurDécalage.value, ligne.value)

def exécuterCommande():
    indiceRechercher = générer(0,0); listeDéclarations = {}; listeRéférences = []; erreurs = []
    # outilCompilateur.c는 interne Déclarations 없이 TinyCC valeurExtérieur 단일 traduireSource 단위만 포함한다.
    # valeurExtérieur 선언을 interne 이름으로 세지 않으며, donnéesEffectif 빌드에서는 traitementContinuer 컴파일한다.
    fichierPossédé = {str(chemin.resolve()) for chemin in racineProjet.rglob('*') if chemin.suffix in ('.c','.h','.cpp','.inc')
              and not set(chemin.relative_to(racineProjet).parts)&{'build','dist','vendor','__pycache__'}
              and chemin.relative_to(racineProjet).as_posix() != 'CompilateurC/outilCompilateur.c'}
    valeurCommun = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(racineProjet/'Utilisateur'),
          '-I'+str(racineProjet.parents[1]/'posix-kor/arm64-native/Entêtes'),'-I'+str(racineProjet/'build'),'-I'+str(racineProjet/'build/user'),
          '-I'+str(racineProjet/'build/remote'),'-I'+str(racineProjet/'vendor/bearssl/inc'),
          '-I'+str(racineProjet/'vendor/bearssl/src'),'-I'+str(racineProjet/'vendor/libassh/src'),
          '-I'+str(racineProjet/'vendor/lwip/src/include'),'-I'+str(racineProjet/'PileRéseau'),
          '-I'+str(racineProjet/'valeurDistant'),'-I'+str(racineProjet/'CompilateurC')]
    for chemin in sorted(Path(nom) for nom in fichierPossédé if nom.endswith(('.c','.cpp'))):
        arguments = valeurCommun + ['-std=c++11' if chemin.suffix=='.cpp' else '-std=c11']
        if 'PileRéseau' in chemin.parts: arguments += ['-I'+str(racineProjet/'PileRéseau'),'-I'+str(racineProjet/'vendor/lwip/src/include')]
        if 'CompilateurC' in chemin.parts:
            arguments += ['-I'+str(racineProjet/'CompilateurC'),'-I'+str(racineProjet/'vendor/tinycc'),'-I'+str(racineProjet/'build/ccompiler'),
                    '-isystem',str(racineProjet.parent/'rpi4/build/rootfs/usr/include')]
        if 'pontPython' in chemin.parts:
            arguments += ['-I'+str(racineProjet/'pontPython'),'-I'+str(racineProjet/'build/micropython-1.24.1'),'-I'+str(racineProjet/'build/python'),'-isystem','/usr/include/newlib']
        if 'valeurDistant' in chemin.parts:
            arguments += ['-isystem', '/usr/include/newlib']
        if 'valeurDistribution' in chemin.parts: arguments += ['-D__JKOROS__=1']
        if chemin.name=='Paquet.c': arguments += ['-I'+str(racineProjet/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        valeurGroupe = (sourceC.c_char_p*len(arguments))(*[valeurEntréeÉlément.encode() for valeurEntréeÉlément in arguments])
        unitéTraduction = examinerValeur(indiceRechercher,str(chemin).encode(),valeurGroupe,len(arguments),None,0,1)
        for numéro in range(nombreÉlémentsDiagnostic(unitéTraduction)):
            valeurDiagnostic = obtenirDiagnostic(unitéTraduction,numéro)
            if valeurGravité(valeurDiagnostic)>=3: erreurs.append((str(chemin.relative_to(racineProjet)),texte(messageDiagnostic(valeurDiagnostic))))
            libérerDiagnostic(valeurDiagnostic)
        @typeVisité
        def inspecterValeur(valeurEntréeÉlément,valeurParent,Données):
            Fichier,valeurDécalage,ligne = indicePosition(valeurEntréeÉlément)
            if Fichier not in fichierPossédé: return 2 if valeurEntréeÉlément.valeurGenre==300 else 1
            motLexical = texte(obtenirNom(valeurEntréeÉlément))
            if not motLexical or any(ord(valeurCaractère)>127 for valeurCaractère in motLexical): return 2
            if valeurEntréeÉlément.valeurGenre in (2,3,4,5,6,7,8,9,10,20,21,501):
                valeurUnique = texte(nomUnique(valeurEntréeÉlément)) or Fichier+':'+str(valeurDécalage)
                listeDéclarations[valeurUnique] = {'Fichier':Fichier,'valeurDécalage':valeurDécalage,'ligne':ligne,'valeurGenre':valeurEntréeÉlément.valeurGenre,'nom':motLexical,'connecter':genreConnexion(valeurEntréeÉlément)}
                listeRéférences.append((Fichier,valeurDécalage,motLexical,valeurUnique))
            else:
                référence = obtenirRéférence(valeurEntréeÉlément)
                fichierRéférence,_,_ = indicePosition(référence)
                if fichierRéférence in fichierPossédé:
                    valeurUnique = texte(nomUnique(référence)); listeRéférences.append((Fichier,valeurDécalage,texte(obtenirNom(référence)),valeurUnique))
            return 2
        visiterValeur(valeurRacine(unitéTraduction),inspecterValeur,None)
        programmeTerminerSession(unitéTraduction)
    valeurDestination = racineProjet/'build/한국어화/시언어분석.json'
    valeurDestination.parent.mkdir(parents=True, exist_ok=True)
    listeHachages = {Fichier:hashlib.sha256(Path(Fichier).read_bytes()).hexdigest() for Fichier in sorted(fichierPossédé)}
    valeurDestination.write_text(json.dumps({'Déclarations':listeDéclarations,'référence':listeRéférences,'erreur':erreurs,'원문해시':listeHachages},ensure_ascii=False,indent=2)+'\n')
    print('Déclarations',len(listeDéclarations),'référence',len(listeRéférences),'erreur',len(erreurs))
    for erreur in erreurs: print(*erreur)

if __name__=='__main__': exécuterCommande()
