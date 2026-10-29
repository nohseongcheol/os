#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from testUserNetwork import VirtualMachine, position
from testJava import editValue, guestFile

def executeCommand():
    result = {}
    source = (position.parent / 'posix-kor/JavaExample/FileDemo.java').read_text()
    for kindValue in ('elf', 'iso'):
        machine = VirtualMachine(position / ('build/kernel.' + kindValue), kindValue, networkValue=False)
        try:
            editValue(machine, 'FileDemo.java', source)
            machine.command('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for iterationValue in range(2):
                Output = machine.command('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            entryList = machine.command('ls', ['java.txt  3 bytes'])
            size = int(re.search(r'FileDemo.class\s+(\d+) bytes', entryList)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as temporaryValue:
                directoryValue = Path(temporaryValue)
                guestFile(machine, 2, size, directoryValue / 'FileDemo.class')
                Host = subprocess.check_output(['java', '-Xverify:all', '-cp', str(directoryValue), 'FileDemo'], cwd=str(directoryValue), universal_newlines=True)
                assert Host == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', Host
                assert (directoryValue / 'java.txt').read_bytes() == b'A\xffB'
            editValue(machine, 'FileDemo.java', source.replace('output.write(65);', 'output.close(); output.write(65);'))
            machine.command('javac FileDemo.java', ['Exit: 0'])
            machine.command('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            editValue(machine, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            machine.command('javac FileDemo.java', ['Exit: 0'])
            machine.command('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            machine.command('run hello recovered', ['Exit: 0'])
            result[kindValue] = machine.logRecord.decode('utf-8', 'replace')
        finally:
            machine.close()
        print('PASS:', kindValue, '게스트 Java file generate/appendContinuation/byteValue/EOF/isClosed/failureValue/OpenJDK 교차 executeCommand', flush=True)
    (position / 'build/JavaFileTest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    executeCommand()
