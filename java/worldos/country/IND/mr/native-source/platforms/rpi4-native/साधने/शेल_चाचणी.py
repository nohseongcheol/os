#!/usr/bin/env python3
"""स्वकीय 커널의 शेल, 프로세스 इनपुट_आउटपुट, Unicode GUI 터미널을 वास्तविक_डेटा raspi4b에서 चाचण्या."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ, आदेश


def सुरू_करा():
    प्रदान = प्रोजेक्ट_मूळ / 'build/verification/shell'; प्रदान.mkdir(parents=True, exist_ok=True)
    पडताळणी_अहवाल = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ / 'build/kernel8.img').read_bytes()).hexdigest()}
    सत्रलेख = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as कार्यरत_पथ:
        अनुकृती_नियंत्रण_कनेक्शन = Path(कार्यरत_पथ) / 'qmp.sock'
        प्रक्रिया = subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(अनुकृती_नियंत्रण_कनेक्शन)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        सज्जता_मॉनिटर=selectors.DefaultSelector(); सज्जता_मॉनिटर.register(प्रक्रिया.stdout,selectors.EVENT_READ)
        def संदेश_स्वीकारा(खूण, निष्पादन_प्रतीक्षामर्यादा=45):
            डेटा=bytearray(); शेवट_करा_ऑफसेट=time.monotonic()+निष्पादन_प्रतीक्षामर्यादा
            while खूण not in डेटा:
                if time.monotonic()>शेवट_करा_ऑफसेट or प्रक्रिया.poll() is not None: raise AssertionError('UART timeout/exit: '+डेटा.decode('utf-8','replace'))
                for दाबलेले_मूल्य,_ in सज्जता_मॉनिटर.select(.1):
                    तुकडा_मूल्य=दाबलेले_मूल्य.fileobj.read(4096)
                    if तुकडा_मूल्य: डेटा.extend(तुकडा_मूल्य); सत्रलेख.extend(तुकडा_मूल्य)
                if b'PANIC:' in डेटा or b'FAIL ' in डेटा: raise AssertionError(डेटा)
            return डेटा.decode('utf-8','replace').replace('\r\n','\n')
        def पाठवा(डेटा, खूण=b'jkoros-native> '):
            प्रक्रिया.stdin.write(डेटा); प्रक्रिया.stdin.flush(); return संदेश_स्वीकारा(खूण)
        def शेल(ओळ, *अपेक्षित):
            मोजमाप=पाठवा(ओळ.encode()+b'\n')
            for मूल्य in अपेक्षित: assert मूल्य in मोजमाप, (ओळ,मूल्य,मोजमाप)
            return मोजमाप
        def फाइल(नाव):
            पाठ्य=शेल('hex '+नाव,'HEX BEGIN','HEX END'); शोध_मोजमाप=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',पाठ्य,re.S)
            डेटा=bytes.fromhex(''.join(शोध_मोजमाप.group(2).split())); assert len(डेटा)==int(शोध_मोजमाप.group(1)); return डेटा
        try:
            संदेश_स्वीकारा(b'jkoros-native> ')
            शेल('mkdir पारपाडा_कार्य; cd पारपाडा_कार्य; pwd','/पारपाडा_कार्य')
            शेल('mkdir 하위; echo "한글 डेटा 😀" > अभिवादन_ae353e94.txt')
            assert फाइल('अभिवादन_ae353e94.txt')=='한글 डेटा 😀\n'.encode()
            शेल('cp अभिवादन_ae353e94.txt इन्स्टन्स_मूल्य.txt; mv इन्स्टन्स_मूल्य.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 डेटा 😀')
            शेल('cd 하위; cat ../अभिवादन_ae353e94.txt; cat /पारपाडा_कार्य/अभिवादन_ae353e94.txt; pwd','한글 डेटा 😀','/पारपाडा_कार्य/하위')
            शेल('cd ..; rmdir 하위; echo $?','1\n')
            शेल('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            शेल('cp अभिवादन_ae353e94.txt अभिवादन_ae353e94.txt; echo $?','1\n'); assert फाइल('अभिवादन_ae353e94.txt')=='한글 डेटा 😀\n'.encode()
            शेल('export अभिवादन_ae353e94=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/पारपाडा_कार्य','GOOD')
            assert b'BAD\n' not in फाइल('अभिवादन_ae353e94.txt')
            शेल("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert फाइल('리터럴')=='$인사\n누리\n'.encode()
            शेल('echo one > विधान_मूल्य; echo two >> विधान_मूल्य; echo three >> विधान_मूल्य')
            शेल('cat < विधान_मूल्य | grep t | tee 추림 | wc -l','2\n'); assert फाइल('추림')==b'two\nthree\n'
            शेल('head -n 1 विधान_मूल्य > पुढील_मूल्य; tail -n 1 विधान_मूल्य > मागे_मूल्य'); assert फाइल('앞')==b'one\n'; assert फाइल('뒤')==b'three\n'
            शेल('grep absent विधान_मूल्य; echo $?','1\n')
            शेल('echo untouched > संरक्षण_मूल्य')
            शेल('echo destroyed > संरक्षण_मूल्य |','명령이 빠졌습니다'); assert फाइल('संरक्षण_मूल्य')==b'untouched\n'
            शेल('echo "oops','따옴표가 닫히지 않았습니다')
            शेल('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            शेल('echo bad 2> संरक्षण_मूल्य','번호를 지정한 फाइल विवरणक_प्रविष्टी इनपुट_आउटपुट स्विच_मोड'); assert फाइल('संरक्षण_मूल्य')==b'untouched\n'
            शेल('rm 빈파일 리터럴 विधान_मूल्य 추림 पुढील_मूल्य मागे_मूल्य संरक्षण_मूल्य')
            पडताळणी_अहवाल['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            शेल("python -c 'print(123)' | wc -c",'4\n')
            शेल("python -c 'print(456)' > अनुप्रयोग_f5044b9b.txt"); assert फाइल('अनुप्रयोग_f5044b9b.txt')==b'456\n'
            शेल("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            शेल("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < अनुप्रयोग_f5044b9b.txt", "b'456\\n'", "b''")
            शेल("python -c 'print(\"x\"*17000)' | wc -c", 'त्रुटी -28')
            शेल('echo recovered | wc -c','10\n')
            शेल("python -c 'import jkoros; print(jkoros.read("+'"/पारपाडा_कार्य/अनुप्रयोग_f5044b9b.txt"'+"))'",'456','exit 0')
            शेल('cd /; javac Hello.java','Compiled:','exit 0')
            शेल('java Hello > /पारपाडा_कार्य/जावा.txt'); assert '안녕하세요'.encode() in फाइल('/पारपाडा_कार्य/जावा.txt')
            शेल('cd पारपाडा_कार्य; echo "echo script > निष्पादन_मोजमाप" > आदेश.sh; echo "false || echo recovered >> निष्पादन_मोजमाप" >> आदेश.sh; sh आदेश.sh')
            assert फाइल('निष्पादन_मोजमाप')==b'script\nrecovered\n'
            शेल('rm निष्पादन_मोजमाप; echo "exit 7" > निर्गमन_करा_अनुप्रयोग.sh; sh निर्गमन_करा_अनुप्रयोग.sh; echo $?','7\n')
            शेल('rm निर्गमन_करा_अनुप्रयोग.sh आदेश.sh अनुप्रयोग_f5044b9b.txt जावा.txt अभिवादन_ae353e94.txt; cd /; rmdir पारपाडा_कार्य')
            पडताळणी_अहवाल['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            शेल('echo history-proof','history-proof')
            मोजमाप=पाठवा(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert मोजमाप.count('history-proof')>=2, मोजमाप
            पाठवा(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            मोजमाप=पाठवा(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in मोजमाप, मोजमाप
            मोजमाप=पाठवा(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in मोजमाप,मोजमाप
            मोजमाप=पाठवा('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in मोजमाप,मोजमाप
            दीर्घ_मजकूर='한글'*50
            मोजमाप=पाठवा(('echo '+दीर्घ_मजकूर+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+दीर्घ_मजकूर+'\r\njkoros-native> ').encode()); assert '\n'+दीर्घ_मजकूर+'\n' in मोजमाप
            शेल('terminal','TERMINAL READY')
            शेल('clear')
            शेल('echo "한글 टर्मिनल ABC xyz 012 😀"','한글 टर्मिनल ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as क्लायंट:
                क्लायंट.settimeout(10); क्लायंट.connect(str(अनुकृती_नियंत्रण_कनेक्शन))
                with क्लायंट.makefile('rwb') as प्रवाह_मूल्य:
                    json.loads(प्रवाह_मूल्य.readline())
                    def आवाहन(नाव,वितर्क_ऍरे=None):
                        संचारजाळे_संदेश={'execute':नाव}
                        if वितर्क_ऍरे: संचारजाळे_संदेश['arguments']=वितर्क_ऍरे
                        प्रवाह_मूल्य.write((json.dumps(संचारजाळे_संदेश)+'\n').encode()); प्रवाह_मूल्य.flush()
                        while True:
                            प्रत्युत्तर_द्या=json.loads(प्रवाह_मूल्य.readline())
                            if 'error' in प्रत्युत्तर_द्या: raise AssertionError(प्रत्युत्तर_द्या)
                            if 'return' in प्रत्युत्तर_द्या: return प्रत्युत्तर_द्या['return']
                    आवाहन('qmp_capabilities')
                    चित्र=प्रदान/'terminal.ppm'; आवाहन('screendump',{'filename':str(चित्र),'format':'ppm'})
                    आवाहन('screendump',{'filename':str(प्रदान/'terminal.png'),'format':'png'})
                    डेटा=चित्र.read_bytes().split(b'\n',3)[3]
                    def पिक्सेल(आडवे_समन्वयीत,उभे_समन्वयीत): return tuple(डेटा[(उभे_समन्वयीत*640+आडवे_समन्वयीत)*3:(उभे_समन्वयीत*640+आडवे_समन्वयीत)*3+3])
                    assert पिक्सेल(12,48)==(32,80,144),पिक्सेल(12,48)
                    assert len(set(पिक्सेल(आडवे_समन्वयीत,उभे_समन्वयीत) for उभे_समन्वयीत in range(100,116) for आडवे_समन्वयीत in range(24,56)))>1,'Hangul glyphs missing'
                    शेल('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    शेल("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    आवाहन('screendump',{'filename':str(चित्र),'format':'ppm'})
                    पुनर्स्थापित_डेटा=चित्र.read_bytes().split(b'\n',3)[3]
                    assert tuple(पुनर्स्थापित_डेटा[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    शेल('echo test > visible.txt; cat visible.txt','test')
                    for क्रमांक_अनुक्रमणिका in range(27): शेल('echo scroll-'+str(क्रमांक_अनुक्रमणिका),'scroll-'+str(क्रमांक_अनुक्रमणिका))
                    पाठवा(b'\x1b[5~\x1b[6~\n')
                    आवाहन('screendump',{'filename':str(प्रदान/'terminal-scroll.png'),'format':'png'})
                    मोजमाप=पाठवा(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in मोजमाप,मोजमाप
                    शेल('rm visible.txt')
                    आवाहन('quit')
            प्रक्रिया.wait(timeout=5)
            पडताळणी_अहवाल['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            पडताळणी_अहवाल['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if प्रक्रिया.poll() is None:
                प्रक्रिया.terminate()
                try: प्रक्रिया.wait(timeout=5)
                except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            सज्जता_मॉनिटर.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            (प्रदान/'serial.log').write_bytes(सत्रलेख)
            (प्रदान/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': सुरू_करा()
