#!/usr/bin/env python3
"""자체 커널의 කවචය, 프로세스 ආදාන_ප්_රතිදාන, Unicode GUI 터미널을 තථ්_ය_දත්ත raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from ක්_රියාත්මක_කරන්න_විධානය import 기준, විධානය


def ක්_රියාත්මක_කරන්න_2():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    වලංගුකරණය_වාර්තාව = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        සැකසුම = subprocess.Popen(විධානය()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(සැකසුම.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            දත්ත=bytearray(); නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+시간제한
            while 확인표시 not in දත්ත:
                if time.monotonic()>නිමා_කරන්න_ඕෆ්සෙට් or සැකසුම.poll() is not None: raise AssertionError('UART timeout/exit: '+දත්ත.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: දත්ත.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in දත්ත or b'FAIL ' in දත්ත: raise AssertionError(දත්ත)
            return දත්ත.decode('utf-8','replace').replace('\r\n','\n')
        def ඊමේල්(දත්ත, 확인표시=b'jkoros-native> '):
            සැකසුම.stdin.write(දත්ත); සැකසුම.stdin.flush(); return 수신하기(확인표시)
        def කවචය(පේළිය, *예상결과):
            결과=ඊමේල්(පේළිය.encode()+b'\n')
            for අගය in 예상결과: assert අගය in 결과, (පේළිය,අගය,결과)
            return 결과
        def ගොනු(නම):
            පෙළ=කවචය('hex '+නම,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',පෙළ,re.S)
            දත්ත=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(දත්ත)==int(찾은결과.group(1)); return දත්ත
        try:
            수신하기(b'jkoros-native> ')
            කවචය('mkdir 작업; cd 작업; pwd','/작업')
            කවචය('mkdir 하위; echo "한글 දත්ත 😀" > 인사.txt')
            assert ගොනු('인사.txt')=='한글 දත්ත 😀\n'.encode()
            කවචය('cp 인사.txt ප්_රස්තාව_අගය.txt; mv ප්_රස්තාව_අගය.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 දත්ත 😀')
            කවචය('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 දත්ත 😀','/작업/하위')
            කවචය('cd ..; rmdir 하위; echo $?','1\n')
            කවචය('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            කවචය('cp 인사.txt 인사.txt; echo $?','1\n'); assert ගොනු('인사.txt')=='한글 දත්ත 😀\n'.encode()
            කවචය('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ගොනු('인사.txt')
            කවචය("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ගොනු('리터럴')=='$인사\n누리\n'.encode()
            කවචය('echo one > ප්_රකාශය_අගය; echo two >> ප්_රකාශය_අගය; echo three >> ප්_රකාශය_අගය')
            කවචය('cat < ප්_රකාශය_අගය | grep t | tee 추림 | wc -l','2\n'); assert ගොනු('추림')==b'two\nthree\n'
            කවචය('head -n 1 ප්_රකාශය_අගය > 앞; tail -n 1 ප්_රකාශය_අගය > ආපසු_අගය'); assert ගොනු('앞')==b'one\n'; assert ගොනු('뒤')==b'three\n'
            කවචය('grep absent ප්_රකාශය_අගය; echo $?','1\n')
            කවචය('echo untouched > ආරක්ෂා_කරන්න_අගය')
            කවචය('echo destroyed > ආරක්ෂා_කරන්න_අගය |','명령이 빠졌습니다'); assert ගොනු('ආරක්ෂා_කරන්න_අගය')==b'untouched\n'
            කවචය('echo "oops','따옴표가 닫히지 않았습니다')
            කවචය('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            කවචය('echo bad 2> ආරක්ෂා_කරන්න_අගය','번호를 지정한 ගොනු 서술자 ආදාන_ප්_රතිදාන මාරු_වන්න_ප්_රකාරය'); assert ගොනු('ආරක්ෂා_කරන්න_අගය')==b'untouched\n'
            කවචය('rm 빈파일 리터럴 ප්_රකාශය_අගය 추림 앞 ආපසු_අගය ආරක්ෂා_කරන්න_අගය')
            වලංගුකරණය_වාර්තාව['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            කවචය("python -c 'print(123)' | wc -c",'4\n')
            කවචය("python -c 'print(456)' > යෙදු_f5044b9b.txt"); assert ගොනු('යෙදු_f5044b9b.txt')==b'456\n'
            කවචය("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            කවචය("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < යෙදු_f5044b9b.txt", "b'456\\n'", "b''")
            කවචය("python -c 'print(\"x\"*17000)' | wc -c", 'දෝෂය -28')
            කවචය('echo recovered | wc -c','10\n')
            කවචය("python -c 'import jkoros; print(jkoros.read("+'"/작업/යෙදු_f5044b9b.txt"'+"))'",'456','exit 0')
            කවචය('cd /; javac Hello.java','Compiled:','exit 0')
            කවචය('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ගොනු('/작업/자바.txt')
            කවචය('cd 작업; echo "echo script > 실행결과" > විධානය.sh; echo "false || echo recovered >> 실행결과" >> විධානය.sh; sh විධානය.sh')
            assert ගොනු('실행결과')==b'script\nrecovered\n'
            කවචය('rm 실행결과; echo "exit 7" > පිටවීම_යෙදු.sh; sh පිටවීම_යෙදු.sh; echo $?','7\n')
            කවචය('rm පිටවීම_යෙදු.sh විධානය.sh යෙදු_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            වලංගුකරණය_වාර්තාව['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            කවචය('echo history-proof','history-proof')
            결과=ඊමේල්(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            ඊමේල්(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=ඊමේල්(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=ඊමේල්(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=ඊමේල්('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=ඊමේල්(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            කවචය('terminal','TERMINAL READY')
            කවචය('clear')
            කවචය('echo "한글 අග්_රය ABC xyz 012 😀"','한글 අග්_රය ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as සේවාලාභීයා:
                සේවාලාභීයා.settimeout(10); සේවාලාභීයා.connect(str(모의제어접속))
                with සේවාලාභීයා.makefile('rwb') as දහර_අගය:
                    json.loads(දහර_අගය.readline())
                    def 호출(නම,විස්තාරකය_ආරා_ව=None):
                        ජාලය_පණිවිඩය={'execute':නම}
                        if විස්තාරකය_ආරා_ව: ජාලය_පණිවිඩය['arguments']=විස්තාරකය_ආරා_ව
                        දහර_අගය.write((json.dumps(ජාලය_පණිවිඩය)+'\n').encode()); දහර_අගය.flush()
                        while True:
                            පිළිතුරු_දෙන්න=json.loads(දහර_අගය.readline())
                            if 'error' in පිළිතුරු_දෙන්න: raise AssertionError(පිළිතුරු_දෙන්න)
                            if 'return' in පිළිතුරු_දෙන්න: return පිළිතුරු_දෙන්න['return']
                    호출('qmp_capabilities')
                    අනුරුව=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(අනුරුව),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    දත්ත=අනුරුව.read_bytes().split(b'\n',3)[3]
                    def පික්සලය(x_ඛණ්ඩාංකය,세로좌표): return tuple(දත්ත[(세로좌표*640+x_ඛණ්ඩාංකය)*3:(세로좌표*640+x_ඛණ්ඩාංකය)*3+3])
                    assert පික්සලය(12,48)==(32,80,144),පික්සලය(12,48)
                    assert len(set(පික්සලය(x_ඛණ්ඩාංකය,세로좌표) for 세로좌표 in range(100,116) for x_ඛණ්ඩාංකය in range(24,56)))>1,'Hangul glyphs missing'
                    කවචය('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    කවචය("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(අනුරුව),'format':'ppm'})
                    복원자료=අනුරුව.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    කවචය('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): කවචය('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ඊමේල්(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=ඊමේල්(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    කවචය('rm visible.txt')
                    호출('quit')
            සැකසුම.wait(timeout=5)
            වලංගුකරණය_වාර්තාව['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            වලංගුකරණය_වාර්තාව['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if සැකසුම.poll() is None:
                සැකසුම.terminate()
                try: සැකසුම.wait(timeout=5)
                except subprocess.TimeoutExpired: සැකසුම.kill(); සැකසුම.wait()
            준비살피미.close(); සැකසුම.stdin.close(); සැකසුම.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ක්_රියාත්මක_කරන්න_2()
