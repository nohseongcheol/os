#!/usr/bin/env python3
"""Native 커널의 shell, 프로세스 inputOutput, Unicode GUI 터미널을 actualData raspi4b에서 tests."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from executeCommand import projectRoot, command


def run():
    output = projectRoot / 'build/verification/shell'; output.mkdir(parents=True, exist_ok=True)
    validationReport = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((projectRoot / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcript = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as workingPath:
        mockControlConnection = Path(workingPath) / 'qmp.sock'
        process = subprocess.Popen(command()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(mockControlConnection)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        readinessMonitor=selectors.DefaultSelector(); readinessMonitor.register(process.stdout,selectors.EVENT_READ)
        def receiveMessage(marker, executionTimeout=45):
            data=bytearray(); endOffset=time.monotonic()+executionTimeout
            while marker not in data:
                if time.monotonic()>endOffset or process.poll() is not None: raise AssertionError('UART timeout/exit: '+data.decode('utf-8','replace'))
                for pressedValue,_ in readinessMonitor.select(.1):
                    fragmentValue=pressedValue.fileobj.read(4096)
                    if fragmentValue: data.extend(fragmentValue); transcript.extend(fragmentValue)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8','replace').replace('\r\n','\n')
        def send(data, marker=b'jkoros-native> '):
            process.stdin.write(data); process.stdin.flush(); return receiveMessage(marker)
        def shell(line, *expected):
            result=send(line.encode()+b'\n')
            for value in expected: assert value in result, (line,value,result)
            return result
        def file(name):
            text=shell('hex '+name,'HEX BEGIN','HEX END'); searchResult=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',text,re.S)
            data=bytes.fromhex(''.join(searchResult.group(2).split())); assert len(data)==int(searchResult.group(1)); return data
        try:
            receiveMessage(b'jkoros-native> ')
            shell('mkdir performTask; cd performTask; pwd','/performTask')
            shell('mkdir 하위; echo "hangulText data 😀" > Greeting.txt')
            assert file('Greeting.txt')=='hangulText data 😀\n'.encode()
            shell('cp Greeting.txt copyValue.txt; mv copyValue.txt 하위/옮김.txt; cat 하위/옮김.txt','hangulText data 😀')
            shell('cd 하위; cat ../Greeting.txt; cat /performTask/Greeting.txt; pwd','hangulText data 😀','/performTask/하위')
            shell('cd ..; rmdir 하위; echo $?','1\n')
            shell('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            shell('cp Greeting.txt Greeting.txt; echo $?','1\n'); assert file('Greeting.txt')=='hangulText data 😀\n'.encode()
            shell('export Greeting=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/performTask','GOOD')
            assert b'BAD\n' not in file('Greeting.txt')
            shell("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert file('리터럴')=='$인사\n누리\n'.encode()
            shell('echo one > statementValue; echo two >> statementValue; echo three >> statementValue')
            shell('cat < statementValue | grep t | tee 추림 | wc -l','2\n'); assert file('추림')==b'two\nthree\n'
            shell('head -n 1 statementValue > frontValue; tail -n 1 statementValue > backValue'); assert file('frontValue')==b'one\n'; assert file('backValue')==b'three\n'
            shell('grep absent statementValue; echo $?','1\n')
            shell('echo untouched > protectValue')
            shell('echo destroyed > protectValue |','명령이 빠졌습니다'); assert file('protectValue')==b'untouched\n'
            shell('echo "oops','따옴표가 닫히지 않았습니다')
            shell('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            shell('echo bad 2> protectValue','번호를 지정한 file descriptorEntry inputOutput switchMode'); assert file('protectValue')==b'untouched\n'
            shell('rm 빈파일 리터럴 statementValue 추림 frontValue backValue protectValue')
            validationReport['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            shell("python -c 'print(123)' | wc -c",'4\n')
            shell("python -c 'print(456)' > Program.txt"); assert file('Program.txt')==b'456\n'
            shell("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            shell("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Program.txt", "b'456\\n'", "b''")
            shell("python -c 'print(\"x\"*17000)' | wc -c", 'error -28')
            shell('echo recovered | wc -c','10\n')
            shell("python -c 'import jkoros; print(jkoros.read("+'"/performTask/Program.txt"'+"))'",'456','exit 0')
            shell('cd /; javac Hello.java','Compiled:','exit 0')
            shell('java Hello > /performTask/Java.txt'); assert '안녕하세요'.encode() in file('/performTask/Java.txt')
            shell('cd performTask; echo "echo script > executionResult" > command.sh; echo "false || echo recovered >> executionResult" >> command.sh; sh command.sh')
            assert file('executionResult')==b'script\nrecovered\n'
            shell('rm executionResult; echo "exit 7" > exitProgram.sh; sh exitProgram.sh; echo $?','7\n')
            shell('rm exitProgram.sh command.sh Program.txt Java.txt Greeting.txt; cd /; rmdir performTask')
            validationReport['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            shell('echo history-proof','history-proof')
            result=send(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert result.count('history-proof')>=2, result
            send(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            result=send(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in result, result
            result=send(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in result,result
            result=send('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in result,result
            longText='hangulText'*50
            result=send(('echo '+longText+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+longText+'\r\njkoros-native> ').encode()); assert '\n'+longText+'\n' in result
            shell('terminal','TERMINAL READY')
            shell('clear')
            shell('echo "hangulText terminal ABC xyz 012 😀"','hangulText terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as client:
                client.settimeout(10); client.connect(str(mockControlConnection))
                with client.makefile('rwb') as streamValue:
                    json.loads(streamValue.readline())
                    def invoke(name,argumentArray=None):
                        networkMessage={'execute':name}
                        if argumentArray: networkMessage['arguments']=argumentArray
                        streamValue.write((json.dumps(networkMessage)+'\n').encode()); streamValue.flush()
                        while True:
                            reply=json.loads(streamValue.readline())
                            if 'error' in reply: raise AssertionError(reply)
                            if 'return' in reply: return reply['return']
                    invoke('qmp_capabilities')
                    image=output/'terminal.ppm'; invoke('screendump',{'filename':str(image),'format':'ppm'})
                    invoke('screendump',{'filename':str(output/'terminal.png'),'format':'png'})
                    data=image.read_bytes().split(b'\n',3)[3]
                    def pixel(xCoordinate,yCoordinate): return tuple(data[(yCoordinate*640+xCoordinate)*3:(yCoordinate*640+xCoordinate)*3+3])
                    assert pixel(12,48)==(32,80,144),pixel(12,48)
                    assert len(set(pixel(xCoordinate,yCoordinate) for yCoordinate in range(100,116) for xCoordinate in range(24,56)))>1,'Hangul glyphs missing'
                    shell('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    shell("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    invoke('screendump',{'filename':str(image),'format':'ppm'})
                    restoredData=image.read_bytes().split(b'\n',3)[3]
                    assert tuple(restoredData[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    shell('echo test > visible.txt; cat visible.txt','test')
                    for ordinalIndex in range(27): shell('echo scroll-'+str(ordinalIndex),'scroll-'+str(ordinalIndex))
                    send(b'\x1b[5~\x1b[6~\n')
                    invoke('screendump',{'filename':str(output/'terminal-scroll.png'),'format':'png'})
                    result=send(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in result,result
                    shell('rm visible.txt')
                    invoke('quit')
            process.wait(timeout=5)
            validationReport['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validationReport['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=5)
                except subprocess.TimeoutExpired: process.kill(); process.wait()
            readinessMonitor.close(); process.stdin.close(); process.stdout.close()
            (output/'serial.log').write_bytes(transcript)
            (output/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': run()
