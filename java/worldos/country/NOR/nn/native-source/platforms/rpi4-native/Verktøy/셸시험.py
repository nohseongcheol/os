#!/usr/bin/env python3
"""자체 커널의 grensesnitt, 프로세스 I_U, Unicode GUI 터미널을 faktisk_data raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from Utfør_kommando import spegle_rot, Kommando


def Køyr_2():
    출력결과 = spegle_rot / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    validering_rapport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Prosess = subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Prosess.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            data=bytearray(); avslutte_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in data:
                if time.monotonic()>avslutte_OFFSET or Prosess.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def sende(data, 확인표시=b'jkoros-native> '):
            Prosess.stdin.write(data); Prosess.stdin.flush(); return 수신하기(확인표시)
        def grensesnitt(linje, *예상결과):
            forretningsmål=sende(linje.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in forretningsmål, (linje,VALUE,forretningsmål)
            return forretningsmål
        def Fil(Namn):
            Tekst=grensesnitt('hex '+Namn,'HEX BEGIN','HEX END'); Søk_forretningsmål=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Tekst,re.S)
            data=bytes.fromhex(''.join(Søk_forretningsmål.group(2).split())); assert len(data)==int(Søk_forretningsmål.group(1)); return data
        try:
            수신하기(b'jkoros-native> ')
            grensesnitt('mkdir 작업; cd 작업; pwd','/작업')
            grensesnitt('mkdir 하위; echo "한글 data 😀" > 인사.txt')
            assert Fil('인사.txt')=='한글 data 😀\n'.encode()
            grensesnitt('cp 인사.txt kopiere_VALUE.txt; mv kopiere_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 data 😀')
            grensesnitt('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 data 😀','/작업/하위')
            grensesnitt('cd ..; rmdir 하위; echo $?','1\n')
            grensesnitt('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            grensesnitt('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fil('인사.txt')=='한글 data 😀\n'.encode()
            grensesnitt('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fil('인사.txt')
            grensesnitt("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fil('리터럴')=='$인사\n누리\n'.encode()
            grensesnitt('echo one > uttrykk_VALUE; echo two >> uttrykk_VALUE; echo three >> uttrykk_VALUE')
            grensesnitt('cat < uttrykk_VALUE | grep t | tee 추림 | wc -l','2\n'); assert Fil('추림')==b'two\nthree\n'
            grensesnitt('head -n 1 uttrykk_VALUE > 앞; tail -n 1 uttrykk_VALUE > TILBAKE_VALUE'); assert Fil('앞')==b'one\n'; assert Fil('뒤')==b'three\n'
            grensesnitt('grep absent uttrykk_VALUE; echo $?','1\n')
            grensesnitt('echo untouched > verne_VALUE')
            grensesnitt('echo destroyed > verne_VALUE |','명령이 빠졌습니다'); assert Fil('verne_VALUE')==b'untouched\n'
            grensesnitt('echo "oops','따옴표가 닫히지 않았습니다')
            grensesnitt('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            grensesnitt('echo bad 2> verne_VALUE','번호를 지정한 Fil 서술자 I_U byte_MODE'); assert Fil('verne_VALUE')==b'untouched\n'
            grensesnitt('rm 빈파일 리터럴 uttrykk_VALUE 추림 앞 TILBAKE_VALUE verne_VALUE')
            validering_rapport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            grensesnitt("python -c 'print(123)' | wc -c",'4\n')
            grensesnitt("python -c 'print(456)' > app_f5044b9b.txt"); assert Fil('app_f5044b9b.txt')==b'456\n'
            grensesnitt("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            grensesnitt("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < app_f5044b9b.txt", "b'456\\n'", "b''")
            grensesnitt("python -c 'print(\"x\"*17000)' | wc -c", 'FEIL -28')
            grensesnitt('echo recovered | wc -c','10\n')
            grensesnitt("python -c 'import jkoros; print(jkoros.read("+'"/작업/app_f5044b9b.txt"'+"))'",'456','exit 0')
            grensesnitt('cd /; javac Hello.java','Compiled:','exit 0')
            grensesnitt('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fil('/작업/자바.txt')
            grensesnitt('cd 작업; echo "echo script > 실행결과" > Kommando.sh; echo "false || echo recovered >> 실행결과" >> Kommando.sh; sh Kommando.sh')
            assert Fil('실행결과')==b'script\nrecovered\n'
            grensesnitt('rm 실행결과; echo "exit 7" > Utgang_app.sh; sh Utgang_app.sh; echo $?','7\n')
            grensesnitt('rm Utgang_app.sh Kommando.sh app_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            validering_rapport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            grensesnitt('echo history-proof','history-proof')
            forretningsmål=sende(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert forretningsmål.count('history-proof')>=2, forretningsmål
            sende(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            forretningsmål=sende(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in forretningsmål, forretningsmål
            forretningsmål=sende(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in forretningsmål,forretningsmål
            forretningsmål=sende('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in forretningsmål,forretningsmål
            긴글='한글'*50
            forretningsmål=sende(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in forretningsmål
            grensesnitt('terminal','TERMINAL READY')
            grensesnitt('clear')
            grensesnitt('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as klient:
                klient.settimeout(10); klient.connect(str(모의제어접속))
                with klient.makefile('rwb') as Stream_VALUE:
                    json.loads(Stream_VALUE.readline())
                    def 호출(Namn,argument_ARRAY=None):
                        Nettverk_melding={'execute':Namn}
                        if argument_ARRAY: Nettverk_melding['arguments']=argument_ARRAY
                        Stream_VALUE.write((json.dumps(Nettverk_melding)+'\n').encode()); Stream_VALUE.flush()
                        while True:
                            svare=json.loads(Stream_VALUE.readline())
                            if 'error' in svare: raise AssertionError(svare)
                            if 'return' in svare: return svare['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    data=IMAGE.read_bytes().split(b'\n',3)[3]
                    def piksel(x_koordinat,Y_koordinat): return tuple(data[(Y_koordinat*640+x_koordinat)*3:(Y_koordinat*640+x_koordinat)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(x_koordinat,Y_koordinat) for Y_koordinat in range(100,116) for x_koordinat in range(24,56)))>1,'Hangul glyphs missing'
                    grensesnitt('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    grensesnitt("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    grensesnitt('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): grensesnitt('echo scroll-'+str(순번),'scroll-'+str(순번))
                    sende(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    forretningsmål=sende(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in forretningsmål,forretningsmål
                    grensesnitt('rm visible.txt')
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
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Køyr_2()
