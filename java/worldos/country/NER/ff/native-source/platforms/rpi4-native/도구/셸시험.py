#!/usr/bin/env python3
"""자체 커널의 laalagal, 프로세스 I_O, Unicode GUI 터미널을 laatii_keɓe raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 실행 import 기준, ginol


def huutoraade():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    teeŋtingol_ciimtol = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Yuɓɓo_golle = subprocess.Popen(ginol()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Yuɓɓo_golle.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            keɓe=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in keɓe:
                if time.monotonic()>끝위치 or Yuɓɓo_golle.poll() is not None: raise AssertionError('UART timeout/exit: '+keɓe.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: keɓe.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in keɓe or b'FAIL ' in keɓe: raise AssertionError(keɓe)
            return keɓe.decode('utf-8','replace').replace('\r\n','\n')
        def neldude(keɓe, 확인표시=b'jkoros-native> '):
            Yuɓɓo_golle.stdin.write(keɓe); Yuɓɓo_golle.stdin.flush(); return 수신하기(확인표시)
        def laalagal(diidol, *예상결과):
            결과=neldude(diidol.encode()+b'\n')
            for njaru in 예상결과: assert njaru in 결과, (diidol,njaru,결과)
            return 결과
        def fiilde(innde):
            binndi=laalagal('hex '+innde,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',binndi,re.S)
            keɓe=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(keɓe)==int(찾은결과.group(1)); return keɓe
        try:
            수신하기(b'jkoros-native> ')
            laalagal('mkdir 작업; cd 작업; pwd','/작업')
            laalagal('mkdir 하위; echo "한글 keɓe 😀" > 인사.txt')
            assert fiilde('인사.txt')=='한글 keɓe 😀\n'.encode()
            laalagal('cp 인사.txt waanjitaade_njaru.txt; mv waanjitaade_njaru.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 keɓe 😀')
            laalagal('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 keɓe 😀','/작업/하위')
            laalagal('cd ..; rmdir 하위; echo $?','1\n')
            laalagal('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            laalagal('cp 인사.txt 인사.txt; echo $?','1\n'); assert fiilde('인사.txt')=='한글 keɓe 😀\n'.encode()
            laalagal('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in fiilde('인사.txt')
            laalagal("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert fiilde('리터럴')=='$인사\n누리\n'.encode()
            laalagal('echo one > konngol_njaru; echo two >> konngol_njaru; echo three >> konngol_njaru')
            laalagal('cat < konngol_njaru | grep t | tee 추림 | wc -l','2\n'); assert fiilde('추림')==b'two\nthree\n'
            laalagal('head -n 1 konngol_njaru > 앞; tail -n 1 konngol_njaru > Caggal_njaru'); assert fiilde('앞')==b'one\n'; assert fiilde('뒤')==b'three\n'
            laalagal('grep absent konngol_njaru; echo $?','1\n')
            laalagal('echo untouched > suurde_njaru')
            laalagal('echo destroyed > suurde_njaru |','명령이 빠졌습니다'); assert fiilde('suurde_njaru')==b'untouched\n'
            laalagal('echo "oops','따옴표가 닫히지 않았습니다')
            laalagal('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            laalagal('echo bad 2> suurde_njaru','번호를 지정한 fiilde 서술자 I_O waylude_modd'); assert fiilde('suurde_njaru')==b'untouched\n'
            laalagal('rm 빈파일 리터럴 konngol_njaru 추림 앞 Caggal_njaru suurde_njaru')
            teeŋtingol_ciimtol['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            laalagal("python -c 'print(123)' | wc -c",'4\n')
            laalagal("python -c 'print(456)' > tafirde_f5044b9b.txt"); assert fiilde('tafirde_f5044b9b.txt')==b'456\n'
            laalagal("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            laalagal("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < tafirde_f5044b9b.txt", "b'456\\n'", "b''")
            laalagal("python -c 'print(\"x\"*17000)' | wc -c", 'juumre -28')
            laalagal('echo recovered | wc -c','10\n')
            laalagal("python -c 'import jkoros; print(jkoros.read("+'"/작업/tafirde_f5044b9b.txt"'+"))'",'456','exit 0')
            laalagal('cd /; javac Hello.java','Compiled:','exit 0')
            laalagal('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in fiilde('/작업/자바.txt')
            laalagal('cd 작업; echo "echo script > 실행결과" > ginol.sh; echo "false || echo recovered >> 실행결과" >> ginol.sh; sh ginol.sh')
            assert fiilde('실행결과')==b'script\nrecovered\n'
            laalagal('rm 실행결과; echo "exit 7" > yaltude_tafirde.sh; sh yaltude_tafirde.sh; echo $?','7\n')
            laalagal('rm yaltude_tafirde.sh ginol.sh tafirde_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            teeŋtingol_ciimtol['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            laalagal('echo history-proof','history-proof')
            결과=neldude(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            neldude(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=neldude(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=neldude(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=neldude('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=neldude(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            laalagal('terminal','TERMINAL READY')
            laalagal('clear')
            laalagal('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as kiliyaan:
                kiliyaan.settimeout(10); kiliyaan.connect(str(모의제어접속))
                with kiliyaan.makefile('rwb') as waraango_njaru:
                    json.loads(waraango_njaru.readline())
                    def 호출(innde,인수배열=None):
                        laylaytol_ɓatakuru={'execute':innde}
                        if 인수배열: laylaytol_ɓatakuru['arguments']=인수배열
                        waraango_njaru.write((json.dumps(laylaytol_ɓatakuru)+'\n').encode()); waraango_njaru.flush()
                        while True:
                            응답=json.loads(waraango_njaru.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    natal=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(natal),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    keɓe=natal.read_bytes().split(b'\n',3)[3]
                    def piksel(가로좌표,세로좌표): return tuple(keɓe[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    laalagal('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    laalagal("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(natal),'format':'ppm'})
                    복원자료=natal.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    laalagal('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): laalagal('echo scroll-'+str(순번),'scroll-'+str(순번))
                    neldude(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=neldude(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    laalagal('rm visible.txt')
                    호출('quit')
            Yuɓɓo_golle.wait(timeout=5)
            teeŋtingol_ciimtol['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            teeŋtingol_ciimtol['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Yuɓɓo_golle.poll() is None:
                Yuɓɓo_golle.terminate()
                try: Yuɓɓo_golle.wait(timeout=5)
                except subprocess.TimeoutExpired: Yuɓɓo_golle.kill(); Yuɓɓo_golle.wait()
            준비살피미.close(); Yuɓɓo_golle.stdin.close(); Yuɓɓo_golle.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(teeŋtingol_ciimtol,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': huutoraade()
