#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from testRéseauUtilisateur import MachineVirtuelle, position
from TestJava import valeurÉditer, fichierInvité

def exécuterCommande():
    résultat = {}
    source = (position.parent / 'posix-kor/ExempleJava/FileDemo.java').read_text()
    for valeurGenre in ('elf', 'iso'):
        machine = MachineVirtuelle(position / ('build/kernel.' + valeurGenre), valeurGenre, valeurRéseau=False)
        try:
            valeurÉditer(machine, 'FileDemo.java', source)
            machine.commande('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for valeurItération in range(2):
                Sortie = machine.commande('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            listeEntréeÉlément = machine.commande('ls', ['java.txt  3 bytes'])
            taille = int(re.search(r'FileDemo.class\s+(\d+) bytes', listeEntréeÉlément)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as valeurTemporaire:
                valeurRépertoire = Path(valeurTemporaire)
                fichierInvité(machine, 2, taille, valeurRépertoire / 'FileDemo.class')
                Hôte = subprocess.check_output(['java', '-Xverify:all', '-cp', str(valeurRépertoire), 'FileDemo'], cwd=str(valeurRépertoire), universal_newlines=True)
                assert Hôte == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Hôte
                assert (valeurRépertoire / 'java.txt').read_bytes() == b'A\xffB'
            valeurÉditer(machine, 'FileDemo.java', source.replace('output.write(65);', 'output.close(); output.write(65);'))
            machine.commande('javac FileDemo.java', ['Exit: 0'])
            machine.commande('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            valeurÉditer(machine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            machine.commande('javac FileDemo.java', ['Exit: 0'])
            machine.commande('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            machine.commande('run hello recovered', ['Exit: 0'])
            résultat[valeurGenre] = machine.enregistrementJournal.decode('utf-8', 'replace')
        finally:
            machine.fermer()
        print('PASS:', valeurGenre, '게스트 Java Fichier générer/ajouterFinContinuation/valeurOctet/EOF/estFermé/valeurÉchec/OpenJDK 교차 exécuterCommande', flush=True)
    (position / 'build/TestFichierJava.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    exécuterCommande()
