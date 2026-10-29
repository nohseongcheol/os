"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from construireBibliothèqueJava import créerBibliothèqueJava


def créerRecueilExemples(cheminRacine, cheminDépôt, exécuterCommande):
    donnéesOriginal=cheminDépôt/'example';donnéesRésultat=cheminRacine/'build/examples';donnéesRésultat.mkdir(parents=True,exist_ok=True)
    cheminClasse=donnéesRésultat/'classes';cheminClasse.mkdir(exist_ok=True)
    créerBibliothèqueJava(cheminRacine,exécuterCommande)
    ip_settings = read_config(cheminRacine)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = donnéesRésultat/'java-source'; java_sources.mkdir(exist_ok=True)
    exécuterJava=[]
    for path in sorted((donnéesOriginal/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); exécuterJava.append(target)
    exécuterCommande(['javac','--release','8','-encoding','UTF-8','-cp',cheminRacine/'build/java-library/classes','-d',cheminClasse]+exécuterJava)
    séquenceInstructionMachine=['public final class LotExemple { public static int installerValeur(int Langue) { int valeurTraité;',
          'valeurTraité=InterpréteurCommandes.répertoireExemple("/example"); if(valeurTraité<0)return valeurTraité;']
    manifesteLot={}
    lisezMoi=guest_bytes(donnéesOriginal/'README.md')
    if len(lisezMoi)>16384: raise ValueError('example README exceeds native VFS limit')
    séquenceInstructionMachine.append('valeurTraité=InterpréteurCommandes.fichierExemple("/example/README.md","%s"); if(valeurTraité<0)return valeurTraité;'%lisezMoi.hex())
    manifesteLot['/example/README.md']={'bytes':len(lisezMoi),'sha256':hashlib.sha256(lisezMoi).hexdigest()}
    séquenceInstructionMachine.append('if(Langue==0){valeurTraité=InterpréteurCommandes.répertoireExemple("/lib"); if(valeurTraité<0)return valeurTraité;')
    for chemin in [donnéesOriginal/'python/français.py'] + sorted((cheminRacine/'pontPython/bibliothèque').glob('*.py')):
        valeurContenuValeur=guest_bytes(chemin);valeurCible='/lib/'+chemin.name
        if len(valeurContenuValeur)>16384 or len(valeurCible.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+valeurCible)
        séquenceInstructionMachine.append('valeurTraité=InterpréteurCommandes.fichierExemple(%s,"%s"); if(valeurTraité<0)return valeurTraité;'%(json.dumps(valeurCible,ensure_ascii=True),valeurContenuValeur.hex()))
        manifesteLot[valeurCible]={'bytes':len(valeurContenuValeur),'sha256':hashlib.sha256(valeurContenuValeur).hexdigest()}
    séquenceInstructionMachine.append('}')
    for indiceRechercher,Langue in enumerate(('java','c','python')):
        listeFichier=[(positionDonnées.name,positionDonnées) for positionDonnées in sorted((donnéesOriginal/Langue).iterdir()) if positionDonnées.is_file()]
        if Langue=='java':listeFichier += [(positionDonnées.stem+'.class',cheminClasse/(positionDonnées.stem+'.class')) for positionDonnées in exécuterJava]
        séquenceInstructionMachine += ['if(Langue==%d){'%indiceRechercher,'valeurTraité=InterpréteurCommandes.répertoireExemple("/example/%s"); if(valeurTraité<0)return valeurTraité;'%Langue]
        for nom,chemin in listeFichier:
            valeurContenuValeur=guest_bytes(chemin);valeurCible='/example/'+Langue+'/'+nom
            if len(valeurContenuValeur)>16384 or len(valeurCible.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+valeurCible)
            séquenceInstructionMachine.append('valeurTraité=InterpréteurCommandes.fichierExemple(%s,"%s"); if(valeurTraité<0)return valeurTraité;'%(json.dumps(valeurCible,ensure_ascii=True),valeurContenuValeur.hex()))
            manifesteLot[valeurCible]={'bytes':len(valeurContenuValeur),'sha256':hashlib.sha256(valeurContenuValeur).hexdigest()}
        séquenceInstructionMachine += ['return 0;}']
    séquenceInstructionMachine += ['return -22;}}']
    (cheminRacine/'build/LotExemple.java').write_text('\n'.join(séquenceInstructionMachine)+'\n')
    (donnéesRésultat/'manifest.json').write_text(json.dumps(manifesteLot,ensure_ascii=False,indent=2)+'\n')
