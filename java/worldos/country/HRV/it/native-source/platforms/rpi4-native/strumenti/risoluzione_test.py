#!/usr/bin/env python3
"""effettivo_dati QEMU/VNC에서 schermata Dimensione·limite_VALORE·Finestra spostare_VALORE·Swing·언어별 그리기를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from PC_Vista import IDENTICO_VALORE
from Esegui_comando import azione_radice


def risoluzione_test(너비, altezza_VALORE, KR_percorso):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numero_di_porta = 임시.getsockname()[1]
    ridimensionare_SMS = '{}x{}'.format(너비, altezza_VALORE)
    Processi_VALORE = subprocess.Popen(['python3', str(azione_radice/'strumenti/Esegui_comando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numero_di_porta), '--resolution', ridimensionare_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettore_a916db4e = selectors.DefaultSelector(); selettore_a916db4e.register(Processi_VALORE.stdout, selectors.EVENT_READ)
    LOG_riga = bytearray(); remoto_VALORE = None; trasferire_VALORE = None

    def 기다리기(mostrare_VALORE, avvia=0):
        scadenza_VALORE = time.monotonic() + 60
        while mostrare_VALORE not in LOG_riga[avvia:]:
            if time.monotonic() > scadenza_VALORE or Processi_VALORE.poll() is not None or b'HALTED' in LOG_riga or b'PANIC:' in LOG_riga:
                raise AssertionError(LOG_riga[avvia:].decode('utf-8', 'replace'))
            for Evento, _ in selettore_a916db4e.select(.1):
                dati = Evento.fileobj.read(65536)
                if dati: LOG_riga.extend(dati)
        return LOG_riga[avvia:].decode('utf-8', 'replace')

    def clic_pulsante(simbolo, 눌림=True): remoto_VALORE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolo))

    def inviare_SMS(testo):
        avvia = len(LOG_riga)
        for carattere_VALORE in testo:
            simbolo = 0xff0d if carattere_VALORE == '\n' else ord(carattere_VALORE) if ord(carattere_VALORE) < 256 else 0x1000000 | ord(carattere_VALORE)
            clic_pulsante(simbolo); clic_pulsante(simbolo, False)
        return avvia

    def Shell(testo): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', inviare_SMS(testo+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Verticale_funzione, 눌림): remoto_VALORE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Verticale_funzione))

    def clic_VALORE(가로, Verticale_funzione): 가리키기(가로, Verticale_funzione, 1); 가리키기(가로, Verticale_funzione, 0)

    def bitmap_foto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 effettivo_dati 너비를 쓴다.
        remoto_VALORE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, altezza_VALORE))
        disegno_VALORE = Image.new('RGB', (너비, altezza_VALORE)); area_VALORE_9285603e = 0
        while True:
            Kind_VALORE = IDENTICO_VALORE(remoto_VALORE, 1)[0]
            if Kind_VALORE == 2: continue
            if Kind_VALORE == 3:
                durata_VALORE = struct.unpack('>I', IDENTICO_VALORE(remoto_VALORE, 7)[3:])[0]; IDENTICO_VALORE(remoto_VALORE, durata_VALORE); continue
            assert Kind_VALORE == 0, Kind_VALORE
            articolo_CONTA_NUMERI = struct.unpack('>H', IDENTICO_VALORE(remoto_VALORE, 3)[1:])[0]
            for _ in range(articolo_CONTA_NUMERI):
                가로, Verticale_funzione, 폭, durata_VALORE, Codifica_VALORE = struct.unpack('>HHHHi', IDENTICO_VALORE(remoto_VALORE, 12))
                assert Codifica_VALORE == 0 and 가로+폭 <= 너비 and Verticale_funzione+durata_VALORE <= altezza_VALORE
                disegno_VALORE.paste(Image.frombytes('RGB', (폭, durata_VALORE), IDENTICO_VALORE(remoto_VALORE, 폭*durata_VALORE*4), 'raw', 'BGRX'), (가로, Verticale_funzione))
                area_VALORE_9285603e += 폭*durata_VALORE
            if area_VALORE_9285603e:
                assert area_VALORE_9285603e == 너비*altezza_VALORE, area_VALORE_9285603e
                return disegno_VALORE

    def assegno_pixel(coordinata_VALORE, 색):
        scadenza_VALORE = time.monotonic()+10
        while True:
            disegno_VALORE = bitmap_foto()
            if disegno_VALORE.getpixel(coordinata_VALORE) == 색: return disegno_VALORE
            if time.monotonic() > scadenza_VALORE: raise AssertionError((coordinata_VALORE, disegno_VALORE.getpixel(coordinata_VALORE), 색))

    def Upload_File(Nome, dati): trasferire_VALORE.storbinary('STOR '+Nome, io.BytesIO(dati))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ridimensionare_SMS+' RGB32').encode() in LOG_riga
        print('BOOT:', ridimensionare_SMS, flush=True)
        remoto_numero = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_riga).group(1))
        remoto_VALORE = socket.create_connection(('127.0.0.1', remoto_numero), timeout=20)
        assert IDENTICO_VALORE(remoto_VALORE, 12) == b'RFB 003.008\n'; remoto_VALORE.sendall(b'RFB 003.008\n')
        assert 1 in IDENTICO_VALORE(remoto_VALORE, IDENTICO_VALORE(remoto_VALORE, 1)[0]); remoto_VALORE.sendall(b'\x01')
        assert IDENTICO_VALORE(remoto_VALORE, 4) == b'\0'*4; remoto_VALORE.sendall(b'\x01')
        stato_iniziale = IDENTICO_VALORE(remoto_VALORE, 24); assert struct.unpack('>HH', stato_iniziale[:4]) == (너비, altezza_VALORE)
        IDENTICO_VALORE(remoto_VALORE, struct.unpack('>I', stato_iniziale[20:])[0])
        remoto_VALORE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        remoto_VALORE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        assegno_pixel((너비-1, altezza_VALORE-1), (24, 32, 48))
        # schermata DESTRA 아래까지 이동한다. Indietro_articolo 640×480 limite_VALORE 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, altezza_VALORE-360+12, 1); 가리키기(너비-568+28, altezza_VALORE-360+12, 0)
        assegno_pixel((너비-568, altezza_VALORE-360), (32, 80, 144))
        avvia = len(LOG_riga); clic_VALORE(너비-20, altezza_VALORE-345); 기다리기(b'TERMINAL FOCUS 1', avvia)
        assegno_pixel((너비-568, altezza_VALORE-360), (24, 32, 48))
        avvia = len(LOG_riga); clic_VALORE(80, 16); 기다리기(b'TERMINAL FOCUS 1', avvia)
        Shell('ftpd start')
        trasferire_VALORE = ftplib.FTP(); trasferire_VALORE.encoding = 'utf-8'; trasferire_VALORE.connect('127.0.0.1', numero_di_porta, timeout=20); trasferire_VALORE.login()
        # C limite_VALORE 검사는 32비트 unsigned negativo_VALORE CONVERTI_VALORE·ritagliare 밖·빈 사각형을 포함한다.
        codiceSorgente = '''#include <schermata_ABI.h>
#include <File_ABI.h>
int main(void) {
    unsigned 너비=화면너비(), altezza_VALORE=schermata_altezza();
    if(너비!=WIDTH || altezza_VALORE!=HEIGHT) return 1;
    if(Disegno_rettangolo(너비,altezza_VALORE,0,0,0)) return 2;
    if(Disegno_rettangolo(너비,altezza_VALORE-1,1,1,0)!=-22) return 3;
    if(Disegno_rettangolo(너비-1,altezza_VALORE,1,1,0)!=-22) return 4;
    if(Disegno_rettangolo(-1,0,1,1,0)!=-22) return 5;
    if(Disegno_rettangolo(0,0,-1,1,0)!=-22) return 6;
    if(Disegno_rettangolo(너비-1,altezza_VALORE-1,1,1,0x332211)) return 7;
    scrivere_File_dati(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altezza_VALORE))
        Upload_File('test_schermata.c', codiceSorgente.encode())
        assert 'exit 0' in Shell('cc /test_schermata.c -o /test_schermata')
        기다리기(b'C RESOLUTION PASS', inviare_SMS('run /test_schermata\n'))
        assegno_pixel((너비-1, altezza_VALORE-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', inviare_SMS('q'))
        codiceSorgente = '''from Italiano import schermata_ridimensionare, Disegno_rettangolo, 그림기다리기, uscitaTesto, errore_di_sistema
너비, altezza_VALORE = schermata_ridimensionare()
assert (너비, altezza_VALORE) == (WIDTH, HEIGHT)
try:
    Disegno_rettangolo(너비, altezza_VALORE-1, 1, 1, 0)
    raise AssertionError("boundary")
except errore_di_sistema as errore:
    assert errore.INDICE == 22
Disegno_rettangolo(너비-1, altezza_VALORE-1, 1, 1, 0x665544)
uscitaTesto("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altezza_VALORE))
        Upload_File('test_schermata.py', codiceSorgente.encode())
        기다리기(b'PYTHON RESOLUTION PASS', inviare_SMS('python /test_schermata.py\n'))
        assegno_pixel((너비-1, altezza_VALORE-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', inviare_SMS('q'))
        codiceSorgente = '''import Italiano.nativo.*;
public class risoluzione_test {
    public static void main(String[] argomenti) {
        int 너비=schermata.너비(), altezza_VALORE=schermata.altezza_VALORE();
        if (너비!=WIDTH || altezza_VALORE!=HEIGHT) throw new Stato_eccezione("Dimensione");
        try { schermata.rettangolo(너비,altezza_VALORE-1,1,1,0); throw new Stato_eccezione("ritagliare"); }
        catch (non_valida_argomento_eccezione errore) { }
        schermata.cancellare_voce(0x302018);
        schermata.rettangolo(너비-1,altezza_VALORE-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        schermata.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altezza_VALORE))
        # eccezione 처리는 host javac 결과를 nativo JVM에 올려 검사한다.
        limite_fonte = KR_percorso/'해상도경계시험.java'
        limite_fonte.write_text(codiceSorgente.replace('class risoluzione_test', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(azione_radice/'dist/jkoros-native-korean.jar'), '-d', str(KR_percorso), str(limite_fonte)])
        Upload_File('해상도경계시험.class', (KR_percorso/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', inviare_SMS('java 해상도경계시험\n'))
        assegno_pixel((너비-1, altezza_VALORE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', inviare_SMS('q'))
        # 게스트 javac의 Supporto_VALORE 문법으로 Dimensione query_VALORE·cancellare_voce·다섯 argomenti 그리기를 컴파일한다.
        codiceSorgente = '''public class risoluzione_test {
    public static void main(String[] argomenti) {
        int 너비=Italiano.nativo.schermata.너비();
        int altezza_VALORE=Italiano.nativo.schermata.altezza_VALORE();
        if (너비!=WIDTH || altezza_VALORE!=HEIGHT) return;
        Italiano.nativo.schermata.cancellare_voce(3153944);
        Italiano.nativo.schermata.rettangolo(너비-1,altezza_VALORE-1,1,1,10061943);
        Italiano.nativo.uscitaTesto.scrivere_riga("JAVA RESOLUTION PASS");
        Italiano.nativo.schermata.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(altezza_VALORE))
        Upload_File('risoluzione_test.java', codiceSorgente.encode())
        risultato = Shell('javac risoluzione_test.java'); assert 'exit 0' in risultato, risultato
        기다리기(b'JAVA RESOLUTION PASS', inviare_SMS('java risoluzione_test\n'))
        assegno_pixel((너비-1, altezza_VALORE-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', inviare_SMS('q'))
        Upload_File('Swing_test.class', (KR_percorso/'Swing_test.class').read_bytes())
        기다리기(b'SWING READY', inviare_SMS('java Swing_test\n'))
        가로, Verticale_funzione = (너비-400)//2, (altezza_VALORE-280)//2
        disegno_VALORE = assegno_pixel((가로, Verticale_funzione), (32, 80, 144))
        disegno_VALORE.save(str(KR_percorso/(ridimensionare_SMS+'.png')))
        avvia = len(LOG_riga); clic_VALORE(가로+80, Verticale_funzione+155)
        기다리기('SWING CLICK Nome'.encode(), avvia)
        avvia = len(LOG_riga); clic_VALORE(가로+385, Verticale_funzione+15); 기다리기(b'jkoros-native> ', avvia)
        assert 'AFTER_RESOLUTION' in Shell('echo AFTER_RESOLUTION')
        print('PASS:', ridimensionare_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if trasferire_VALORE: trasferire_VALORE.close()
        if remoto_VALORE: remoto_VALORE.close()
        if Processi_VALORE.poll() is None:
            Processi_VALORE.terminate()
            try: Processi_VALORE.wait(timeout=8)
            except subprocess.TimeoutExpired: Processi_VALORE.kill(); Processi_VALORE.wait()
        selettore_a916db4e.close(); Processi_VALORE.stdout.close()
        (KR_percorso/(ridimensionare_SMS+'.log')).write_bytes(LOG_riga)


def avvia():
    KR_percorso = azione_radice/'build/verification/resolution'; KR_percorso.mkdir(parents=True, exist_ok=True)
    LOG_riga = {'passed': False, 'kernel_sha256': hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for non_valida_VALORE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            risultato = subprocess.run(['python3', str(azione_radice/'strumenti/Esegui_comando.py'), '--resolution', non_valida_VALORE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert risultato.returncode == 2 and b'--resolution' in risultato.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_percorso), str(azione_radice/'prove/자바/Swing_test.java')])
        for 너비, altezza_VALORE in ((1920,1080), (1280,720), (640,480)):
            risoluzione_test(너비, altezza_VALORE, KR_percorso); LOG_riga['resolutions'].append([너비, altezza_VALORE])
        LOG_riga.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_percorso/'report.json').write_text(json.dumps(LOG_riga, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': avvia()
