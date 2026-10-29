#!/usr/bin/env python3
"""자체 커널의 slige, 프로세스 I_O, Unicode GUI 터미널을 dearbh_dàta raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from gnìomhaich_àithne import tilg_freumh, àithne


def ruith():
    출력결과 = tilg_freumh / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    dearbhadh_aithisg = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Pròiseas = subprocess.Popen(àithne()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Pròiseas.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            dàta=bytearray(); crìochnaich_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in dàta:
                if time.monotonic()>crìochnaich_OFFSET or Pròiseas.poll() is not None: raise AssertionError('UART timeout/exit: '+dàta.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: dàta.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in dàta or b'FAIL ' in dàta: raise AssertionError(dàta)
            return dàta.decode('utf-8','replace').replace('\r\n','\n')
        def cuir(dàta, 확인표시=b'jkoros-native> '):
            Pròiseas.stdin.write(dàta); Pròiseas.stdin.flush(); return 수신하기(확인표시)
        def slige(loidhne, *예상결과):
            tomhas=cuir(loidhne.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in tomhas, (loidhne,VALUE,tomhas)
            return tomhas
        def faidhle(Ainm):
            SMS=slige('hex '+Ainm,'HEX BEGIN','HEX END'); lorg_tomhas=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            dàta=bytes.fromhex(''.join(lorg_tomhas.group(2).split())); assert len(dàta)==int(lorg_tomhas.group(1)); return dàta
        try:
            수신하기(b'jkoros-native> ')
            slige('mkdir 작업; cd 작업; pwd','/작업')
            slige('mkdir 하위; echo "한글 dàta 😀" > 인사.txt')
            assert faidhle('인사.txt')=='한글 dàta 😀\n'.encode()
            slige('cp 인사.txt ionstans_VALUE.txt; mv ionstans_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 dàta 😀')
            slige('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 dàta 😀','/작업/하위')
            slige('cd ..; rmdir 하위; echo $?','1\n')
            slige('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            slige('cp 인사.txt 인사.txt; echo $?','1\n'); assert faidhle('인사.txt')=='한글 dàta 😀\n'.encode()
            slige('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in faidhle('인사.txt')
            slige("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert faidhle('리터럴')=='$인사\n누리\n'.encode()
            slige('echo one > aithris_VALUE; echo two >> aithris_VALUE; echo three >> aithris_VALUE')
            slige('cat < aithris_VALUE | grep t | tee 추림 | wc -l','2\n'); assert faidhle('추림')==b'two\nthree\n'
            slige('head -n 1 aithris_VALUE > 앞; tail -n 1 aithris_VALUE > Air_ais_VALUE'); assert faidhle('앞')==b'one\n'; assert faidhle('뒤')==b'three\n'
            slige('grep absent aithris_VALUE; echo $?','1\n')
            slige('echo untouched > dìon_VALUE')
            slige('echo destroyed > dìon_VALUE |','명령이 빠졌습니다'); assert faidhle('dìon_VALUE')==b'untouched\n'
            slige('echo "oops','따옴표가 닫히지 않았습니다')
            slige('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            slige('echo bad 2> dìon_VALUE','번호를 지정한 faidhle 서술자 I_O SWITCH_MODE'); assert faidhle('dìon_VALUE')==b'untouched\n'
            slige('rm 빈파일 리터럴 aithris_VALUE 추림 앞 Air_ais_VALUE dìon_VALUE')
            dearbhadh_aithisg['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            slige("python -c 'print(123)' | wc -c",'4\n')
            slige("python -c 'print(456)' > ap_f5044b9b.txt"); assert faidhle('ap_f5044b9b.txt')==b'456\n'
            slige("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            slige("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ap_f5044b9b.txt", "b'456\\n'", "b''")
            slige("python -c 'print(\"x\"*17000)' | wc -c", 'Mearachd -28')
            slige('echo recovered | wc -c','10\n')
            slige("python -c 'import jkoros; print(jkoros.read("+'"/작업/ap_f5044b9b.txt"'+"))'",'456','exit 0')
            slige('cd /; javac Hello.java','Compiled:','exit 0')
            slige('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in faidhle('/작업/자바.txt')
            slige('cd 작업; echo "echo script > 실행결과" > àithne.sh; echo "false || echo recovered >> 실행결과" >> àithne.sh; sh àithne.sh')
            assert faidhle('실행결과')==b'script\nrecovered\n'
            slige('rm 실행결과; echo "exit 7" > fàg_ap.sh; sh fàg_ap.sh; echo $?','7\n')
            slige('rm fàg_ap.sh àithne.sh ap_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            dearbhadh_aithisg['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            slige('echo history-proof','history-proof')
            tomhas=cuir(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert tomhas.count('history-proof')>=2, tomhas
            cuir(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            tomhas=cuir(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in tomhas, tomhas
            tomhas=cuir(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in tomhas,tomhas
            tomhas=cuir('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in tomhas,tomhas
            긴글='한글'*50
            tomhas=cuir(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in tomhas
            slige('terminal','TERMINAL READY')
            slige('clear')
            slige('echo "한글 tèirmineal ABC xyz 012 😀"','한글 tèirmineal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as cliant:
                cliant.settimeout(10); cliant.connect(str(모의제어접속))
                with cliant.makefile('rwb') as sruth_VALUE:
                    json.loads(sruth_VALUE.readline())
                    def 호출(Ainm,argamaid_ARRAY=None):
                        lìonra_teachdaireachd={'execute':Ainm}
                        if argamaid_ARRAY: lìonra_teachdaireachd['arguments']=argamaid_ARRAY
                        sruth_VALUE.write((json.dumps(lìonra_teachdaireachd)+'\n').encode()); sruth_VALUE.flush()
                        while True:
                            freagair=json.loads(sruth_VALUE.readline())
                            if 'error' in freagair: raise AssertionError(freagair)
                            if 'return' in freagair: return freagair['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    dàta=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pel(co_chomharra_x,세로좌표): return tuple(dàta[(세로좌표*640+co_chomharra_x)*3:(세로좌표*640+co_chomharra_x)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(co_chomharra_x,세로좌표) for 세로좌표 in range(100,116) for co_chomharra_x in range(24,56)))>1,'Hangul glyphs missing'
                    slige('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    slige("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    slige('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): slige('echo scroll-'+str(순번),'scroll-'+str(순번))
                    cuir(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    tomhas=cuir(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in tomhas,tomhas
                    slige('rm visible.txt')
                    호출('quit')
            Pròiseas.wait(timeout=5)
            dearbhadh_aithisg['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            dearbhadh_aithisg['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Pròiseas.poll() is None:
                Pròiseas.terminate()
                try: Pròiseas.wait(timeout=5)
                except subprocess.TimeoutExpired: Pròiseas.kill(); Pròiseas.wait()
            준비살피미.close(); Pròiseas.stdin.close(); Pròiseas.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ruith()
