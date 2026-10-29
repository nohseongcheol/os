#!/usr/bin/env python3
"""자체 커널의 anga, 프로세스 I_O, Unicode GUI 터미널을 tūturu_raraunga raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from kawe_tono import whakaatu_pūtake, tono


def whakahaere():
    출력결과 = whakaatu_pūtake / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    whakamana_pūrongo = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((whakaatu_pūtake / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Hātepe = subprocess.Popen(tono()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Hātepe.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            raraunga=bytearray(); mutu_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in raraunga:
                if time.monotonic()>mutu_OFFSET or Hātepe.poll() is not None: raise AssertionError('UART timeout/exit: '+raraunga.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: raraunga.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in raraunga or b'FAIL ' in raraunga: raise AssertionError(raraunga)
            return raraunga.decode('utf-8','replace').replace('\r\n','\n')
        def tuku(raraunga, 확인표시=b'jkoros-native> '):
            Hātepe.stdin.write(raraunga); Hātepe.stdin.flush(); return 수신하기(확인표시)
        def anga(hononga, *예상결과):
            mēhua=tuku(hononga.encode()+b'\n')
            for uara in 예상결과: assert uara in mēhua, (hononga,uara,mēhua)
            return mēhua
        def Kōnae(Ingoa):
            Ngā_kupu=anga('hex '+Ingoa,'HEX BEGIN','HEX END'); Rapu_mēhua=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Ngā_kupu,re.S)
            raraunga=bytes.fromhex(''.join(Rapu_mēhua.group(2).split())); assert len(raraunga)==int(Rapu_mēhua.group(1)); return raraunga
        try:
            수신하기(b'jkoros-native> ')
            anga('mkdir 작업; cd 작업; pwd','/작업')
            anga('mkdir 하위; echo "한글 raraunga 😀" > 인사.txt')
            assert Kōnae('인사.txt')=='한글 raraunga 😀\n'.encode()
            anga('cp 인사.txt tārua_uara.txt; mv tārua_uara.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 raraunga 😀')
            anga('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 raraunga 😀','/작업/하위')
            anga('cd ..; rmdir 하위; echo $?','1\n')
            anga('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            anga('cp 인사.txt 인사.txt; echo $?','1\n'); assert Kōnae('인사.txt')=='한글 raraunga 😀\n'.encode()
            anga('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in Kōnae('인사.txt')
            anga("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Kōnae('리터럴')=='$인사\n누리\n'.encode()
            anga('echo one > tauākī_uara; echo two >> tauākī_uara; echo three >> tauākī_uara')
            anga('cat < tauākī_uara | grep t | tee 추림 | wc -l','2\n'); assert Kōnae('추림')==b'two\nthree\n'
            anga('head -n 1 tauākī_uara > 앞; tail -n 1 tauākī_uara > Hoki_uara'); assert Kōnae('앞')==b'one\n'; assert Kōnae('뒤')==b'three\n'
            anga('grep absent tauākī_uara; echo $?','1\n')
            anga('echo untouched > pare_uara')
            anga('echo destroyed > pare_uara |','명령이 빠졌습니다'); assert Kōnae('pare_uara')==b'untouched\n'
            anga('echo "oops','따옴표가 닫히지 않았습니다')
            anga('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            anga('echo bad 2> pare_uara','번호를 지정한 Kōnae 서술자 I_O SWITCH_MODE'); assert Kōnae('pare_uara')==b'untouched\n'
            anga('rm 빈파일 리터럴 tauākī_uara 추림 앞 Hoki_uara pare_uara')
            whakamana_pūrongo['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            anga("python -c 'print(123)' | wc -c",'4\n')
            anga("python -c 'print(456)' > kaupapa_f5044b9b.txt"); assert Kōnae('kaupapa_f5044b9b.txt')==b'456\n'
            anga("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            anga("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < kaupapa_f5044b9b.txt", "b'456\\n'", "b''")
            anga("python -c 'print(\"x\"*17000)' | wc -c", 'Pōhēhē -28')
            anga('echo recovered | wc -c','10\n')
            anga("python -c 'import jkoros; print(jkoros.read("+'"/작업/kaupapa_f5044b9b.txt"'+"))'",'456','exit 0')
            anga('cd /; javac Hello.java','Compiled:','exit 0')
            anga('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in Kōnae('/작업/자바.txt')
            anga('cd 작업; echo "echo script > 실행결과" > tono.sh; echo "false || echo recovered >> 실행결과" >> tono.sh; sh tono.sh')
            assert Kōnae('실행결과')==b'script\nrecovered\n'
            anga('rm 실행결과; echo "exit 7" > Putaatu_kaupapa.sh; sh Putaatu_kaupapa.sh; echo $?','7\n')
            anga('rm Putaatu_kaupapa.sh tono.sh kaupapa_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            whakamana_pūrongo['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            anga('echo history-proof','history-proof')
            mēhua=tuku(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert mēhua.count('history-proof')>=2, mēhua
            tuku(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            mēhua=tuku(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in mēhua, mēhua
            mēhua=tuku(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in mēhua,mēhua
            mēhua=tuku('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in mēhua,mēhua
            긴글='한글'*50
            mēhua=tuku(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in mēhua
            anga('terminal','TERMINAL READY')
            anga('clear')
            anga('echo "한글 Tauranga ABC xyz 012 😀"','한글 Tauranga ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as kiritaki:
                kiritaki.settimeout(10); kiritaki.connect(str(모의제어접속))
                with kiritaki.makefile('rwb') as roma_uara:
                    json.loads(roma_uara.readline())
                    def 호출(Ingoa,tohenga_HUĀNGA=None):
                        whatunga_karere={'execute':Ingoa}
                        if tohenga_HUĀNGA: whatunga_karere['arguments']=tohenga_HUĀNGA
                        roma_uara.write((json.dumps(whatunga_karere)+'\n').encode()); roma_uara.flush()
                        while True:
                            whakautu=json.loads(roma_uara.readline())
                            if 'error' in whakautu: raise AssertionError(whakautu)
                            if 'return' in whakautu: return whakautu['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    raraunga=IMAGE.read_bytes().split(b'\n',3)[3]
                    def pika(taunga_x,세로좌표): return tuple(raraunga[(세로좌표*640+taunga_x)*3:(세로좌표*640+taunga_x)*3+3])
                    assert pika(12,48)==(32,80,144),pika(12,48)
                    assert len(set(pika(taunga_x,세로좌표) for 세로좌표 in range(100,116) for taunga_x in range(24,56)))>1,'Hangul glyphs missing'
                    anga('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    anga("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    anga('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): anga('echo scroll-'+str(순번),'scroll-'+str(순번))
                    tuku(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    mēhua=tuku(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in mēhua,mēhua
                    anga('rm visible.txt')
                    호출('quit')
            Hātepe.wait(timeout=5)
            whakamana_pūrongo['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            whakamana_pūrongo['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Hātepe.poll() is None:
                Hātepe.terminate()
                try: Hātepe.wait(timeout=5)
                except subprocess.TimeoutExpired: Hātepe.kill(); Hātepe.wait()
            준비살피미.close(); Hātepe.stdin.close(); Hātepe.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': whakahaere()
