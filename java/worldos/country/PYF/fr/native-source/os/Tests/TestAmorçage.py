#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 valeurSériel/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

position = Path(__file__).resolve().parents[1]


def attendreFin(Contrôles, description, valeurLimite=15):
    terminaison = time.monotonic() + valeurLimite
    while time.monotonic() < terminaison:
        résultat = Contrôles()
        if résultat:
            return résultat
        time.sleep(0.05)
    raise AssertionError('valeurTemps 초과: ' + description)


def Tests(valeurGenre):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as valeurTemporaire:
        valeurTemporaire = Path(valeurTemporaire)
        cheminSériel = valeurTemporaire / 'serial.sock'
        cheminMoniteur = valeurTemporaire / 'monitor.sock'
        commande = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(cheminSériel) + ',server,nowait',
                '-monitor', 'unix:' + str(cheminMoniteur) + ',server,nowait']
        commande += ['-kernel', str(position / 'build/kernel.elf')] if valeurGenre == 'elf' else [
            '-cdrom', str(position / 'build/kernel.iso'), '-boot', 'd']
        # valeurSériel 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        commande += ['-S']
        valeurProcessus = subprocess.Popen(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        valeurSériel = socket.socket(socket.AF_UNIX)
        valeurMoniteur = socket.socket(socket.AF_UNIX)
        enregistrementJournal = bytearray()
        try:
            def préparerPriseRéseau():
                if valeurProcessus.poll() is not None:
                    raise AssertionError(valeurProcessus.stderr.read().decode('utf-8', 'replace'))
                return cheminSériel.exists() and cheminMoniteur.exists()
            attendreFin(préparerPriseRéseau, 'QEMU valeurPriseRéseau')
            valeurSériel.connect(str(cheminSériel))
            valeurMoniteur.connect(str(cheminMoniteur))
            valeurSériel.setblocking(False)
            valeurMoniteur.sendall(b'cont\n')

            def Entêtes(Chaîne, lancer=0):
                lire, _, _ = select.select([valeurSériel], [], [], 0.1)
                if lire:
                    Données = valeurSériel.recv(65536)
                    if not Données:
                        raise AssertionError('valeurSériel connecter programmeQuitter')
                    enregistrementJournal.extend(Données)
                if valeurProcessus.poll() is not None:
                    raise AssertionError('QEMU 비정상 programmeQuitter: ' + str(valeurProcessus.returncode))
                return Chaîne.encode('utf-8') in enregistrementJournal[lancer:]

            def testCommandes(valeurEntrée, attente):
                lancer = len(enregistrementJournal)
                valeurSériel.sendall(valeurEntrée.encode('ascii'))
                attendreFin(lambda: Entêtes(attente, lancer), attente)
                attendreFin(lambda: Entêtes('jkoros> ', lancer), 'commande étatValeurAprès 프롬프트')

            attendreFin(lambda: Entêtes('READY'), valeurGenre + ' Amorçage')
            assert b'JAVA SELFTEST PASS' in enregistrementJournal
            assert 'Java 기계어 valeurNoyau lancer'.encode() in enregistrementJournal
            testCommandes('info\r\n', 'embedded subset JVM / polling kernel')
            testCommandes('help\n', 'free N | echo TEXT')
            testCommandes('mem\n', ' / 8 (각 4096바이트)')
            testCommandes('echo natix\bve\n', 'native\r\n')
            for numéro in range(8):
                testCommandes('alloc\n', 'valeurSection numéro: ' + str(numéro))
            testCommandes('alloc\n', 'valeurSection numéro: -1')
            testCommandes('free 3\n', '반환됨')
            testCommandes('free 3\n', '할당되지 않은 valeurSection')
            testCommandes('free 99\n', '사용법: free 0..7')
            testCommandes('alloc\n', 'valeurSection numéro: 3')
            testCommandes('free 0\n', '반환됨')
            testCommandes('test\n', 'JAVA SELFTEST PASS')
            testCommandes('unknown\n', '알 nombre 없는 명령입니다')
            testCommandes('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            lancer = len(enregistrementJournal)
            for valeurTouche in ('i', 'n', 'f', 'o', 'ret'):
                valeurMoniteur.sendall(('sendkey ' + valeurTouche + ' 30\n').encode())
                time.sleep(0.09)
            attendreFin(lambda: Entêtes('embedded subset JVM / polling kernel', lancer), 'PS/2 info valeurEntrée')
            testCommandes('echo ' + 'a' * 150 + '\n', 'a' * 123)
            valeurSériel.sendall(b'halt\n')
            attendreFin(lambda: Entêtes('HALTED'), 'exécutionArrêterMachine commande')
            assert b'PANIC' not in enregistrementJournal and b'SELFTEST FAIL' not in enregistrementJournal
            print('PASS: {} Amorçage, Java interne Tests, valeurSériel commande, PS/2 valeurEntrée, allouerStockage/résultatRetourner, exécutionArrêterMachine'.format(valeurGenre))
            return enregistrementJournal.decode('utf-8', 'replace')
        finally:
            valeurSériel.close()
            valeurMoniteur.close()
            valeurProcessus.terminate()
            try:
                valeurProcessus.wait(timeout=3)
            except subprocess.TimeoutExpired:
                valeurProcessus.kill()
                valeurProcessus.wait()


if __name__ == '__main__':
    résultat = {valeurGenre: Tests(valeurGenre) for valeurGenre in ('elf', 'iso')}
    (position / 'build/TestAmorçage.json').write_text(json.dumps(résultat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
