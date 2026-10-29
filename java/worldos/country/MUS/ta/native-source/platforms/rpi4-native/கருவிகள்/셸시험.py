#!/usr/bin/env python3
"""자체 커널의 கூடு, 프로세스 உள்ளீடு_வெளியீடு, Unicode GUI 터미널을 அசல்_தரவு raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம், கட்டளை


def செயல்படுத்துக():
    출력결과 = திட்டப்பணி_மூலம் / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        செயல்பாடு = subprocess.Popen(கட்டளை()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(செயல்பாடு.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            தரவு=bytearray(); முடி_ஆஃப்செட்=time.monotonic()+시간제한
            while 확인표시 not in தரவு:
                if time.monotonic()>முடி_ஆஃப்செட் or செயல்பாடு.poll() is not None: raise AssertionError('UART timeout/exit: '+தரவு.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: தரவு.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in தரவு or b'FAIL ' in தரவு: raise AssertionError(தரவு)
            return தரவு.decode('utf-8','replace').replace('\r\n','\n')
        def அனுப்பு(தரவு, 확인표시=b'jkoros-native> '):
            செயல்பாடு.stdin.write(தரவு); செயல்பாடு.stdin.flush(); return 수신하기(확인표시)
        def கூடு(உள்ளீட்டு_வரி, *예상결과):
            அளவிடக்கூடியது=அனுப்பு(உள்ளீட்டு_வரி.encode()+b'\n')
            for மதிப்பு in 예상결과: assert மதிப்பு in அளவிடக்கூடியது, (உள்ளீட்டு_வரி,மதிப்பு,அளவிடக்கூடியது)
            return அளவிடக்கூடியது
        def கோப்பின்_பெயர்(பெயர்):
            உரை=கூடு('hex '+பெயர்,'HEX BEGIN','HEX END'); தேடு_அளவிடக்கூடியது=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',உரை,re.S)
            தரவு=bytes.fromhex(''.join(தேடு_அளவிடக்கூடியது.group(2).split())); assert len(தரவு)==int(தேடு_அளவிடக்கூடியது.group(1)); return தரவு
        try:
            수신하기(b'jkoros-native> ')
            கூடு('mkdir 작업; cd 작업; pwd','/작업')
            கூடு('mkdir 하위; echo "한글 தரவு 😀" > 인사.txt')
            assert கோப்பின்_பெயர்('인사.txt')=='한글 தரவு 😀\n'.encode()
            கூடு('cp 인사.txt நகலெடு_மதிப்பு.txt; mv நகலெடு_மதிப்பு.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 தரவு 😀')
            கூடு('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 தரவு 😀','/작업/하위')
            கூடு('cd ..; rmdir 하위; echo $?','1\n')
            கூடு('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            கூடு('cp 인사.txt 인사.txt; echo $?','1\n'); assert கோப்பின்_பெயர்('인사.txt')=='한글 தரவு 😀\n'.encode()
            கூடு('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in கோப்பின்_பெயர்('인사.txt')
            கூடு("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert கோப்பின்_பெயர்('리터럴')=='$인사\n누리\n'.encode()
            கூடு('echo one > கூற்று_மதிப்பு; echo two >> கூற்று_மதிப்பு; echo three >> கூற்று_மதிப்பு')
            கூடு('cat < கூற்று_மதிப்பு | grep t | tee 추림 | wc -l','2\n'); assert கோப்பின்_பெயர்('추림')==b'two\nthree\n'
            கூடு('head -n 1 கூற்று_மதிப்பு > முன்_மதிப்பு; tail -n 1 கூற்று_மதிப்பு > பின்_மதிப்பு'); assert கோப்பின்_பெயர்('앞')==b'one\n'; assert கோப்பின்_பெயர்('뒤')==b'three\n'
            கூடு('grep absent கூற்று_மதிப்பு; echo $?','1\n')
            கூடு('echo untouched > பாதுகாப்பளி_மதிப்பு')
            கூடு('echo destroyed > பாதுகாப்பளி_மதிப்பு |','명령이 빠졌습니다'); assert கோப்பின்_பெயர்('பாதுகாப்பளி_மதிப்பு')==b'untouched\n'
            கூடு('echo "oops','따옴표가 닫히지 않았습니다')
            கூடு('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            கூடு('echo bad 2> பாதுகாப்பளி_மதிப்பு','번호를 지정한 கோப்பின்_பெயர் 서술자 உள்ளீடு_வெளியீடு சுவிட்ச்_பயன்முறை'); assert கோப்பின்_பெயர்('பாதுகாப்பளி_மதிப்பு')==b'untouched\n'
            கூடு('rm 빈파일 리터럴 கூற்று_மதிப்பு 추림 முன்_மதிப்பு பின்_மதிப்பு பாதுகாப்பளி_மதிப்பு')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            கூடு("python -c 'print(123)' | wc -c",'4\n')
            கூடு("python -c 'print(456)' > நிரல்_f5044b9b.txt"); assert கோப்பின்_பெயர்('நிரல்_f5044b9b.txt')==b'456\n'
            கூடு("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            கூடு("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < நிரல்_f5044b9b.txt", "b'456\\n'", "b''")
            கூடு("python -c 'print(\"x\"*17000)' | wc -c", 'பிழை -28')
            கூடு('echo recovered | wc -c','10\n')
            கூடு("python -c 'import jkoros; print(jkoros.read("+'"/작업/நிரல்_f5044b9b.txt"'+"))'",'456','exit 0')
            கூடு('cd /; javac Hello.java','Compiled:','exit 0')
            கூடு('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in கோப்பின்_பெயர்('/작업/자바.txt')
            கூடு('cd 작업; echo "echo script > 실행결과" > கட்டளை.sh; echo "false || echo recovered >> 실행결과" >> கட்டளை.sh; sh கட்டளை.sh')
            assert கோப்பின்_பெயர்('실행결과')==b'script\nrecovered\n'
            கூடு('rm 실행결과; echo "exit 7" > முடிவு_நிரல்.sh; sh முடிவு_நிரல்.sh; echo $?','7\n')
            கூடு('rm முடிவு_நிரல்.sh கட்டளை.sh நிரல்_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            கூடு('echo history-proof','history-proof')
            அளவிடக்கூடியது=அனுப்பு(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert அளவிடக்கூடியது.count('history-proof')>=2, அளவிடக்கூடியது
            அனுப்பு(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            அளவிடக்கூடியது=அனுப்பு(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in அளவிடக்கூடியது, அளவிடக்கூடியது
            அளவிடக்கூடியது=அனுப்பு(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in அளவிடக்கூடியது,அளவிடக்கூடியது
            அளவிடக்கூடியது=அனுப்பு('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in அளவிடக்கூடியது,அளவிடக்கூடியது
            긴글='한글'*50
            அளவிடக்கூடியது=அனுப்பு(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in அளவிடக்கூடியது
            கூடு('terminal','TERMINAL READY')
            கூடு('clear')
            கூடு('echo "한글 கட்டளை_விளக்கி ABC xyz 012 😀"','한글 கட்டளை_விளக்கி ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as பயனகம்:
                பயனகம்.settimeout(10); பயனகம்.connect(str(모의제어접속))
                with பயனகம்.makefile('rwb') as தொடரோடி_மதிப்பு:
                    json.loads(தொடரோடி_மதிப்பு.readline())
                    def 호출(பெயர்,மதிப்புரு_கோவை=None):
                        பிணையம்_செய்தி={'execute':பெயர்}
                        if மதிப்புரு_கோவை: பிணையம்_செய்தி['arguments']=மதிப்புரு_கோவை
                        தொடரோடி_மதிப்பு.write((json.dumps(பிணையம்_செய்தி)+'\n').encode()); தொடரோடி_மதிப்பு.flush()
                        while True:
                            பதிலளி=json.loads(தொடரோடி_மதிப்பு.readline())
                            if 'error' in பதிலளி: raise AssertionError(பதிலளி)
                            if 'return' in பதிலளி: return பதிலளி['return']
                    호출('qmp_capabilities')
                    படம்=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(படம்),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    தரவு=படம்.read_bytes().split(b'\n',3)[3]
                    def படக்_கூறு(x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு): return tuple(தரவு[(Y_பொத்தான்_அச்சுத்_தொகுப்பு*640+x_ஒத்ததரமுள்ளது)*3:(Y_பொத்தான்_அச்சுத்_தொகுப்பு*640+x_ஒத்ததரமுள்ளது)*3+3])
                    assert படக்_கூறு(12,48)==(32,80,144),படக்_கூறு(12,48)
                    assert len(set(படக்_கூறு(x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு) for Y_பொத்தான்_அச்சுத்_தொகுப்பு in range(100,116) for x_ஒத்ததரமுள்ளது in range(24,56)))>1,'Hangul glyphs missing'
                    கூடு('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    கூடு("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(படம்),'format':'ppm'})
                    복원자료=படம்.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    கூடு('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): கூடு('echo scroll-'+str(순번),'scroll-'+str(순번))
                    அனுப்பு(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    அளவிடக்கூடியது=அனுப்பு(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in அளவிடக்கூடியது,அளவிடக்கூடியது
                    கூடு('rm visible.txt')
                    호출('quit')
            செயல்பாடு.wait(timeout=5)
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            செல்லுபடியாக்கம்_அறிக்கை['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if செயல்பாடு.poll() is None:
                செயல்பாடு.terminate()
                try: செயல்பாடு.wait(timeout=5)
                except subprocess.TimeoutExpired: செயல்பாடு.kill(); செயல்பாடு.wait()
            준비살피미.close(); செயல்பாடு.stdin.close(); செயல்பாடு.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': செயல்படுத்துக()
