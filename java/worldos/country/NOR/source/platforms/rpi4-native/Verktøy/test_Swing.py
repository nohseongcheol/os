#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Utfør_kommando import speile_rot,Kommando

def Kjør_2():
    mål_VERDI_plassere=speile_rot/'build/verification/swing';mål_VERDI_plassere.mkdir(parents=True,exist_ok=True)
    time_bane=speile_rot/'build/verification/new-java';time_bane.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(speile_rot/'dist/jkoros-native-korean.jar'),'-d',str(time_bane),str(speile_rot/'시험/자바/Swing_test.java'),str(speile_rot/'시험/자바/한글창시험.java')])
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest()};LOG_POST=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_plassere=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        velger_a916db4e=selectors.DefaultSelector();velger_a916db4e.register(data_plassere.stdout,selectors.EVENT_READ)
        def håndtak_hendelse(초단위=.1):
            for 누름값,_ in velger_a916db4e.select(초단위):
                SEKUND_VERDI=누름값.fileobj.read(65536)
                if SEKUND_VERDI:LOG_POST.extend(SEKUND_VERDI)
            assert b'PANIC:' not in LOG_POST and b'HALTED' not in LOG_POST,LOG_POST[-2048:]
        def 기다리기(tusj,betalt_plassere,초단위=50):
            avslutte_en_samtale_FORSKYVNING=time.monotonic()+초단위
            while tusj not in LOG_POST[betalt_plassere:]:
                if time.monotonic()>avslutte_en_samtale_FORSKYVNING or data_plassere.poll() is not None:raise AssertionError(LOG_POST[betalt_plassere:].decode('utf-8','replace'))
                håndtak_hendelse()
            return bytes(LOG_POST[betalt_plassere:])
        def sende(SEKUND_VERDI,tusj=b'jkoros-native> '):
            betalt_plassere=len(LOG_POST);data_plassere.stdin.write(SEKUND_VERDI);data_plassere.stdin.flush();return 기다리기(tusj,betalt_plassere)
        def Shell(streng_data):return sende((streng_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def alias_VERDI(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikk_knapp(x_koordinat,Y_koordinat):return bytes([30,1,1,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8])
        def kommando_MODUS():
            data_plassere.stdin.write(b'\x1b');data_plassere.stdin.flush();avslutte_en_samtale_FORSKYVNING=time.monotonic()+.2
            while time.monotonic()<avslutte_en_samtale_FORSKYVNING:håndtak_hendelse(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');håndtak_hendelse(.3)
            data=(speile_rot/'build/verification/new-java/Swing_test.class').read_bytes()
            sende('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):sende(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            sende(b'.\n')
            sende('java Swing_test\n'.encode(),b'SWING READY')
            avslutte_en_samtale_FORSKYVNING=time.monotonic()+3
            while time.monotonic()<avslutte_en_samtale_FORSKYVNING:håndtak_hendelse(.1)
            # JFrame centered at (120,100), content at y=130.
            sende(klikk_knapp(200,210),b'',)  # focus JTextField
            data_plassere.stdin.write('누리'.encode());data_plassere.stdin.flush()
            avslutte_en_samtale_FORSKYVNING=time.monotonic()+.3
            while time.monotonic()<avslutte_en_samtale_FORSKYVNING:håndtak_hendelse(.05)
            KR=sende(klikk_knapp(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_POST)-len(KR))
            sende(alias_VERDI(1),b'TERMINAL FOCUS 2')
            KR=Shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in KR
            sende(klikk_knapp(180,12),b'TERMINAL FOCUS 1')
            avslutte_en_samtale_FORSKYVNING=time.monotonic()+.3
            while time.monotonic()<avslutte_en_samtale_FORSKYVNING:håndtak_hendelse(.05)
            with socket.socket(socket.AF_UNIX) as tegnkode:
                tegnkode.settimeout(10);tegnkode.connect(str(모의제어접속))
                with tegnkode.makefile('rwb') as Fil_oppføring:
                    json.loads(Fil_oppføring.readline())
                    for forespørsel_VERDI in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mål_VERDI_plassere/'native-swing.png'),'format':'png'}}):
                        Fil_oppføring.write((json.dumps(forespørsel_VERDI)+'\n').encode());Fil_oppføring.flush()
                        while True:
                            반환값=json.loads(Fil_oppføring.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            sende(klikk_knapp(505,115))
            Shell('echo SWING_CLOSED_OK')
            data=(time_bane/'한글창시험.class').read_bytes()
            sende('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):sende(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            sende(b'.\n')
            sende('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            sende(klikk_knapp(200,255),'KOREAN SWING CLICK Navn'.encode())
            sende(klikk_knapp(505,115))
            Shell('echo KOREAN_SWING_CLOSED_OK')
            validering_rapport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','norsk Vindu/Knapp/Gjøremål_notice/hendelse_kø directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_plassere.poll() is None:data_plassere.terminate()
            try:data_plassere.wait(timeout=5)
            except subprocess.TimeoutExpired:data_plassere.kill();data_plassere.wait()
            velger_a916db4e.close();data_plassere.stdin.close();data_plassere.stdout.close();(mål_VERDI_plassere/'serial.log').write_bytes(LOG_POST);(mål_VERDI_plassere/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kjør_2()
