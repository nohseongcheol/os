#!/usr/bin/env python3
"""oma 커널의 liittymä, 프로세스 I_O, Unicode GUI 터미널을 todellinen_data raspi4b에서 testit."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Suorita_komento import aloite_juuri, komento


def Suorita_2():
    tulos = aloite_juuri / 'build/verification/shell'; tulos.mkdir(parents=True, exist_ok=True)
    vahvistus_raportti = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkriptio = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Prosessi = subprocess.Popen(komento()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Prosessi.stdout,selectors.EVENT_READ)
        def saada_sanoma(merkintä, suoritus_AIKAKATKAISU=45):
            data=bytearray(); lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+suoritus_AIKAKATKAISU
            while merkintä not in data:
                if time.monotonic()>lopettaa_puhelu_SIIRTYMÄ or Prosessi.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); transkriptio.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def lähettää(data, merkintä=b'jkoros-native> '):
            Prosessi.stdin.write(data); Prosessi.stdin.flush(); return saada_sanoma(merkintä)
        def liittymä(syöterivi, *예상결과):
            TULOS=lähettää(syöterivi.encode()+b'\n')
            for ARVO in 예상결과: assert ARVO in TULOS, (syöterivi,ARVO,TULOS)
            return TULOS
        def tiedoston_nimi(Nimi):
            teksti=liittymä('hex '+Nimi,'HEX BEGIN','HEX END'); Hae_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',teksti,re.S)
            data=bytes.fromhex(''.join(Hae_KR.group(2).split())); assert len(data)==int(Hae_KR.group(1)); return data
        try:
            saada_sanoma(b'jkoros-native> ')
            liittymä('mkdir 작업; cd 작업; pwd','/작업')
            liittymä('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert tiedoston_nimi('인사.txt')=='한글 data 😀\n'.encode()
            liittymä('cp 인사.txt kopioida_ARVO.txt; mv kopioida_ARVO.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            liittymä('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            liittymä('cd ..; rmdir 하위; echo $?','1\n')
            liittymä('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            liittymä('cp 인사.txt 인사.txt; echo $?','1\n'); assert tiedoston_nimi('인사.txt')=='한글 data 😀\n'.encode()
            liittymä('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in tiedoston_nimi('인사.txt')
            liittymä("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert tiedoston_nimi('리터럴')=='$인사\n누리\n'.encode()
            liittymä('echo one > lauseke_ARVO; echo two >> lauseke_ARVO; echo three >> lauseke_ARVO')
            liittymä('cat < lauseke_ARVO | grep t | tee 추림 | wc -l','2\n'); assert tiedoston_nimi('추림')==b'two\nthree\n'
            liittymä('head -n 1 lauseke_ARVO > etukamera_ARVO; tail -n 1 lauseke_ARVO > BACK_ARVO'); assert tiedoston_nimi('앞')==b'one\n'; assert tiedoston_nimi('뒤')==b'three\n'
            liittymä('grep absent lauseke_ARVO; echo $?','1\n')
            liittymä('echo untouched > suojata_ARVO')
            liittymä('echo destroyed > suojata_ARVO |','명령이 빠졌습니다'); assert tiedoston_nimi('suojata_ARVO')==b'untouched\n'
            liittymä('echo "oops','따옴표가 닫히지 않았습니다')
            liittymä('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            liittymä('echo bad 2> suojata_ARVO','번호를 지정한 tiedoston_nimi 서술자 I_O MUUTA_tila'); assert tiedoston_nimi('suojata_ARVO')==b'untouched\n'
            liittymä('rm 빈파일 리터럴 lauseke_ARVO 추림 etukamera_ARVO BACK_ARVO suojata_ARVO')
            vahvistus_raportti['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            liittymä("python -c 'print(123)' | wc -c",'4\n')
            liittymä("python -c 'print(456)' > ohjelma_f5044b9b.txt"); assert tiedoston_nimi('ohjelma_f5044b9b.txt')==b'456\n'
            liittymä("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            liittymä("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ohjelma_f5044b9b.txt", "b'456\\n'", "b''")
            liittymä("python -c 'print(\"x\"*17000)' | wc -c", 'VIRHE -28')
            liittymä('echo recovered | wc -c','10\n')
            liittymä("python -c 'import jkoros; print(jkoros.read("+'"/작업/ohjelma_f5044b9b.txt"'+"))'",'456','exit 0')
            liittymä('cd /; javac Hello.java','Compiled:','exit 0')
            liittymä('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in tiedoston_nimi('/작업/자바.txt')
            liittymä('cd 작업; echo "echo script > suoritus_KR" > komento.sh; echo "false || echo recovered >> suoritus_KR" >> komento.sh; sh komento.sh')
            assert tiedoston_nimi('suoritus_KR')==b'script\nrecovered\n'
            liittymä('rm suoritus_KR; echo "exit 7" > Lopeta_ohjelma.sh; sh Lopeta_ohjelma.sh; echo $?','7\n')
            liittymä('rm Lopeta_ohjelma.sh komento.sh ohjelma_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            vahvistus_raportti['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            liittymä('echo history-proof','history-proof')
            TULOS=lähettää(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert TULOS.count('history-proof')>=2, TULOS
            lähettää(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            TULOS=lähettää(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in TULOS, TULOS
            TULOS=lähettää(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in TULOS,TULOS
            TULOS=lähettää('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in TULOS,TULOS
            긴글='한글'*50
            TULOS=lähettää(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in TULOS
            liittymä('terminal','TERMINAL READY')
            liittymä('clear')
            liittymä('echo "한글 komentotulkki ABC xyz 012 😀"','한글 komentotulkki ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as asiakas:
                asiakas.settimeout(10); asiakas.connect(str(모의제어접속))
                with asiakas.makefile('rwb') as virta_ARVO:
                    json.loads(virta_ARVO.readline())
                    def 호출(Nimi,argumentti_MATRIISI=None):
                        verkko_sanoma={'execute':Nimi}
                        if argumentti_MATRIISI: verkko_sanoma['arguments']=argumentti_MATRIISI
                        virta_ARVO.write((json.dumps(verkko_sanoma)+'\n').encode()); virta_ARVO.flush()
                        while True:
                            palaute=json.loads(virta_ARVO.readline())
                            if 'error' in palaute: raise AssertionError(palaute)
                            if 'return' in palaute: return palaute['return']
                    호출('qmp_capabilities')
                    KUVA=tulos/'terminal.ppm'; 호출('screendump',{'filename':str(KUVA),'format':'ppm'})
                    호출('screendump',{'filename':str(tulos/'terminal.png'),'format':'png'})
                    data=KUVA.read_bytes().split(b'\n',3)[3]
                    def kuvapiste(x_koordinaatti,Y_koordinaatti): return tuple(data[(Y_koordinaatti*640+x_koordinaatti)*3:(Y_koordinaatti*640+x_koordinaatti)*3+3])
                    assert kuvapiste(12,48)==(32,80,144),kuvapiste(12,48)
                    assert len(set(kuvapiste(x_koordinaatti,Y_koordinaatti) for Y_koordinaatti in range(100,116) for x_koordinaatti in range(24,56)))>1,'Hangul glyphs missing'
                    liittymä('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    liittymä("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(KUVA),'format':'ppm'})
                    복원자료=KUVA.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    liittymä('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): liittymä('echo scroll-'+str(순번),'scroll-'+str(순번))
                    lähettää(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(tulos/'terminal-scroll.png'),'format':'png'})
                    TULOS=lähettää(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in TULOS,TULOS
                    liittymä('rm visible.txt')
                    호출('quit')
            Prosessi.wait(timeout=5)
            vahvistus_raportti['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            vahvistus_raportti['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Prosessi.poll() is None:
                Prosessi.terminate()
                try: Prosessi.wait(timeout=5)
                except subprocess.TimeoutExpired: Prosessi.kill(); Prosessi.wait()
            준비살피미.close(); Prosessi.stdin.close(); Prosessi.stdout.close()
            (tulos/'serial.log').write_bytes(transkriptio)
            (tulos/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Suorita_2()
