#!/usr/bin/env python3
"""자체 커널의 piqujijjutiliriji, 프로세스 I_O, Unicode GUI 터미널을 taannallarik_titiqqat raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from 실행 import 기준, piqujijjut


def 시작():
    출력결과 = 기준 / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    naammannirainiq_unikkaaq = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Pivallianiq = subprocess.Popen(piqujijjut()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Pivallianiq.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            titiqqat=bytearray(); 끝위치=time.monotonic()+시간제한
            while 확인표시 not in titiqqat:
                if time.monotonic()>끝위치 or Pivallianiq.poll() is not None: raise AssertionError('UART timeout/exit: '+titiqqat.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: titiqqat.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in titiqqat or b'FAIL ' in titiqqat: raise AssertionError(titiqqat)
            return titiqqat.decode('utf-8','replace').replace('\r\n','\n')
        def nassiutili(titiqqat, 확인표시=b'jkoros-native> '):
            Pivallianiq.stdin.write(titiqqat); Pivallianiq.stdin.flush(); return 수신하기(확인표시)
        def piqujijjutiliriji(titikutaak, *예상결과):
            결과=nassiutili(titikutaak.encode()+b'\n')
            for atuutilik in 예상결과: assert atuutilik in 결과, (titikutaak,atuutilik,결과)
            return 결과
        def ini(atiq):
            titiqqaq=piqujijjutiliriji('hex '+atiq,'HEX BEGIN','HEX END'); 찾은결과=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',titiqqaq,re.S)
            titiqqat=bytes.fromhex(''.join(찾은결과.group(2).split())); assert len(titiqqat)==int(찾은결과.group(1)); return titiqqat
        try:
            수신하기(b'jkoros-native> ')
            piqujijjutiliriji('mkdir 작업; cd 작업; pwd','/작업')
            piqujijjutiliriji('mkdir 하위; echo "한글 titiqqat 😀" > 인사.txt')
            assert ini('인사.txt')=='한글 titiqqat 😀\n'.encode()
            piqujijjutiliriji('cp 인사.txt ijjuarli_atuutilik.txt; mv ijjuarli_atuutilik.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 titiqqat 😀')
            piqujijjutiliriji('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 titiqqat 😀','/작업/하위')
            piqujijjutiliriji('cd ..; rmdir 하위; echo $?','1\n')
            piqujijjutiliriji('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            piqujijjutiliriji('cp 인사.txt 인사.txt; echo $?','1\n'); assert ini('인사.txt')=='한글 titiqqat 😀\n'.encode()
            piqujijjutiliriji('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ini('인사.txt')
            piqujijjutiliriji("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ini('리터럴')=='$인사\n누리\n'.encode()
            piqujijjutiliriji('echo one > uqaqtaujuq_atuutilik; echo two >> uqaqtaujuq_atuutilik; echo three >> uqaqtaujuq_atuutilik')
            piqujijjutiliriji('cat < uqaqtaujuq_atuutilik | grep t | tee 추림 | wc -l','2\n'); assert ini('추림')==b'two\nthree\n'
            piqujijjutiliriji('head -n 1 uqaqtaujuq_atuutilik > 앞; tail -n 1 uqaqtaujuq_atuutilik > Utimut_atuutilik'); assert ini('앞')==b'one\n'; assert ini('뒤')==b'three\n'
            piqujijjutiliriji('grep absent uqaqtaujuq_atuutilik; echo $?','1\n')
            piqujijjutiliriji('echo untouched > pijjairli_atuutilik')
            piqujijjutiliriji('echo destroyed > pijjairli_atuutilik |','명령이 빠졌습니다'); assert ini('pijjairli_atuutilik')==b'untouched\n'
            piqujijjutiliriji('echo "oops','따옴표가 닫히지 않았습니다')
            piqujijjutiliriji('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            piqujijjutiliriji('echo bad 2> pijjairli_atuutilik','번호를 지정한 ini 서술자 I_O kipulli_mode'); assert ini('pijjairli_atuutilik')==b'untouched\n'
            piqujijjutiliriji('rm 빈파일 리터럴 uqaqtaujuq_atuutilik 추림 앞 Utimut_atuutilik pijjairli_atuutilik')
            naammannirainiq_unikkaaq['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            piqujijjutiliriji("python -c 'print(123)' | wc -c",'4\n')
            piqujijjutiliriji("python -c 'print(456)' > pilirijjut_f5044b9b.txt"); assert ini('pilirijjut_f5044b9b.txt')==b'456\n'
            piqujijjutiliriji("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            piqujijjutiliriji("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < pilirijjut_f5044b9b.txt", "b'456\\n'", "b''")
            piqujijjutiliriji("python -c 'print(\"x\"*17000)' | wc -c", 'tammarniq -28')
            piqujijjutiliriji('echo recovered | wc -c','10\n')
            piqujijjutiliriji("python -c 'import jkoros; print(jkoros.read("+'"/작업/pilirijjut_f5044b9b.txt"'+"))'",'456','exit 0')
            piqujijjutiliriji('cd /; javac Hello.java','Compiled:','exit 0')
            piqujijjutiliriji('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ini('/작업/자바.txt')
            piqujijjutiliriji('cd 작업; echo "echo script > 실행결과" > piqujijjut.sh; echo "false || echo recovered >> 실행결과" >> piqujijjut.sh; sh piqujijjut.sh')
            assert ini('실행결과')==b'script\nrecovered\n'
            piqujijjutiliriji('rm 실행결과; echo "exit 7" > taima_pilirijjut.sh; sh taima_pilirijjut.sh; echo $?','7\n')
            piqujijjutiliriji('rm taima_pilirijjut.sh piqujijjut.sh pilirijjut_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            naammannirainiq_unikkaaq['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            piqujijjutiliriji('echo history-proof','history-proof')
            결과=nassiutili(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert 결과.count('history-proof')>=2, 결과
            nassiutili(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            결과=nassiutili(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in 결과, 결과
            결과=nassiutili(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in 결과,결과
            결과=nassiutili('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in 결과,결과
            긴글='한글'*50
            결과=nassiutili(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in 결과
            piqujijjutiliriji('terminal','TERMINAL READY')
            piqujijjutiliriji('clear')
            piqujijjutiliriji('echo "한글 터미널 ABC xyz 012 😀"','한글 터미널 ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as pijittiqtaq:
                pijittiqtaq.settimeout(10); pijittiqtaq.connect(str(모의제어접속))
                with pijittiqtaq.makefile('rwb') as ingirrania_aulataup_atuutilik:
                    json.loads(ingirrania_aulataup_atuutilik.readline())
                    def 호출(atiq,aturniqarnirainiq_array=None):
                        Kasuqatigiitsimajut_titiqqausiaq={'execute':atiq}
                        if aturniqarnirainiq_array: Kasuqatigiitsimajut_titiqqausiaq['arguments']=aturniqarnirainiq_array
                        ingirrania_aulataup_atuutilik.write((json.dumps(Kasuqatigiitsimajut_titiqqausiaq)+'\n').encode()); ingirrania_aulataup_atuutilik.flush()
                        while True:
                            응답=json.loads(ingirrania_aulataup_atuutilik.readline())
                            if 'error' in 응답: raise AssertionError(응답)
                            if 'return' in 응답: return 응답['return']
                    호출('qmp_capabilities')
                    ajjinnguaq=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(ajjinnguaq),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    titiqqat=ajjinnguaq.read_bytes().split(b'\n',3)[3]
                    def pel(가로좌표,세로좌표): return tuple(titiqqat[(세로좌표*640+가로좌표)*3:(세로좌표*640+가로좌표)*3+3])
                    assert pel(12,48)==(32,80,144),pel(12,48)
                    assert len(set(pel(가로좌표,세로좌표) for 세로좌표 in range(100,116) for 가로좌표 in range(24,56)))>1,'Hangul glyphs missing'
                    piqujijjutiliriji('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    piqujijjutiliriji("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(ajjinnguaq),'format':'ppm'})
                    복원자료=ajjinnguaq.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    piqujijjutiliriji('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): piqujijjutiliriji('echo scroll-'+str(순번),'scroll-'+str(순번))
                    nassiutili(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    결과=nassiutili(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in 결과,결과
                    piqujijjutiliriji('rm visible.txt')
                    호출('quit')
            Pivallianiq.wait(timeout=5)
            naammannirainiq_unikkaaq['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            naammannirainiq_unikkaaq['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Pivallianiq.poll() is None:
                Pivallianiq.terminate()
                try: Pivallianiq.wait(timeout=5)
                except subprocess.TimeoutExpired: Pivallianiq.kill(); Pivallianiq.wait()
            준비살피미.close(); Pivallianiq.stdin.close(); Pivallianiq.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(naammannirainiq_unikkaaq,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': 시작()
