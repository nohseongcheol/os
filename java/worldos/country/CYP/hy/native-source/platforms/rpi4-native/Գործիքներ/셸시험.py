#!/usr/bin/env python3
"""자체 커널의 խեցի, 프로세스 ներածում_արտածում, Unicode GUI 터미널을 իրական_տվյալ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from կատարել_հրաման import արձակել_արմատ, Հրահանգ


def Գործարկել():
    출력결과 = արձակել_արմատ / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    վավերացում_զեկույց = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((արձակել_արմատ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Գործընթաց = subprocess.Popen(Հրահանգ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Գործընթաց.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            տվյալ=bytearray(); վերջացնել_Տեղաշարժում=time.monotonic()+시간제한
            while 확인표시 not in տվյալ:
                if time.monotonic()>վերջացնել_Տեղաշարժում or Գործընթաց.poll() is not None: raise AssertionError('UART timeout/exit: '+տվյալ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: տվյալ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in տվյալ or b'FAIL ' in տվյալ: raise AssertionError(տվյալ)
            return տվյալ.decode('utf-8','replace').replace('\r\n','\n')
        def ուղարկել(տվյալ, 확인표시=b'jkoros-native> '):
            Գործընթաց.stdin.write(տվյալ); Գործընթաց.stdin.flush(); return 수신하기(확인표시)
        def խեցի(կապ, *예상결과):
            չափ=ուղարկել(կապ.encode()+b'\n')
            for արժեք in 예상결과: assert արժեք in չափ, (կապ,արժեք,չափ)
            return չափ
        def Ֆայլ(Անուն):
            Տեքստ=խեցի('hex '+Անուն,'HEX BEGIN','HEX END'); որոնել_չափ=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Տեքստ,re.S)
            տվյալ=bytes.fromhex(''.join(որոնել_չափ.group(2).split())); assert len(տվյալ)==int(որոնել_չափ.group(1)); return տվյալ
        try:
            수신하기(b'jkoros-native> ')
            խեցի('mkdir 작업; cd 작업; pwd','/작업')
            խեցի('mkdir 하위; echo "한글 տվյալ 😀" > 인사.txt')
            assert Ֆայլ('인사.txt')=='한글 տվյալ 😀\n'.encode()
            խեցի('cp 인사.txt պատճեն_արժեք.txt; mv պատճեն_արժեք.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 տվյալ 😀')
            խեցի('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 տվյալ 😀','/작업/하위')
            խեցի('cd ..; rmdir 하위; echo $?','1\n')
            խեցի('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            խեցի('cp 인사.txt 인사.txt; echo $?','1\n'); assert Ֆայլ('인사.txt')=='한글 տվյալ 😀\n'.encode()
            խեցի('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Ֆայլ('인사.txt')
            խեցի("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Ֆայլ('리터럴')=='$인사\n누리\n'.encode()
            խեցի('echo one > դրույթ_արժեք; echo two >> դրույթ_արժեք; echo three >> դրույթ_արժեք')
            խեցի('cat < դրույթ_արժեք | grep t | tee 추림 | wc -l','2\n'); assert Ֆայլ('추림')==b'two\nthree\n'
            խեցի('head -n 1 դրույթ_արժեք > 앞; tail -n 1 դրույթ_արժեք > Հետ_արժեք'); assert Ֆայլ('앞')==b'one\n'; assert Ֆայլ('뒤')==b'three\n'
            խեցի('grep absent դրույթ_արժեք; echo $?','1\n')
            խեցի('echo untouched > պաշտպանել_արժեք')
            խեցի('echo destroyed > պաշտպանել_արժեք |','명령이 빠졌습니다'); assert Ֆայլ('պաշտպանել_արժեք')==b'untouched\n'
            խեցի('echo "oops','따옴표가 닫히지 않았습니다')
            խեցի('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            խեցի('echo bad 2> պաշտպանել_արժեք','번호를 지정한 Ֆայլ 서술자 ներածում_արտածում փոխարկել_կերպ'); assert Ֆայլ('պաշտպանել_արժեք')==b'untouched\n'
            խեցի('rm 빈파일 리터럴 դրույթ_արժեք 추림 앞 Հետ_արժեք պաշտպանել_արժեք')
            վավերացում_զեկույց['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            խեցի("python -c 'print(123)' | wc -c",'4\n')
            խեցի("python -c 'print(456)' > ծրագիր_f5044b9b.txt"); assert Ֆայլ('ծրագիր_f5044b9b.txt')==b'456\n'
            խեցի("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            խեցի("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < ծրագիր_f5044b9b.txt", "b'456\\n'", "b''")
            խեցի("python -c 'print(\"x\"*17000)' | wc -c", 'Սխալ -28')
            խեցի('echo recovered | wc -c','10\n')
            խեցի("python -c 'import jkoros; print(jkoros.read("+'"/작업/ծրագիր_f5044b9b.txt"'+"))'",'456','exit 0')
            խեցի('cd /; javac Hello.java','Compiled:','exit 0')
            խեցի('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Ֆայլ('/작업/자바.txt')
            խեցի('cd 작업; echo "echo script > 실행결과" > Հրահանգ.sh; echo "false || echo recovered >> 실행결과" >> Հրահանգ.sh; sh Հրահանգ.sh')
            assert Ֆայլ('실행결과')==b'script\nrecovered\n'
            խեցի('rm 실행결과; echo "exit 7" > Ելք_ծրագիր.sh; sh Ելք_ծրագիր.sh; echo $?','7\n')
            խեցի('rm Ելք_ծրագիր.sh Հրահանգ.sh ծրագիր_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            վավերացում_զեկույց['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            խեցի('echo history-proof','history-proof')
            չափ=ուղարկել(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert չափ.count('history-proof')>=2, չափ
            ուղարկել(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            չափ=ուղարկել(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in չափ, չափ
            չափ=ուղարկել(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in չափ,չափ
            չափ=ուղարկել('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in չափ,չափ
            긴글='한글'*50
            չափ=ուղարկել(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in չափ
            խեցի('terminal','TERMINAL READY')
            խեցի('clear')
            խեցի('echo "한글 Տերմինալ ABC xyz 012 😀"','한글 Տերմինալ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as սպասառու:
                սպասառու.settimeout(10); սպասառու.connect(str(모의제어접속))
                with սպասառու.makefile('rwb') as հոսք_արժեք:
                    json.loads(հոսք_արժեք.readline())
                    def 호출(Անուն,արգումենտ_ԶԱՆԳՎԱԾ=None):
                        Ցանց_ուղերձ={'execute':Անուն}
                        if արգումենտ_ԶԱՆԳՎԱԾ: Ցանց_ուղերձ['arguments']=արգումենտ_ԶԱՆԳՎԱԾ
                        հոսք_արժեք.write((json.dumps(Ցանց_ուղերձ)+'\n').encode()); հոսք_արժեք.flush()
                        while True:
                            պատասխանել=json.loads(հոսք_արժեք.readline())
                            if 'error' in պատասխանել: raise AssertionError(պատասխանել)
                            if 'return' in պատասխանել: return պատասխանել['return']
                    호출('qmp_capabilities')
                    նկար=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(նկար),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    տվյալ=նկար.read_bytes().split(b'\n',3)[3]
                    def փիքսել(x_կոորդինատ,세로좌표): return tuple(տվյալ[(세로좌표*640+x_կոորդինատ)*3:(세로좌표*640+x_կոորդինատ)*3+3])
                    assert փիքսել(12,48)==(32,80,144),փիքսել(12,48)
                    assert len(set(փիքսել(x_կոորդինատ,세로좌표) for 세로좌표 in range(100,116) for x_կոորդինատ in range(24,56)))>1,'Hangul glyphs missing'
                    խեցի('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    խեցի("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(նկար),'format':'ppm'})
                    복원자료=նկար.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    խեցի('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): խեցի('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ուղարկել(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    չափ=ուղարկել(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in չափ,չափ
                    խեցի('rm visible.txt')
                    호출('quit')
            Գործընթաց.wait(timeout=5)
            վավերացում_զեկույց['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            վավերացում_զեկույց['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Գործընթաց.poll() is None:
                Գործընթաց.terminate()
                try: Գործընթաց.wait(timeout=5)
                except subprocess.TimeoutExpired: Գործընթաց.kill(); Գործընթաց.wait()
            준비살피미.close(); Գործընթաց.stdin.close(); Գործընթաց.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': Գործարկել()
