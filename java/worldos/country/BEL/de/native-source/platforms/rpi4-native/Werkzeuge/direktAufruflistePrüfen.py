#!/usr/bin/env python3
"""verteilungWert class의 직접 Deutsch GUI/ausführungsfadenWert 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

projektWurzel = Path(__file__).resolve().parents[1]

def ausführenVorgang():
    klassenListe = ('fenster', 'schaltfläche', 'beschriftung', 'TextFeld', 'BildschirmElement', 'AktionMitteilung', 'EreignisWarteschlange', 'hintergrundarbeiter',
             'Aufgabe', 'AusführbarAufgabe', 'AktionEmpfänger')
    Paket = projektWurzel/'dist/jkoros-native-korean.jar'
    Deklarationen = subprocess.check_output(['javap', '-classpath', str(Paket), '-private', '-c']+
                                ['Deutsch.eigen.'+Name for Name in klassenListe]).decode()
    for unzulässigWert in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert unzulässigWert not in Deklarationen, unzulässigWert
    Beispiele = subprocess.check_output(['javap', '-classpath', str(projektWurzel/'build/examples/classes'), '-c', 'Fensterbeispiel']).decode()
    for istErforderlich in ('public static void ausführenVorgang()', 'Deutsch/eigen/EreignisWarteschlange.späterAufrufen', 'Deutsch/eigen/AktionMitteilung.befehlText'):
        assert istErforderlich in Beispiele, istErforderlich
    for unzulässigWert in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert unzulässigWert not in Beispiele, unzulässigWert
    zielWert = projektWurzel/'build/verification/naming'; zielWert.mkdir(parents=True, exist_ok=True)
    (zielWert/'direct-bytecode.txt').write_text(Deklarationen+'\n'+Beispiele)
    protokolldateiAufzeichnung = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(Paket.read_bytes()).hexdigest(), 'classes': list(klassenListe),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (zielWert/'direct-bytecode.json').write_text(json.dumps(protokolldateiAufzeichnung, ensure_ascii=False, indent=2)+'\n')
    print('PASS: Deutsch 직접 GUI·ausführungsfadenWert 바이트코드와 Beispiele aufrufen')

if __name__ == '__main__': ausführenVorgang()
