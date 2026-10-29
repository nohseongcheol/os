#!/usr/bin/env python3
"""자체 커널의 셸, 프로세스 ចូល_ចេញ, Unicode GUI 터미널을 ដែលពិត_ទិន្នន័យ raspi4b에서 시험."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស, ពាក្យ_បញ្ជា


def រត់():
    출력결과 = បញ្ចាំង_ឬស / 'build/verification/shell'; 출력결과.mkdir(parents=True, exist_ok=True)
    សុពលភាព_រាយការណ៍ = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as 작업경로:
        모의제어접속 = Path(작업경로) / 'qmp.sock'
        ដំណើរការ = subprocess.Popen(ពាក្យ_បញ្ជា()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        준비살피미=selectors.DefaultSelector(); 준비살피미.register(ដំណើរការ.stdout,selectors.EVENT_READ)
        def 수신하기(확인표시, 시간제한=45):
            ទិន្នន័យ=bytearray(); បញ្ចប់_ការបែង_ភាគ=time.monotonic()+시간제한
            while 확인표시 not in ទិន្នន័យ:
                if time.monotonic()>បញ្ចប់_ការបែង_ភាគ or ដំណើរការ.poll() is not None: raise AssertionError('UART timeout/exit: '+ទិន្នន័យ.decode('utf-8','replace'))
                for 누름값,_ in 준비살피미.select(.1):
                    조각=누름값.fileobj.read(4096)
                    if 조각: ទិន្នន័យ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ទិន្នន័យ or b'FAIL ' in ទិន្នន័យ: raise AssertionError(ទិន្នន័យ)
            return ទិន្នន័យ.decode('utf-8','replace').replace('\r\n','\n')
        def ផ្ញើ(ទិន្នន័យ, 확인표시=b'jkoros-native> '):
            ដំណើរការ.stdin.write(ទិន្នន័យ); ដំណើរការ.stdin.flush(); return 수신하기(확인표시)
        def 셸(បន្ទាត់, *예상결과):
            ការវាស់វែង=ផ្ញើ(បន្ទាត់.encode()+b'\n')
            for តំលៃ in 예상결과: assert តំលៃ in ការវាស់វែង, (បន្ទាត់,តំលៃ,ការវាស់វែង)
            return ការវាស់វែង
        def ឯកសារ(ឈ្មោះ):
            អត្ថបទ=셸('hex '+ឈ្មោះ,'HEX BEGIN','HEX END'); រុករក_ការវាស់វែង=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',អត្ថបទ,re.S)
            ទិន្នន័យ=bytes.fromhex(''.join(រុករក_ការវាស់វែង.group(2).split())); assert len(ទិន្នន័យ)==int(រុករក_ការវាស់វែង.group(1)); return ទិន្នន័យ
        try:
            수신하기(b'jkoros-native> ')
            셸('mkdir 작업; cd 작업; pwd','/작업')
            셸('mkdir 하위; echo "한글 ទិន្នន័យ 😀" > 인사.txt')
            assert ឯកសារ('인사.txt')=='한글 ទិន្នន័យ 😀\n'.encode()
            셸('cp 인사.txt ចំលង_តំលៃ.txt; mv ចំលង_តំលៃ.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 ទិន្នន័យ 😀')
            셸('cd 하위; cat ../인사.txt; cat /작업/인사.txt; pwd','한글 ទិន្នន័យ 😀','/작업/하위')
            셸('cd ..; rmdir 하위; echo $?','1\n')
            셸('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            셸('cp 인사.txt 인사.txt; echo $?','1\n'); assert ឯកសារ('인사.txt')=='한글 ទិន្នន័យ 😀\n'.encode()
            셸('export 인사=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/작업','GOOD')
            assert b'BAD\n' not in ឯកសារ('인사.txt')
            셸("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert ឯកសារ('리터럴')=='$인사\n누리\n'.encode()
            셸('echo one > ឃ្លា_សេចក្តី_តំលៃ; echo two >> ឃ្លា_សេចក្តី_តំលៃ; echo three >> ឃ្លា_សេចក្តី_តំលៃ')
            셸('cat < ឃ្លា_សេចក្តី_តំលៃ | grep t | tee 추림 | wc -l','2\n'); assert ឯកសារ('추림')==b'two\nthree\n'
            셸('head -n 1 ឃ្លា_សេចក្តី_តំលៃ > ខាងមុខ_តំលៃ; tail -n 1 ឃ្លា_សេចក្តី_តំលៃ > ការថយ_តំលៃ'); assert ឯកសារ('앞')==b'one\n'; assert ឯកសារ('뒤')==b'three\n'
            셸('grep absent ឃ្លា_សេចក្តី_តំលៃ; echo $?','1\n')
            셸('echo untouched > ការពារ_តំលៃ')
            셸('echo destroyed > ការពារ_តំលៃ |','명령이 빠졌습니다'); assert ឯកសារ('ការពារ_តំលៃ')==b'untouched\n'
            셸('echo "oops','따옴표가 닫히지 않았습니다')
            셸('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            셸('echo bad 2> ការពារ_តំលៃ','번호를 지정한 ឯកសារ 서술자 ចូល_ចេញ ប្ដូរ_ម៉ូដ'); assert ឯកសារ('ការពារ_តំលៃ')==b'untouched\n'
            셸('rm 빈파일 리터럴 ឃ្លា_សេចក្តី_តំលៃ 추림 ខាងមុខ_តំលៃ ការថយ_តំលៃ ការពារ_តំលៃ')
            សុពលភាព_រាយការណ៍['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            셸("python -c 'print(123)' | wc -c",'4\n')
            셸("python -c 'print(456)' > កម្មវិធី_f5044b9b.txt"); assert ឯកសារ('កម្មវិធី_f5044b9b.txt')==b'456\n'
            셸("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            셸("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < កម្មវិធី_f5044b9b.txt", "b'456\\n'", "b''")
            셸("python -c 'print(\"x\"*17000)' | wc -c", 'កំហុស -28')
            셸('echo recovered | wc -c','10\n')
            셸("python -c 'import jkoros; print(jkoros.read("+'"/작업/កម្មវិធី_f5044b9b.txt"'+"))'",'456','exit 0')
            셸('cd /; javac Hello.java','Compiled:','exit 0')
            셸('java Hello > /작업/자바.txt'); assert '안녕하세요'.encode() in ឯកសារ('/작업/자바.txt')
            셸('cd 작업; echo "echo script > 실행결과" > ពាក្យ_បញ្ជា.sh; echo "false || echo recovered >> 실행결과" >> ពាក្យ_បញ្ជា.sh; sh ពាក្យ_បញ្ជា.sh')
            assert ឯកសារ('실행결과')==b'script\nrecovered\n'
            셸('rm 실행결과; echo "exit 7" > ចេញ_កម្មវិធី.sh; sh ចេញ_កម្មវិធី.sh; echo $?','7\n')
            셸('rm ចេញ_កម្មវិធី.sh ពាក្យ_បញ្ជា.sh កម្មវិធី_f5044b9b.txt 자바.txt 인사.txt; cd /; rmdir 작업')
            សុពលភាព_រាយការណ៍['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            셸('echo history-proof','history-proof')
            ការវាស់វែង=ផ្ញើ(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ការវាស់វែង.count('history-proof')>=2, ការវាស់វែង
            ផ្ញើ(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ការវាស់វែង=ផ្ញើ(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ការវាស់វែង, ការវាស់វែង
            ការវាស់វែង=ផ្ញើ(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ការវាស់វែង,ការវាស់វែង
            ការវាស់វែង=ផ្ញើ('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ការវាស់វែង,ការវាស់វែង
            긴글='한글'*50
            ការវាស់វែង=ផ្ញើ(('echo '+긴글+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+긴글+'\r\njkoros-native> ').encode()); assert '\n'+긴글+'\n' in ការវាស់វែង
            셸('terminal','TERMINAL READY')
            셸('clear')
            셸('echo "한글 ស្ថានីយ ABC xyz 012 😀"','한글 ស្ថានីយ ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as អតិថិជន:
                អតិថិជន.settimeout(10); អតិថិជន.connect(str(모의제어접속))
                with អតិថិជន.makefile('rwb') as ស្ទ្រីម_តំលៃ:
                    json.loads(ស្ទ្រីម_តំលៃ.readline())
                    def 호출(ឈ្មោះ,អាគុយម៉ង់_អារេ=None):
                        ណិតវឺក_សារ={'execute':ឈ្មោះ}
                        if អាគុយម៉ង់_អារេ: ណិតវឺក_សារ['arguments']=អាគុយម៉ង់_អារេ
                        ស្ទ្រីម_តំលៃ.write((json.dumps(ណិតវឺក_សារ)+'\n').encode()); ស្ទ្រីម_តំលៃ.flush()
                        while True:
                            ឆ្លើយតប=json.loads(ស្ទ្រីម_តំលៃ.readline())
                            if 'error' in ឆ្លើយតប: raise AssertionError(ឆ្លើយតប)
                            if 'return' in ឆ្លើយតប: return ឆ្លើយតប['return']
                    호출('qmp_capabilities')
                    រូបថត=출력결과/'terminal.ppm'; 호출('screendump',{'filename':str(រូបថត),'format':'ppm'})
                    호출('screendump',{'filename':str(출력결과/'terminal.png'),'format':'png'})
                    ទិន្នន័យ=រូបថត.read_bytes().split(b'\n',3)[3]
                    def ចំនុចតូចៗ(កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ): return tuple(ទិន្នន័យ[(ប៊ូតុង_Y_កូអរដោនេ*640+កូអរដោណេ_x)*3:(ប៊ូតុង_Y_កូអរដោនេ*640+កូអរដោណេ_x)*3+3])
                    assert ចំនុចតូចៗ(12,48)==(32,80,144),ចំនុចតូចៗ(12,48)
                    assert len(set(ចំនុចតូចៗ(កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ) for ប៊ូតុង_Y_កូអរដោនេ in range(100,116) for កូអរដោណេ_x in range(24,56)))>1,'Hangul glyphs missing'
                    셸('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    셸("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    호출('screendump',{'filename':str(រូបថត),'format':'ppm'})
                    복원자료=រូបថត.read_bytes().split(b'\n',3)[3]
                    assert tuple(복원자료[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    셸('echo test > visible.txt; cat visible.txt','test')
                    for 순번 in range(27): 셸('echo scroll-'+str(순번),'scroll-'+str(순번))
                    ផ្ញើ(b'\x1b[5~\x1b[6~\n')
                    호출('screendump',{'filename':str(출력결과/'terminal-scroll.png'),'format':'png'})
                    ការវាស់វែង=ផ្ញើ(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ការវាស់វែង,ការវាស់វែង
                    셸('rm visible.txt')
                    호출('quit')
            ដំណើរការ.wait(timeout=5)
            សុពលភាព_រាយការណ៍['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            សុពលភាព_រាយការណ៍['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if ដំណើរការ.poll() is None:
                ដំណើរការ.terminate()
                try: ដំណើរការ.wait(timeout=5)
                except subprocess.TimeoutExpired: ដំណើរការ.kill(); ដំណើរការ.wait()
            준비살피미.close(); ដំណើរការ.stdin.close(); ដំណើរការ.stdout.close()
            (출력결과/'serial.log').write_bytes(대화기록)
            (출력결과/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': រត់()
