#!/usr/bin/env python3
"""자체 커널의 ᎤᏯᏍᎦ, 프로세스 I_O, Unicode GUI 터미널을 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준, ᎤᏁᏤᎸᎩ


def ᎠᎢᏎᏍᏗ():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ᎢᏯᏛᏁᎵᏓᏍᏗ = subprocess.Popen(ᎤᏁᏤᎸᎩ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ᎦᏟᏌᏅᎯ=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in ᎦᏟᏌᏅᎯ:
                if time.monotonic()>끝위치 or ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is not None: raise AssertionError('UART timeout/exit: '+ᎦᏟᏌᏅᎯ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ᎦᏟᏌᏅᎯ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ᎦᏟᏌᏅᎯ or b'FAIL ' in ᎦᏟᏌᏅᎯ: raise AssertionError(ᎦᏟᏌᏅᎯ)
            return ᎦᏟᏌᏅᎯ.decode('utf-8','replace').replace('\r\n','\n')
        def ᏫᎦᏅᏗ(ᎦᏟᏌᏅᎯ, 확인표시=b'jkoros-native> '):
            ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᎦᏟᏌᏅᎯ); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush(); return 수신하기(확인표시)
        def ᎤᏯᏍᎦ(ᏚᏓᏅᏅᎢ, *예상결과):
            결과=ᏫᎦᏅᏗ(ᏚᏓᏅᏅᎢ.encode()+b'\n')
            for ᏧᎬᏩᎶᏗᏯ in 예상결과: assert ᏧᎬᏩᎶᏗᏯ in 결과, (ᏚᏓᏅᏅᎢ,ᏧᎬᏩᎶᏗᏯ,결과)
            return 결과
        def ᎠᏍᏆᏂᎪᏙᏗ(ᏚᏙᎥᎢ):
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('hex '+ᏚᏙᎥᎢ,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',ᎠᎪᎵᏰᏗ,re.S)
            ᎦᏟᏌᏅᎯ=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(ᎦᏟᏌᏅᎯ)==int(찾은결과.group(1)); return ᎦᏟᏌᏅᎯ
        try:
            수신하기(b'jkoros-native> ')
            ᎤᏯᏍᎦ('mkdir 작업; cd 작업; pwd','/작업')
            ᎤᏯᏍᎦ('mkdir 하위; echo "한글 ᎦᏟᏌᏅᎯ 😀" > 인사.txt')
            assert ᎠᏍᏆᏂᎪᏙᏗ('인사.txt')=='한글 ᎦᏟᏌᏅᎯ 😀\n'.encode()
            ᎤᏯᏍᎦ('cp 인사.txt ᏗᏟᎶᏍᏔᏅᎯ_ᏧᎬᏩᎶᏗᏯ.txt; mv ᏗᏟᎶᏍᏔᏅᎯ_ᏧᎬᏩᎶᏗᏯ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ᎦᏟᏌᏅᎯ 😀')
            ᎤᏯᏍᎦ('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ᎦᏟᏌᏅᎯ 😀','/작업/하위')
            ᎤᏯᏍᎦ('cd ..; rmdir 하위; echo $?','1\n')
            ᎤᏯᏍᎦ('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ᎤᏯᏍᎦ('cp 인사.txt 인사.txt; echo $?','1\n'); assert ᎠᏍᏆᏂᎪᏙᏗ('인사.txt')=='한글 ᎦᏟᏌᏅᎯ 😀\n'.encode()
            ᎤᏯᏍᎦ('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ᎠᏍᏆᏂᎪᏙᏗ('인사.txt')
            ᎤᏯᏍᎦ("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ᎠᏍᏆᏂᎪᏙᏗ('리터럴')=='$인사\n누리\n'.encode()
            ᎤᏯᏍᎦ('echo one > ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ; echo two >> ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ; echo three >> ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ')
            ᎤᏯᏍᎦ('cat < ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ | grep t | tee 추림 | wc -l','2\n'); assert ᎠᏍᏆᏂᎪᏙᏗ('추림')==b'two\nthree\n'
            ᎤᏯᏍᎦ('head -n 1 ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ > 앞; tail -n 1 ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ > ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ'); assert ᎠᏍᏆᏂᎪᏙᏗ('앞')==b'one\n'; assert ᎠᏍᏆᏂᎪᏙᏗ('뒤')==b'three\n'
            ᎤᏯᏍᎦ('grep absent ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ; echo $?','1\n')
            ᎤᏯᏍᎦ('echo untouched > ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ')
            ᎤᏯᏍᎦ('echo destroyed > ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ |','명령이 빠졌습니다'); assert ᎠᏍᏆᏂᎪᏙᏗ('ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ')==b'untouched\n'
            ᎤᏯᏍᎦ('echo "oops','따옴표가 닫히지 않았습니다')
            ᎤᏯᏍᎦ('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ᎤᏯᏍᎦ('echo bad 2> ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ','번호를 지정한 ᎠᏍᏆᏂᎪᏙᏗ 서술자 I_O ᎦᏁᏟᏴᏍᏗ_ᎬᏙᏗ'); assert ᎠᏍᏆᏂᎪᏙᏗ('ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ')==b'untouched\n'
            ᎤᏯᏍᎦ('rm 빈파일 리터럴 ᎧᏁᏨᎯ_ᏧᎬᏩᎶᏗᏯ 추림 앞 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ ᎠᏓᎦᏎᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ᎤᏯᏍᎦ("python -c 'print(123)' | wc -c",'4\n')
            ᎤᏯᏍᎦ("python -c 'print(456)' > ᎬᏙᏗ_f5044b9b.txt"); assert ᎠᏍᏆᏂᎪᏙᏗ('ᎬᏙᏗ_f5044b9b.txt')==b'456\n'
            ᎤᏯᏍᎦ("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ᎤᏯᏍᎦ("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ᎬᏙᏗ_f5044b9b.txt", "b'456\\n'", "b''")
            ᎤᏯᏍᎦ("python -c 'print(\"x\"*17000)' | wc -c", 'ᎦᎵᏓᏍᏔᏅ -28')
            ᎤᏯᏍᎦ('echo recovered | wc -c','10\n')
            ᎤᏯᏍᎦ("python -c 'import jkoros; print(jkoros.read("+'"/작업/ᎬᏙᏗ_f5044b9b.txt"'+"))'",'456','exit 0')
            ᎤᏯᏍᎦ('cd /; javac Hello.java','Compiled:','exit 0')
            ᎤᏯᏍᎦ('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ᎠᏍᏆᏂᎪᏙᏗ('/작업/자바.txt')
            ᎤᏯᏍᎦ('cd 작업; echo "echo script > 실행결과" > ᎤᏁᏤᎸᎩ.sh; echo "false || echo recovered >> 실행결과" >> ᎤᏁᏤᎸᎩ.sh; sh ᎤᏁᏤᎸᎩ.sh')
            assert ᎠᏍᏆᏂᎪᏙᏗ('실행결과')==b'script\nrecovered\n'
            ᎤᏯᏍᎦ('rm 실행결과; echo "exit 7" > ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.sh; sh ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.sh; echo $?','7\n')
            ᎤᏯᏍᎦ('rm ᎦᏅᎪᎢᏍᏗ_ᎬᏙᏗ.sh ᎤᏁᏤᎸᎩ.sh ᎬᏙᏗ_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ᎤᏯᏍᎦ('echo history-proof','history-proof')
            결과=ᏫᎦᏅᏗ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            ᏫᎦᏅᏗ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=ᏫᎦᏅᏗ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=ᏫᎦᏅᏗ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=ᏫᎦᏅᏗ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=ᏫᎦᏅᏗ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            ᎤᏯᏍᎦ('terminal','TERMINAL READY')
            ᎤᏯᏍᎦ('clear')
            ᎤᏯᏍᎦ('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as ᎠᏥᏍᏕᎵᏍᎩ:
                ᎠᏥᏍᏕᎵᏍᎩ.settimeout(10); ᎠᏥᏍᏕᎵᏍᎩ.connect(str(모의제어접속))
                with ᎠᏥᏍᏕᎵᏍᎩ.makefile('rwb') as ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ:
                    json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                    def 호출(ᏚᏙᎥᎢ,ᏗᏓᎦᏘᎸᏍᏗ_array=None):
                        ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ={'execute':ᏚᏙᎥᎢ}
                        if ᏗᏓᎦᏘᎸᏍᏗ_array: ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ['arguments']=ᏗᏓᎦᏘᎸᏍᏗ_array
                        ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.write((json.dumps(ᏧᎾᏚᏓᎵ_ᎠᎪᎵᏰᏗ)+'\n').encode()); ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.flush()
                        while True:
                            응답=json.loads(ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    ᎤᏓᏴᎳᏛ=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ᎤᏓᏴᎳᏛ),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ᎦᏟᏌᏅᎯ=ᎤᏓᏴᎳᏛ.read_bytes().split(b'\n',3)[3]
                    def pel(가로좌표,세로좌표): return tuple(ᎦᏟᏌᏅᎯ[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    ᎤᏯᏍᎦ('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ᎤᏯᏍᎦ("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ᎤᏓᏴᎳᏛ),'format':'ppm'})
                    복원자료=ᎤᏓᏴᎳᏛ.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ᎤᏯᏍᎦ('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ᎤᏯᏍᎦ('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ᏫᎦᏅᏗ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=ᏫᎦᏅᏗ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    ᎤᏯᏍᎦ('rm visible.txt')
                    호출('quit')
            ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is None:
                ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
                try: ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
                except subprocess.TimeoutExpired: ᎢᏯᏛᏁᎵᏓᏍᏗ.kill(); ᎢᏯᏛᏁᎵᏓᏍᏗ.wait()
            준비살피미.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ᎠᎢᏎᏍᏗ()
