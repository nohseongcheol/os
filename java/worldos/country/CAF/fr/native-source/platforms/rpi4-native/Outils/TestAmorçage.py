#!/usr/bin/env python3
"""donnéesEffectif raspi4b Amorçage, UART valeurEntrée, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from exécuterCommande import racineProjet, commande


def lancer():
    sortie = racineProjet / 'build/verification'
    sortie.mkdir(parents=True, exist_ok=True)
    transcription = bytearray()
    rapportValidation = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as cheminTravailEnCours:
        cheminQMP = Path(cheminTravailEnCours) / 'qmp.sock'
        argumentsCommande = commande() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(cheminQMP),
                           '-vnc', 'unix:{}'.format(Path(cheminTravailEnCours) / 'vnc.sock')]
        rapportValidation['command'] = argumentsCommande
        processus = subprocess.Popen(argumentsCommande, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        sélecteur = selectors.DefaultSelector()
        sélecteur.register(processus.stdout, selectors.EVENT_READ)
        def recevoirJusquÀ(marqueur, valeurDécalage=0, délaiExpirationExécution=45):
            tempsÉchéance = time.monotonic() + délaiExpirationExécution
            while marqueur not in transcription[valeurDécalage:]:
                if time.monotonic() > tempsÉchéance:
                    raise AssertionError('UART timeout: ' + repr(marqueur))
                for valeurEnfoncé, _ in sélecteur.select(0.2):
                    blocDonnées = valeurEnfoncé.fileobj.read(4096)
                    if blocDonnées:
                        transcription.extend(blocDonnées)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', transcription):
                    raise AssertionError('kernel failure')
                if processus.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(processus.returncode))
        try:
            recevoirJusquÀ(b'jkoros-native> ')
            marqueurs = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for marqueur in marqueurs:
                assert marqueur in transcription, marqueur
            # GTK 없는 élémentListeActuel 호스트에서도 VNC로 donnéesEffectif GUI를 볼 nombre 있어야 한다.
            with socket.socket(socket.AF_UNIX) as clientÉcran:
                clientÉcran.settimeout(5); clientÉcran.connect(str(Path(cheminTravailEnCours) / 'vnc.sock'))
                def valeurExact(taille):
                    résultat = b''
                    while len(résultat) < taille:
                        valeurFragment = clientÉcran.recv(taille - len(résultat))
                        if not valeurFragment: raise AssertionError('VNC disconnected')
                        résultat += valeurFragment
                    return résultat
                assert valeurExact(12) == b'RFB 003.008\n'
                clientÉcran.sendall(b'RFB 003.008\n')
                assert 1 in valeurExact(valeurExact(1)[0]); clientÉcran.sendall(b'\x01')
                assert valeurExact(4) == b'\x00\x00\x00\x00'; clientÉcran.sendall(b'\x01')
                valeurServeur = valeurExact(24)
                assert int.from_bytes(valeurServeur[:2], 'big') == 640 and int.from_bytes(valeurServeur[2:4], 'big') == 480
                valeurExact(int.from_bytes(valeurServeur[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for octetCommande, marqueur in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'Tests.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                valeurDécalage = len(transcription)
                processus.stdin.write(octetCommande + b'\n')
                processus.stdin.flush()
                recevoirJusquÀ(b'jkoros-native> ', valeurDécalage)
                assert marqueur in transcription[valeurDécalage:], marqueur
            def interpréteurCommandes(ligne, attendu):
                valeurDécalage = len(transcription)
                processus.stdin.write(ligne.encode('utf-8') + b'\n'); processus.stdin.flush()
                recevoirJusquÀ(b'jkoros-native> ', valeurDécalage)
                réponseRetour = bytes(transcription[valeurDécalage:])
                for texte in attendu:
                    assert texte.encode('utf-8') in réponseRetour, (ligne, texte, réponseRetour)
                return réponseRetour
            def entrer(ligne, invite):
                valeurDécalage = len(transcription)
                processus.stdin.write(ligne.encode('utf-8') + b'\n'); processus.stdin.flush()
                recevoirJusquÀ(invite, valeurDécalage)
                return bytes(transcription[valeurDécalage:])
            def valeurÉditer(nom, valeurContenuValeur, opérationAnnuler=False):
                entrer('edit ' + nom, b'edit> ')
                for ligne in valeurContenuValeur.splitlines(): entrer(ligne, b'edit> ')
                if opérationAnnuler:
                    valeurDécalage = len(transcription)
                    processus.stdin.write(b'\x03'); processus.stdin.flush()
                    recevoirJusquÀ(b'jkoros-native> ', valeurDécalage)
                    assert b'EDIT CANCELLED' in transcription[valeurDécalage:]
                else:
                    assert b'SAVED' in entrer('.', b'jkoros-native> ')
            def fichiersTéléverser(nom, Données):
                assert len(Données) <= 16384
                entrer('load ' + nom, b'hex> ')
                for indiceOrdinal in range(0, len(Données), 64): entrer(Données[indiceOrdinal:indiceOrdinal+64].hex(), b'hex> ')
                assert b'LOADED' in entrer('.', b'jkoros-native> ')
            def télécharger(nom):
                réponseRetour = interpréteurCommandes('hex ' + nom, ['HEX BEGIN', 'HEX END'])
                estÉgal = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', réponseRetour, re.S)
                Données = bytes.fromhex(''.join(estÉgal.group(2).decode('ascii').split()))
                assert len(Données) == int(estÉgal.group(1)); return Données
            interpréteurCommandes('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            interpréteurCommandes('java -version', ['not OpenJDK', 'exit 0'])
            interpréteurCommandes('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            interpréteurCommandes('java Hello "한글 arguments 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 arguments 😀', 'exit 0'])
            interpréteurCommandes('python --version', ['MicroPython 1.24.1', 'exit 0'])
            interpréteurCommandes('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Fichier', 'exit 0'])
            interpréteurCommandes('cat python.txt', ['한글 Fichier'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            classeJava = sortie / 'Hello.class'; classeJava.write_bytes(télécharger('Hello.class'))
            attendu = subprocess.check_output(['java', '-Xverify:all', '-cp', str(sortie), 'Hello', '한글 arguments 😀']).decode('utf-8')
            assert attendu.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 arguments 😀'], attendu
            valeurÉditer('Salutation.java', 'public class Salutation { public static void main(String[] args) { int valeur = 7; System.out.println("한글=" + valeur); } }')
            interpréteurCommandes('javac Salutation.java', ['Compiled: Salutation.class', 'exit 0'])
            interpréteurCommandes('java Salutation', ['한글=7', 'exit 0'])
            (sortie / 'Salutation.class').write_bytes(télécharger('Salutation.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(sortie), 'Salutation']).decode().strip() == '한글=7'
            valeurÉditer('Hello.java', 'broken', opérationAnnuler=True)
            interpréteurCommandes('javac Hello.java', ['Compiled:', 'exit 0'])
            valeurÉditer('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            interpréteurCommandes('javac Broken.java', ['javac error:', 'exit 1'])
            fichiersTéléverser('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            interpréteurCommandes('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            interpréteurCommandes('rm Broken.java', [])
            importé = sortie / 'Imported.java'
            importé.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(importé)])
            fichiersTéléverser('Imported.class', (sortie / 'Imported.class').read_bytes())
            interpréteurCommandes('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            interpréteurCommandes('rm Imported.class', [])
            valeurÉditer('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            interpréteurCommandes('javac Loop.java', ['Compiled:', 'exit 0'])
            réponseRetour = interpréteurCommandes('java Loop', ['exit '])
            assert b'instruction limit' in réponseRetour or b'exit -1004' in réponseRetour
            interpréteurCommandes('rm Loop.java', []); interpréteurCommandes('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            contrôlesPython = """import gc, jkoros
assert len('한글😀') == 3
assert 2**100 == 1267650600228229401496703205376
class Counter:
    def __init__(self, n): self.n = n
    def value(self): return self.n + 1
keep = Counter(41)
for i in range(300):
    garbage = [str(j) for j in range(80)]
    gc.collect()
assert keep.value() == 42
try:
    1 // 0
except ZeroDivisionError:
    print('PY EXCEPTION OK')
a = jkoros.udp_open(9401)
b = jkoros.udp_open(9402)
assert jkoros.udp_send(a, 9402, b'udp-python') == 10
assert jkoros.udp_recv(b) == (b'udp-python', 9401)
try:
    jkoros.udp_recv(b)
except OSError as e:
    assert e.args[0] == 11
jkoros.udp_close(a)
jkoros.udp_close(b)
print('PY GC UNICODE MPZ CLASS UDP OK')
"""
            valeurÉditer('checks.py', contrôlesPython)
            interpréteurCommandes('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            interpréteurCommandes('rm checks.py', [])
            valeurÉditer('helper.py', 'value = 321')
            interpréteurCommandes("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            interpréteurCommandes('rm helper.py', [])
            interpréteurCommandes("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            interpréteurCommandes("python -c 'while True: pass'", ['exit -1004'])
            for indiceOrdinal in range(4):
                interpréteurCommandes('python hello.py', ['한글 Fichier', 'exit 0'])
                interpréteurCommandes('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            fichiersTéléverser('app.elf', (racineProjet / 'build/user/demo.elf').read_bytes())
            assert télécharger('app.elf') == (racineProjet / 'build/user/demo.elf').read_bytes()
            interpréteurCommandes('run app.elf', ['EL0 C++', 'exit 0'])
            fichiersTéléverser('app.elf', b'not an ELF')
            interpréteurCommandes('run app.elf', ['exit -8'])
            interpréteurCommandes('rm app.elf', [])
            interpréteurCommandes('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            cheminDessin = sortie / 'java-framebuffer'; cheminDessin.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(racineProjet / 'dist/jkoros-native-korean.jar'), '-d', str(cheminDessin), str(racineProjet / 'Tests/Java/testÉcran.java')])
            fichiersTéléverser('testÉcran.class', (cheminDessin / 'testÉcran.class').read_bytes())
            interpréteurCommandes('java testÉcran', ['Écran rogner rejeterValeur', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            interpréteurCommandes('rm testÉcran.class', [])
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10)
                client.connect(str(cheminQMP))
                with client.makefile('rwb') as valeurFlux:
                    Salutation = json.loads(valeurFlux.readline())
                    def connexionContrôleSimulacre(exécuterTâche, argumentTransféré=None):
                        messageRéseau = {'execute': exécuterTâche}
                        if argumentTransféré: messageRéseau['arguments'] = argumentTransféré
                        valeurFlux.write((json.dumps(messageRéseau) + '\n').encode())
                        valeurFlux.flush()
                        while True:
                            réponse = json.loads(valeurFlux.readline())
                            if 'error' in réponse: raise AssertionError(réponse)
                            if 'return' in réponse: return réponse['return']
                    connexionContrôleSimulacre('qmp_capabilities')
                    captureÉcran = sortie / 'framebuffer.ppm'
                    connexionContrôleSimulacre('screendump', {'filename': str(captureÉcran), 'format': 'ppm'})
                    def entréesListeExemple(chemin, points):
                        with chemin.open('rb') as fichierPixel:
                            assert fichierPixel.readline().strip() == b'P6'
                            assert fichierPixel.readline().strip() == b'640 480'
                            assert fichierPixel.readline().strip() == b'255'
                            donnéesPixel = fichierPixel.read()
                        assert len(donnéesPixel) == 640 * 480 * 3
                        return [list(donnéesPixel[(coordonnéeCoordonnéeVerticale * 640 + coordonnéeCoordonnéeHorizontale) * 3:(coordonnéeCoordonnéeVerticale * 640 + coordonnéeCoordonnéeHorizontale) * 3 + 3]) for coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale in points]
                    assert entréesListeExemple(captureÉcran, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert entréesListeExemple(captureÉcran, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def envoyer(valeurEnfoncé, marqueur):
                        valeurDécalage = len(transcription)
                        processus.stdin.write(valeurEnfoncé); processus.stdin.flush()
                        recevoirJusquÀ(marqueur, valeurDécalage)
                    envoyer(b'gui\n', b'GUI READY:')
                    gUIPremier = sortie / 'gui-programs.ppm'
                    connexionContrôleSimulacre('screendump', {'filename': str(gUIPremier), 'format': 'ppm'})
                    connexionContrôleSimulacre('screendump', {'filename': str(sortie / 'gui-programs.png'), 'format': 'png'})
                    assert entréesListeExemple(gUIPremier, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    envoyer(b'\r', b'GUI ACTION 0 RESULT 0')
                    envoyer(b'\t', b'GUI FOCUS 1')
                    envoyer(b'\r', b'GUI ACTION 1 RESULT 0')
                    gUIDeuxième = sortie / 'gui-network.ppm'
                    connexionContrôleSimulacre('screendump', {'filename': str(gUIDeuxième), 'format': 'ppm'})
                    connexionContrôleSimulacre('screendump', {'filename': str(sortie / 'gui-network.png'), 'format': 'png'})
                    assert entréesListeExemple(gUIDeuxième, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    envoyer(b'\t', b'GUI FOCUS 2')
                    envoyer(b'\r', b'GUI ACTION 2 RESULT 0')
                    envoyer(b'\t', b'GUI FOCUS 3')
                    envoyer(b'\r', b'GUI ACTION 3 RESULT 0')
                    connexionContrôleSimulacre('screendump', {'filename': str(sortie / 'gui-python.png'), 'format': 'png'})
                    envoyer(b'q', b'jkoros-native> ')
                    rapportValidation['qemu'] = Salutation['QMP']['version']
                    connexionContrôleSimulacre('quit')
            processus.wait(timeout=10)
            # framebuffer 응답뿐 아니라 donnéesEffectif scanout 픽셀도 확인한다.
            with captureÉcran.open('rb') as entréeÉlémentFichier:
                assert entréeÉlémentFichier.readline().strip() == b'P6'
                valeurDimensions = entréeÉlémentFichier.readline().strip()
                assert valeurDimensions == b'640 480', valeurDimensions
                assert entréeÉlémentFichier.readline().strip() == b'255'
                listePixels = entréeÉlémentFichier.read()
            assert len(listePixels) == 640 * 480 * 3
            def pixel(coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale): return list(listePixels[(coordonnéeCoordonnéeVerticale * 640 + coordonnéeCoordonnéeHorizontale) * 3:(coordonnéeCoordonnéeVerticale * 640 + coordonnéeCoordonnéeHorizontale) * 3 + 3])
            entréesListeExemple = {'background': pixel(5, 5), 'panel': pixel(45, 85), 'tile': pixel(65, 115)}
            assert entréesListeExemple == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, entréesListeExemple
            rapportValidation.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
                'UTF-8 Korean/Japanese/Arabic/emoji UART', 'C++ direct RAM file API (21 runs)',
                'cooperative independent stacks (4 runs)', 'line shell/UTF-8/quotes/edit/cancel/hex upload/download',
                'guest Java compiler/JVM and OpenJDK two-way class verification',
                'Korean Java framebuffer library bounds and actual scanout pixels',
                'Korean Java identifiers, UTF-8 validation, malformed source and bounded execution',
                'MicroPython GC/classes/Unicode/MPZ/imports/exceptions/files/UDP and timeout recovery',
                'load and run custom ELF with malformed image rejection', 'RGB32 framebuffer pixels',
                'ELF64 rejection fixtures: 22', 'EL0 C++ constructors/RAII/FP/files/heap/pointer validation',
                'kernel/text/MMIO/guard/NX/privileged instruction protection', 'timer terminates EL0 infinite loop',
                'repeated EL0 program exit closes leaked descriptors', 'UDP loopback payload/peer/reply/truncation/queue/zero datagram/errors/cleanup',
                'GUI focus/keyboard activation/C++/UDP/Java/MicroPython launch/exit and framebuffer pixels'],
                vnc='RFB 3.8 / 640x480 / UART input',
                framebuffer=entréesListeExemple, kernel_sha256=hashlib.sha256((racineProjet / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if processus.poll() is None:
                processus.terminate()
                try: processus.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    processus.kill(); processus.wait(timeout=5)
            sélecteur.close()
            processus.stdin.close(); processus.stdout.close()
            (sortie / 'serial.log').write_bytes(transcription)
            (sortie / 'report.json').write_text(json.dumps(rapportValidation, indent=2) + '\n')


if __name__ == '__main__':
    lancer()
