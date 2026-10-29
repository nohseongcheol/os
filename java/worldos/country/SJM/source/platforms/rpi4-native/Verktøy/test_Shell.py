#!/usr/bin/env python3
"""eget 커널의 Shell, 프로세스 I_U, Unicode GUI 터미널을 faktisk_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Utfør_kommando import speile_rot, Kommando


def Kjør_2():
    produksjon = speile_rot / 'build/verification/shell'; produksjon.mkdir(parents=True, exist_ok=True)
    validering_rapport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    utskrift = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Prosess = subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Prosess.stdout,selectors.EVENT_READ)
        def motta_e_post(tusj, kjøring_TIMEOUT=45):
            data=bytearray(); avslutte_en_samtale_FORSKYVNING=time.monotonic()+kjøring_TIMEOUT
            while tusj not in data:
                if time.monotonic()>avslutte_en_samtale_FORSKYVNING or Prosess.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); utskrift.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def sende(data, tusj=b'jkoros-native> '):
            Prosess.stdin.write(data); Prosess.stdin.flush(); return motta_e_post(tusj)
        def Shell(Linje, *예상결과):
            KR=sende(Linje.encode()+b'\n')
            for VERDI in 예상결과: assert VERDI in KR, (Linje,VERDI,KR)
            return KR
        def Fil(Navn):
            Tekst=Shell('hex '+Navn,'HEX BEGIN','HEX END'); SØK_KR=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekst,re.S)
            data=bytes.fromhex(''.join(SØK_KR.group(2).split())); assert len(data)==int(SØK_KR.group(1)); return data
        try:
            motta_e_post(b'jkoros-native> ')
            Shell('mkdir 작업; cd 작업; pwd','/작업')
            Shell('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert Fil('인사.txt')=='한글 data 😀\n'.encode()
            Shell('cp 인사.txt kopiere_VERDI.txt; mv kopiere_VERDI.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            Shell('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            Shell('cd ..; rmdir 하위; echo $?','1\n')
            Shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            Shell('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fil('인사.txt')=='한글 data 😀\n'.encode()
            Shell('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fil('인사.txt')
            Shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fil('리터럴')=='$인사\n누리\n'.encode()
            Shell('echo one > kontoutdrag_VERDI; echo two >> kontoutdrag_VERDI; echo three >> kontoutdrag_VERDI')
            Shell('cat < kontoutdrag_VERDI | grep t | tee 추림 | wc -l','2\n'); assert Fil('추림')==b'two\nthree\n'
            Shell('head -n 1 kontoutdrag_VERDI > frontkamera_VERDI; tail -n 1 kontoutdrag_VERDI > TILBAKE_VERDI'); assert Fil('앞')==b'one\n'; assert Fil('뒤')==b'three\n'
            Shell('grep absent kontoutdrag_VERDI; echo $?','1\n')
            Shell('echo untouched > beskytte_VERDI')
            Shell('echo destroyed > beskytte_VERDI |','명령이 빠졌습니다'); assert Fil('beskytte_VERDI')==b'untouched\n'
            Shell('echo "oops','따옴표가 닫히지 않았습니다')
            Shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            Shell('echo bad 2> beskytte_VERDI','번호를 지정한 Fil 서술자 I_U bytt_MODUS'); assert Fil('beskytte_VERDI')==b'untouched\n'
            Shell('rm 빈파일 리터럴 kontoutdrag_VERDI 추림 frontkamera_VERDI TILBAKE_VERDI beskytte_VERDI')
            validering_rapport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            Shell("python -c 'print(123)' | wc -c",'4\n')
            Shell("python -c 'print(456)' > app_f5044b9b.txt"); assert Fil('app_f5044b9b.txt')==b'456\n'
            Shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            Shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            Shell("python -c 'print(\"x\"*17000)' | wc -c", 'feil -28')
            Shell('echo recovered | wc -c','10\n')
            Shell("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            Shell('cd /; javac Hello.java','Compiled:','exit 0')
            Shell('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fil('/작업/자바.txt')
            Shell('cd 작업; echo "echo script > kjøring_KR" > Kommando.sh; echo "false || echo recovered >> kjøring_KR" >> Kommando.sh; sh Kommando.sh')
            assert Fil('kjøring_KR')==b'script\nrecovered\n'
            Shell('rm kjøring_KR; echo "exit 7" > Utgang_app.sh; sh Utgang_app.sh; echo $?','7\n')
            Shell('rm Utgang_app.sh Kommando.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validering_rapport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            Shell('echo history-proof','history-proof')
            KR=sende(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert KR.count('history-proof')>=2, KR
            sende(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            KR=sende(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in KR, KR
            KR=sende(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in KR,KR
            KR=sende('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in KR,KR
            긴글='한글'*50
            KR=sende(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in KR
            Shell('terminal','TERMINAL READY')
            Shell('clear')
            Shell('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as strøm_VERDI:
                    json.loads(strøm_VERDI.readline())
                    def 호출(Navn,argument_MATRISE=None):
                        nettverk_e_post={'execute':Navn}
                        if argument_MATRISE: nettverk_e_post['arguments']=argument_MATRISE
                        strøm_VERDI.write((json.dumps(nettverk_e_post)+'\n').encode()); strøm_VERDI.flush()
                        while True:
                            svar=json.loads(strøm_VERDI.readline())
                            if 'error' in svar: raise AssertionError(svar)
                            if 'return' in svar: return svar['return']
                    호출('qmp_capabilities')
                    BILDE=produksjon/'terminal.ppm'; 호출('screendump',{'filename':str(BILDE),'format':'ppm'})
                    호출('screendump',{'filename':str(produksjon/'terminal.png'),'format':'png'})
                    data=BILDE.read_bytes().split(b'\n',3)[3]
                    def piksel(x_koordinat,Y_koordinat): return tuple(data[(Y_koordinat*640+x_koordinat)*3:(Y_koordinat*640+x_koordinat)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(x_koordinat,Y_koordinat) for Y_koordinat in range(100,116) for x_koordinat in range(24,56)))>1,'Hangul glyphs missing'
                    Shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    Shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(BILDE),'format':'ppm'})
                    복원자료=BILDE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    Shell('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): Shell('echo scroll-'+str(순번),'scroll-'+str(순번))
                    sende(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(produksjon/'terminal-scroll.png'),'format':'png'})
                    KR=sende(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in KR,KR
                    Shell('rm visible.txt')
                    호출('quit')
            Prosess.wait(timeout=5)
            validering_rapport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validering_rapport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Prosess.poll() is None:
                Prosess.terminate()
                try: Prosess.wait(timeout=5)
                except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait()
            준비살피미.close(); Prosess.stdin.close(); Prosess.stdout.close()
            (produksjon/'serial.log').write_bytes(utskrift)
            (produksjon/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Kjør_2()
