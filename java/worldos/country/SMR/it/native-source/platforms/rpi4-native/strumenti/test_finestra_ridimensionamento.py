#!/usr/bin/env python3
"""effettivo_dati QEMU/VNC에서 terminale 모서리 trascinare_VALORE·puntatore·동적 carattere_VALORE slot_voce·Modifica_VALORE Contenuto_VALORE 보존를 검사한다."""
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


def test_finestra_ridimensionamento(너비, altezza_VALORE, KR_percorso):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); numero_di_porta = 임시.getsockname()[1]
    ridimensionare_SMS = '{}x{}'.format(너비, altezza_VALORE)
    Processi_VALORE = subprocess.Popen(['python3', str(azione_radice/'strumenti/Esegui_comando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(numero_di_porta), '--resolution', ridimensionare_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selettore_a916db4e = selectors.DefaultSelector(); selettore_a916db4e.register(Processi_VALORE.stdout, selectors.EVENT_READ)
    LOG_riga = bytearray(); remoto_VALORE = None; trasferire_VALORE = None; puntatore_Nascosta=[False]

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

    def Shell(testo): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', inviare_SMS(testo+'; echo __RESIZE_DONE__\n'))

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
                if Codifica_VALORE == -239:
                    assert 폭==0 and durata_VALORE==0, 'remote cursor must be hidden'
                    puntatore_Nascosta[0]=True
                    continue
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
        remoto_VALORE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        assegno_pixel((너비-1, altezza_VALORE-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Evento,_ in selettore_a916db4e.select(.02):
                    dati=Evento.fileobj.read(65536)
                    if dati:LOG_riga.extend(dati)
        Finestra=[12,48,568,360]
        def verificare_ridimensionare():
            colonna_VALORE,riga_VALORE=(Finestra[2]-24)//8,(Finestra[3]-56)//16
            testo=Shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(colonna_VALORE,riga_VALORE) in testo,testo
            # effettivo_dati Finestra 테두리: 단지 Dimensione query_VALORE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            assegno_pixel((Finestra[0],Finestra[1]),(32,80,144))
            disegno_VALORE=assegno_pixel((Finestra[0]+Finestra[2]-1,Finestra[1]+Finestra[3]-1),(39,49,64))
            return disegno_VALORE
        def 모서리(direzione):
            return (Finestra[0]+(3 if direzione in (1,3) else Finestra[2]-4),Finestra[1]+(3 if direzione<=2 else Finestra[3]-4))
        def ridimensionare_trascinare(direzione,차이,pulsante=1):
            가,세=모서리(direzione);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if direzione in (1,4) else 가+7,세-7)
            assegno_pixel(흰점,(255,255,255))
            가리키기(가,세,pulsante)
            끝가=max(0,min(너비-1,가+차이[0]));chiudere_Verticale=max(0,min(altezza_VALORE-1,세+차이[1]))
            가리키기(끝가,chiudere_Verticale,pulsante);가리키기(끝가,chiudere_Verticale,0);숨고르기()
            if pulsante==1:
                SINISTRA_VALORE,위,폭,durata_VALORE=Finestra;DESTRA_VALORE,아래=SINISTRA_VALORE+폭,위+durata_VALORE
                if direzione in (1,3):SINISTRA_VALORE=max(0,min(DESTRA_VALORE-360,SINISTRA_VALORE+끝가-가))
                else:DESTRA_VALORE=max(SINISTRA_VALORE+360,min(너비,DESTRA_VALORE+끝가-가))
                if direzione<=2:위=max(34,min(아래-216,위+chiudere_Verticale-세))
                else:아래=max(위+216,min(altezza_VALORE,아래+chiudere_Verticale-세))
                Finestra[:]=[SINISTRA_VALORE,위,DESTRA_VALORE-SINISTRA_VALORE,아래-위]
        verificare_ridimensionare();assert puntatore_Nascosta[0]
        ridimensionare_trascinare(4,(-100,-60),4);verificare_ridimensionare() # DESTRA 버튼은 크기를 바꾸지 않는다.
        for direzione,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ridimensionare_trascinare(direzione,차이);verificare_ridimensionare()
        # input_VALORE 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        inviare_SMS("echo '"+긴글+"'");숨고르기()
        ridimensionare_trascinare(4,(-1000,-1000));assert Finestra[2:]==[360,216]
        ridimensionare_trascinare(4,(너비,altezza_VALORE))
        avvia=inviare_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),avvia);verificare_ridimensionare()
        # vi가 Modifica_VALORE 중에 schermata 크기를 retry_VALORE 읽고, 저장하지 않은 한글도 유지한다.
        Shell('ftpd start')
        trasferire_VALORE=ftplib.FTP();trasferire_VALORE.encoding='utf-8';trasferire_VALORE.connect('127.0.0.1',numero_di_porta,timeout=20);trasferire_VALORE.login()
        기다리기(b'NORMAL',inviare_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',inviare_SMS('i미저장 한글 dati\n'));숨고르기()
        ridimensionare_trascinare(4,(-너비,-altezza_VALORE))
        # ANSI riga_VALORE 이동에 새 riga_VALORE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Finestra[3]-56)//16)).encode() in LOG_riga[-4096:]
        inviare_SMS('작은 창에서도 이어 Scrittura\n');숨고르기()
        ridimensionare_trascinare(4,(너비,altezza_VALORE))
        inviare_SMS('큰 창에서도 이어 Scrittura\n');숨고르기()
        clic_pulsante(0xff1b);clic_pulsante(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',inviare_SMS(':wq\n'))
        Contenuto_VALORE=bytearray();trasferire_VALORE.retrbinary('RETR 크기자료.txt',Contenuto_VALORE.extend)
        assert Contenuto_VALORE=='미저장 한글 dati\n작은 창에서도 이어 Scrittura\n큰 창에서도 이어 Scrittura\n'.encode(),Contenuto_VALORE
        verificare_ridimensionare().save(str(KR_percorso/(ridimensionare_SMS+'-large.png')))
        # 두 번째 창은 valore_predefinito Dimensione, retry_VALORE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        avvia=len(LOG_riga);clic_VALORE(70,16);기다리기(b'TERMINAL FOCUS 2',avvia)
        assert 'TERMINAL SIZE 68x19' in Shell('terminal size')
        avvia=len(LOG_riga);clic_VALORE(180,16);기다리기(b'TERMINAL FOCUS 1',avvia);verificare_ridimensionare()
        ridimensionare_trascinare(4,(-너비,-altezza_VALORE));verificare_ridimensionare().save(str(KR_percorso/(ridimensionare_SMS+'-small.png')))
        # Dimensione cambiare_VALORE BACK_VALORE X 닫기도 새로운 DESTRA 가장자리를 사용한다.
        avvia=len(LOG_riga);clic_VALORE(Finestra[0]+Finestra[2]-20,Finestra[1]+15);기다리기(b'TERMINAL FOCUS 2',avvia)
        assert 'RESIZE CLOSED' in Shell('echo RESIZE CLOSED')
        print('PASS:',ridimensionare_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if trasferire_VALORE:trasferire_VALORE.close()
        if remoto_VALORE:remoto_VALORE.close()
        if Processi_VALORE.poll() is None:
            Processi_VALORE.terminate()
            try:Processi_VALORE.wait(timeout=8)
            except subprocess.TimeoutExpired:Processi_VALORE.kill();Processi_VALORE.wait()
        selettore_a916db4e.close();Processi_VALORE.stdout.close();(KR_percorso/(ridimensionare_SMS+'.log')).write_bytes(LOG_riga)


def avvia():
    KR_percorso=azione_radice/'build/verification/resize';KR_percorso.mkdir(parents=True,exist_ok=True)
    LOG_riga={'passed':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,altezza_VALORE in ((640,480),(1920,1080)):
            test_finestra_ridimensionamento(너비,altezza_VALORE,KR_percorso);LOG_riga['resolutions'].append([너비,altezza_VALORE])
        LOG_riga.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_percorso/'report.json').write_text(json.dumps(LOG_riga,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':avvia()
