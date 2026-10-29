#!/usr/bin/env python3
"""자체 커널의 ṣẹ́ẹ̀lì, 프로세스 I_O, Unicode GUI 터미널을 gangan_détà raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ṣiṣẹ́_àṣẹ import 기준, Àṣẹ


def Rọ́ọ̀nù():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    Àfọwọ́sí_ìjábọ̀ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Ìlànà = subprocess.Popen(Àṣẹ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Ìlànà.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            détà=bytearray(); parí_Ìtayọ=time.monotonic()+시간제한
            while 확인표시 not in détà:
                if time.monotonic()>parí_Ìtayọ or Ìlànà.poll() is not None: raise AssertionError('UART timeout/exit: '+détà.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: détà.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in détà or b'FAIL ' in détà: raise AssertionError(détà)
            return détà.decode('utf-8','replace').replace('\r\n','\n')
        def í_meèlì(détà, 확인표시=b'jkoros-native> '):
            Ìlànà.stdin.write(détà); Ìlànà.stdin.flush(); return 수신하기(확인표시)
        def ṣẹ́ẹ̀lì(ìlà, *예상결과):
            결과=í_meèlì(ìlà.encode()+b'\n')
            for iye in 예상결과: assert iye in 결과, (ìlà,iye,결과)
            return 결과
        def Fáìlì(Orúkọ):
            SMS=ṣẹ́ẹ̀lì('hex '+Orúkọ,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',SMS,re.S)
            détà=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(détà)==int(찾은결과.group(1)); return détà
        try:
            수신하기(b'jkoros-native> ')
            ṣẹ́ẹ̀lì('mkdir 작업; cd 작업; pwd','/작업')
            ṣẹ́ẹ̀lì('mkdir 하위; echo "한글 détà 😀" > 인사.txt')
            assert Fáìlì('인사.txt')=='한글 détà 😀\n'.encode()
            ṣẹ́ẹ̀lì('cp 인사.txt ṣẹ̀dà_iye.txt; mv ṣẹ̀dà_iye.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 détà 😀')
            ṣẹ́ẹ̀lì('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 détà 😀','/작업/하위')
            ṣẹ́ẹ̀lì('cd ..; rmdir 하위; echo $?','1\n')
            ṣẹ́ẹ̀lì('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            ṣẹ́ẹ̀lì('cp 인사.txt 인사.txt; echo $?','1\n'); assert Fáìlì('인사.txt')=='한글 détà 😀\n'.encode()
            ṣẹ́ẹ̀lì('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Fáìlì('인사.txt')
            ṣẹ́ẹ̀lì("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Fáìlì('리터럴')=='$인사\n누리\n'.encode()
            ṣẹ́ẹ̀lì('echo one > àlàyé_iye; echo two >> àlàyé_iye; echo three >> àlàyé_iye')
            ṣẹ́ẹ̀lì('cat < àlàyé_iye | grep t | tee 추림 | wc -l','2\n'); assert Fáìlì('추림')==b'two\nthree\n'
            ṣẹ́ẹ̀lì('head -n 1 àlàyé_iye > 앞; tail -n 1 àlàyé_iye > Padà_sẹ́yìn_iye'); assert Fáìlì('앞')==b'one\n'; assert Fáìlì('뒤')==b'three\n'
            ṣẹ́ẹ̀lì('grep absent àlàyé_iye; echo $?','1\n')
            ṣẹ́ẹ̀lì('echo untouched > dáàbòbò_iye')
            ṣẹ́ẹ̀lì('echo destroyed > dáàbòbò_iye |','명령이 빠졌습니다'); assert Fáìlì('dáàbòbò_iye')==b'untouched\n'
            ṣẹ́ẹ̀lì('echo "oops','따옴표가 닫히지 않았습니다')
            ṣẹ́ẹ̀lì('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            ṣẹ́ẹ̀lì('echo bad 2> dáàbòbò_iye','번호를 지정한 Fáìlì 서술자 I_O ṣèpapòdà_móòdù'); assert Fáìlì('dáàbòbò_iye')==b'untouched\n'
            ṣẹ́ẹ̀lì('rm 빈파일 리터럴 àlàyé_iye 추림 앞 Padà_sẹ́yìn_iye dáàbòbò_iye')
            Àfọwọ́sí_ìjábọ̀['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            ṣẹ́ẹ̀lì("python -c 'print(123)' | wc -c",'4\n')
            ṣẹ́ẹ̀lì("python -c 'print(456)' > àtòjọ_ètò_f5044b9b.txt"); assert Fáìlì('àtòjọ_ètò_f5044b9b.txt')==b'456\n'
            ṣẹ́ẹ̀lì("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            ṣẹ́ẹ̀lì("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < àtòjọ_ètò_f5044b9b.txt", "b'456\\n'", "b''")
            ṣẹ́ẹ̀lì("python -c 'print(\"x\"*17000)' | wc -c", 'àṣìṣe -28')
            ṣẹ́ẹ̀lì('echo recovered | wc -c','10\n')
            ṣẹ́ẹ̀lì("python -c 'import jkoros; print(jkoros.read("+'"/작업/àtòjọ_ètò_f5044b9b.txt"'+"))'",'456','exit 0')
            ṣẹ́ẹ̀lì('cd /; javac Hello.java','Compiled:','exit 0')
            ṣẹ́ẹ̀lì('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Fáìlì('/작업/자바.txt')
            ṣẹ́ẹ̀lì('cd 작업; echo "echo script > 실행결과" > Àṣẹ.sh; echo "false || echo recovered >> 실행결과" >> Àṣẹ.sh; sh Àṣẹ.sh')
            assert Fáìlì('실행결과')==b'script\nrecovered\n'
            ṣẹ́ẹ̀lì('rm 실행결과; echo "exit 7" > jáde_àtòjọ_ètò.sh; sh jáde_àtòjọ_ètò.sh; echo $?','7\n')
            ṣẹ́ẹ̀lì('rm jáde_àtòjọ_ètò.sh Àṣẹ.sh àtòjọ_ètò_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            Àfọwọ́sí_ìjábọ̀['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            ṣẹ́ẹ̀lì('echo history-proof','history-proof')
            결과=í_meèlì(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            í_meèlì(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=í_meèlì(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=í_meèlì(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=í_meèlì('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=í_meèlì(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            ṣẹ́ẹ̀lì('terminal','TERMINAL READY')
            ṣẹ́ẹ̀lì('clear')
            ṣẹ́ẹ̀lì('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as aṣojú:
                aṣojú.settimeout(10); aṣojú.connect(str(모의제어접속))
                with aṣojú.makefile('rwb') as Stream_iye:
                    json.loads(Stream_iye.readline())
                    def 호출(Orúkọ,ágúmẹ́ntì_ÀRÉÈ=None):
                        Alásopọ̀_iṣé={'execute':Orúkọ}
                        if ágúmẹ́ntì_ÀRÉÈ: Alásopọ̀_iṣé['arguments']=ágúmẹ́ntì_ÀRÉÈ
                        Stream_iye.write((json.dumps(Alásopọ̀_iṣé)+'\n').encode()); Stream_iye.flush()
                        while True:
                            Fèsì=json.loads(Stream_iye.readline())
                            if 'error' in Fèsì: raise AssertionError(Fèsì)
                            if 'return' in Fèsì: return Fèsì['return']
                    호출('qmp_capabilities')
                    àwòrán=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(àwòrán),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    détà=àwòrán.read_bytes().split(b'\n',3)[3]
                    def píkísẹ̀(ibi_ìtọ́kasí_x,세로좌표): return tuple(détà[(세로좌표*640+ibi_ìtọ́kasí_x)*3:(세로좌표*640+ibi_ìtọ́kasí_x)*3+3])
                    assert píkísẹ̀(12,48)==(32,80,144),píkísẹ̀(12,48)
                    assert len(set(píkísẹ̀(ibi_ìtọ́kasí_x,세로좌표) for 세로좌표 in range(100,116) for ibi_ìtọ́kasí_x in range(24,56)))>1,'Hangul glyphs missing'
                    ṣẹ́ẹ̀lì('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    ṣẹ́ẹ̀lì("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(àwòrán),'format':'ppm'})
                    복원자료=àwòrán.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    ṣẹ́ẹ̀lì('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): ṣẹ́ẹ̀lì('echo scroll-'+str(순번),'scroll-'+str(순번))
                    í_meèlì(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=í_meèlì(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    ṣẹ́ẹ̀lì('rm visible.txt')
                    호출('quit')
            Ìlànà.wait(timeout=5)
            Àfọwọ́sí_ìjábọ̀['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            Àfọwọ́sí_ìjábọ̀['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Ìlànà.poll() is None:
                Ìlànà.terminate()
                try: Ìlànà.wait(timeout=5)
                except subprocess.TimeoutExpired: Ìlànà.kill(); Ìlànà.wait()
            준비살피미.close(); Ìlànà.stdin.close(); Ìlànà.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Rọ́ọ̀nù()
