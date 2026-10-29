#!/usr/bin/env python3
"""자체 커널의 aluwataalapu_u, 프로세스 E_A, Unicode GUI 터미널을 실제 raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 실행 import 기준, aluwataaya


def 시작():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    anaajiaakua_ipa_achikiimaajatü = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        실행과정 = subprocess.Popen(aluwataaya()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(실행과정.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            atijaaya=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in atijaaya:
                if time.monotonic()>끝위치 or 실행과정.poll() is not None: raise AssertionError('UART timeout/exit: '+atijaaya.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: atijaaya.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in atijaaya or b'FAIL ' in atijaaya: raise AssertionError(atijaaya)
            return atijaaya.decode('utf-8','replace').replace('\r\n','\n')
        def ajütaa(atijaaya, 확인표시=b'jkoros-native> '):
            실행과정.stdin.write(atijaaya); 실행과정.stdin.flush(); return 수신하기(확인표시)
        def aluwataalapu_u(liinia, *예상결과):
            결과=ajütaa(liinia.encode()+b'\n')
            for ajutuu in 예상결과: assert ajutuu in 결과, (liinia,ajutuu,결과)
            return 결과
        def anaajaalaa(이름):
            글=aluwataalapu_u('hex '+이름,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',글,re.S)
            atijaaya=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(atijaaya)==int(찾은결과.group(1)); return atijaaya
        try:
            수신하기(b'jkoros-native> ')
            aluwataalapu_u('mkdir 작업; cd 작업; pwd','/작업')
            aluwataalapu_u('mkdir 하위; echo "한글 atijaaya 😀" > 인사.txt')
            assert anaajaalaa('인사.txt')=='한글 atijaaya 😀\n'.encode()
            aluwataalapu_u('cp 인사.txt ashataa_ajutuu.txt; mv ashataa_ajutuu.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 atijaaya 😀')
            aluwataalapu_u('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 atijaaya 😀','/작업/하위')
            aluwataalapu_u('cd ..; rmdir 하위; echo $?','1\n')
            aluwataalapu_u('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            aluwataalapu_u('cp 인사.txt 인사.txt; echo $?','1\n'); assert anaajaalaa('인사.txt')=='한글 atijaaya 😀\n'.encode()
            aluwataalapu_u('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in anaajaalaa('인사.txt')
            aluwataalapu_u("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert anaajaalaa('리터럴')=='$인사\n누리\n'.encode()
            aluwataalapu_u('echo one > aluwataayaaleechon_ajutuu; echo two >> aluwataayaaleechon_ajutuu; echo three >> aluwataayaaleechon_ajutuu')
            aluwataalapu_u('cat < aluwataayaaleechon_ajutuu | grep t | tee 추림 | wc -l','2\n'); assert anaajaalaa('추림')==b'two\nthree\n'
            aluwataalapu_u('head -n 1 aluwataayaaleechon_ajutuu > 앞; tail -n 1 aluwataayaaleechon_ajutuu > 뒤'); assert anaajaalaa('앞')==b'one\n'; assert anaajaalaa('뒤')==b'three\n'
            aluwataalapu_u('grep absent aluwataayaaleechon_ajutuu; echo $?','1\n')
            aluwataalapu_u('echo untouched > aa_inmajaa_ajutuu')
            aluwataalapu_u('echo destroyed > aa_inmajaa_ajutuu |','명령이 빠졌습니다'); assert anaajaalaa('aa_inmajaa_ajutuu')==b'untouched\n'
            aluwataalapu_u('echo "oops','따옴표가 닫히지 않았습니다')
            aluwataalapu_u('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            aluwataalapu_u('echo bad 2> aa_inmajaa_ajutuu','번호를 지정한 anaajaalaa 서술자 E_A 전환'); assert anaajaalaa('aa_inmajaa_ajutuu')==b'untouched\n'
            aluwataalapu_u('rm 빈파일 리터럴 aluwataayaaleechon_ajutuu 추림 앞 뒤 aa_inmajaa_ajutuu')
            anaajiaakua_ipa_achikiimaajatü['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            aluwataalapu_u("python -c 'print(123)' | wc -c",'4\n')
            aluwataalapu_u("python -c 'print(456)' > akumajiaa_f5044b9b.txt"); assert anaajaalaa('akumajiaa_f5044b9b.txt')==b'456\n'
            aluwataalapu_u("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            aluwataalapu_u("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < akumajiaa_f5044b9b.txt", "b'456\\n'", "b''")
            aluwataalapu_u("python -c 'print(\"x\"*17000)' | wc -c", 'ajachitia -28')
            aluwataalapu_u('echo recovered | wc -c','10\n')
            aluwataalapu_u("python -c 'import jkoros; print(jkoros.read("+'"/작업/akumajiaa_f5044b9b.txt"'+"))'",'456','exit 0')
            aluwataalapu_u('cd /; javac Hello.java','Compiled:','exit 0')
            aluwataalapu_u('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in anaajaalaa('/작업/자바.txt')
            aluwataalapu_u('cd 작업; echo "echo script > 실행결과" > aluwataaya.sh; echo "false || echo recovered >> 실행결과" >> aluwataaya.sh; sh aluwataaya.sh')
            assert anaajaalaa('실행결과')==b'script\nrecovered\n'
            aluwataalapu_u('rm 실행결과; echo "exit 7" > aju_itaa_akumajiaa.sh; sh aju_itaa_akumajiaa.sh; echo $?','7\n')
            aluwataalapu_u('rm aju_itaa_akumajiaa.sh aluwataaya.sh akumajiaa_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            anaajiaakua_ipa_achikiimaajatü['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            aluwataalapu_u('echo history-proof','history-proof')
            결과=ajütaa(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            ajütaa(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=ajütaa(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=ajütaa(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=ajütaa('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=ajütaa(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            aluwataalapu_u('terminal','TERMINAL READY')
            aluwataalapu_u('clear')
            aluwataalapu_u('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as matchanta:
                matchanta.settimeout(10); matchanta.connect(str(모의제어접속))
                with matchanta.makefile('rwb') as palantüsü_ajutuu:
                    json.loads(palantüsü_ajutuu.readline())
                    def 호출(이름,ajutuu_matüriisü=None):
                        kusu_pütchi={'execute':이름}
                        if ajutuu_matüriisü: kusu_pütchi['arguments']=ajutuu_matüriisü
                        palantüsü_ajutuu.write((json.dumps(kusu_pütchi)+'\n').encode()); palantüsü_ajutuu.flush()
                        while True:
                            응답=json.loads(palantüsü_ajutuu.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    ayaakuaa=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ayaakuaa),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    atijaaya=ayaakuaa.read_bytes().split(b'\n',3)[3]
                    def pikserü(가로좌표,세로좌표): return tuple(atijaaya[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert pikserü(12,48)==(32,80,144),pikserü(12,48)
                    assert len(set(pikserü(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    aluwataalapu_u('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    aluwataalapu_u("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ayaakuaa),'format':'ppm'})
                    복원자료=ayaakuaa.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    aluwataalapu_u('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): aluwataalapu_u('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ajütaa(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=ajütaa(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    aluwataalapu_u('rm visible.txt')
                    호출('quit')
            실행과정.wait(timeout=5)
            anaajiaakua_ipa_achikiimaajatü['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            anaajiaakua_ipa_achikiimaajatü['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if 실행과정.poll() is None:
                실행과정.terminate()
                try: 실행과정.wait(timeout=5)
                except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
            준비살피미.close(); 실행과정.stdin.close(); 실행과정.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(anaajiaakua_ipa_achikiimaajatü,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 시작()
