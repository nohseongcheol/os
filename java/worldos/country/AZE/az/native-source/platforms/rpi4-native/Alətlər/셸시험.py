#!/usr/bin/env python3
"""자체 커널의 örtük, 프로세스 giriş_çıxış, Unicode GUI 터미널을 faktiki_verilənlər raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from icra_etmək_əmr import Project_kök, Əmr


def İcra_Et():
    출력결과 = Project_kök / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    yoxlama_hesabat = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        Proses = subprocess.Popen(Əmr()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proses.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            verilənlər=bytearray(); bitirmək_OFFSET=time.monotonic()+시간제한
            while 확인표시 not in verilənlər:
                if time.monotonic()>bitirmək_OFFSET or Proses.poll() is not None: raise AssertionError('UART timeout/exit: '+verilənlər.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: verilənlər.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in verilənlər or b'FAIL ' in verilənlər: raise AssertionError(verilənlər)
            return verilənlər.decode('utf-8','replace').replace('\r\n','\n')
        def göndərmək(verilənlər, 확인표시=b'jkoros-native> '):
            Proses.stdin.write(verilənlər); Proses.stdin.flush(); return 수신하기(확인표시)
        def örtük(Giriş, *예상결과):
            ölçü=göndərmək(Giriş.encode()+b'\n')
            for VALUE in 예상결과: assert VALUE in ölçü, (Giriş,VALUE,ölçü)
            return ölçü
        def FAYL(Ad):
            Mətn=örtük('hex '+Ad,'HEX BEGIN','HEX END'); SEARCH_ölçü=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Mətn,re.S)
            verilənlər=bytes.fromhex(''.join(SEARCH_ölçü.group(2).split())); assert len(verilənlər)==int(SEARCH_ölçü.group(1)); return verilənlər
        try:
            수신하기(b'jkoros-native> ')
            örtük('mkdir 작업; cd 작업; pwd','/작업')
            örtük('mkdir 하위; echo "한글 verilənlər 😀" > 인사.txt')
            assert FAYL('인사.txt')=='한글 verilənlər 😀\n'.encode()
            örtük('cp 인사.txt nümunə_VALUE.txt; mv nümunə_VALUE.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 verilənlər 😀')
            örtük('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 verilənlər 😀','/작업/하위')
            örtük('cd ..; rmdir 하위; echo $?','1\n')
            örtük('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            örtük('cp 인사.txt 인사.txt; echo $?','1\n'); assert FAYL('인사.txt')=='한글 verilənlər 😀\n'.encode()
            örtük('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in FAYL('인사.txt')
            örtük("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert FAYL('리터럴')=='$인사\n누리\n'.encode()
            örtük('echo one > bəyanat_VALUE; echo two >> bəyanat_VALUE; echo three >> bəyanat_VALUE')
            örtük('cat < bəyanat_VALUE | grep t | tee 추림 | wc -l','2\n'); assert FAYL('추림')==b'two\nthree\n'
            örtük('head -n 1 bəyanat_VALUE > ön_VALUE; tail -n 1 bəyanat_VALUE > GERİ_VALUE'); assert FAYL('앞')==b'one\n'; assert FAYL('뒤')==b'three\n'
            örtük('grep absent bəyanat_VALUE; echo $?','1\n')
            örtük('echo untouched > qorumaq_VALUE')
            örtük('echo destroyed > qorumaq_VALUE |','명령이 빠졌습니다'); assert FAYL('qorumaq_VALUE')==b'untouched\n'
            örtük('echo "oops','따옴표가 닫히지 않았습니다')
            örtük('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            örtük('echo bad 2> qorumaq_VALUE','번호를 지정한 FAYL 서술자 giriş_çıxış SWITCH_MODE'); assert FAYL('qorumaq_VALUE')==b'untouched\n'
            örtük('rm 빈파일 리터럴 bəyanat_VALUE 추림 ön_VALUE GERİ_VALUE qorumaq_VALUE')
            yoxlama_hesabat['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            örtük("python -c 'print(123)' | wc -c",'4\n')
            örtük("python -c 'print(456)' > proqram_f5044b9b.txt"); assert FAYL('proqram_f5044b9b.txt')==b'456\n'
            örtük("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            örtük("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < proqram_f5044b9b.txt", "b'456\\n'", "b''")
            örtük("python -c 'print(\"x\"*17000)' | wc -c", 'XƏTA -28')
            örtük('echo recovered | wc -c','10\n')
            örtük("python -c 'import jkoros; print(jkoros.read("+'"/작업/proqram_f5044b9b.txt"'+"))'",'456','exit 0')
            örtük('cd /; javac Hello.java','Compiled:','exit 0')
            örtük('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in FAYL('/작업/자바.txt')
            örtük('cd 작업; echo "echo script > 실행결과" > Əmr.sh; echo "false || echo recovered >> 실행결과" >> Əmr.sh; sh Əmr.sh')
            assert FAYL('실행결과')==b'script\nrecovered\n'
            örtük('rm 실행결과; echo "exit 7" > Çıxış_proqram.sh; sh Çıxış_proqram.sh; echo $?','7\n')
            örtük('rm Çıxış_proqram.sh Əmr.sh proqram_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            yoxlama_hesabat['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            örtük('echo history-proof','history-proof')
            ölçü=göndərmək(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ölçü.count('history-proof')>=2, ölçü
            göndərmək(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ölçü=göndərmək(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ölçü, ölçü
            ölçü=göndərmək(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ölçü,ölçü
            ölçü=göndərmək('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ölçü,ölçü
            긴글='한글'*50
            ölçü=göndərmək(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ölçü
            örtük('terminal','TERMINAL READY')
            örtük('clear')
            örtük('echo "한글 Terminal ABC xyz 012 😀"','한글 Terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as müştəri:
                müştəri.settimeout(10); müştəri.connect(str(모의제어접속))
                with müştəri.makefile('rwb') as axın_VALUE:
                    json.loads(axın_VALUE.readline())
                    def 호출(Ad,arqument_ARRAY=None):
                        Şəbəkə_mesaj={'execute':Ad}
                        if arqument_ARRAY: Şəbəkə_mesaj['arguments']=arqument_ARRAY
                        axın_VALUE.write((json.dumps(Şəbəkə_mesaj)+'\n').encode()); axın_VALUE.flush()
                        while True:
                            cavab=json.loads(axın_VALUE.readline())
                            if 'error' in cavab: raise AssertionError(cavab)
                            if 'return' in cavab: return cavab['return']
                    호출('qmp_capabilities')
                    IMAGE=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    verilənlər=IMAGE.read_bytes().split(b'\n',3)[3]
                    def piksel(x_koordinatı,Y_koordinat): return tuple(verilənlər[(Y_koordinat*640+x_koordinatı)*3:(Y_koordinat*640+x_koordinatı)*3+3])
                    assert piksel(12,48)==(32,80,144),piksel(12,48)
                    assert len(set(piksel(x_koordinatı,Y_koordinat) for Y_koordinat in range(100,116) for x_koordinatı in range(24,56)))>1,'Hangul glyphs missing'
                    örtük('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    örtük("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(IMAGE),'format':'ppm'})
                    복원자료=IMAGE.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    örtük('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): örtük('echo scroll-'+str(순번),'scroll-'+str(순번))
                    göndərmək(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ölçü=göndərmək(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ölçü,ölçü
                    örtük('rm visible.txt')
                    호출('quit')
            Proses.wait(timeout=5)
            yoxlama_hesabat['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            yoxlama_hesabat['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if Proses.poll() is None:
                Proses.terminate()
                try: Proses.wait(timeout=5)
                except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            준비살피미.close(); Proses.stdin.close(); Proses.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': İcra_Et()
