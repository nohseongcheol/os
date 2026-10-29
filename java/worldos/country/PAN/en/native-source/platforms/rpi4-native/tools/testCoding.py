#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from executeCommand import projectRoot

def run():
    resultData=projectRoot/'build/verification/coding';resultData.mkdir(parents=True,exist_ok=True)
    validationReport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(projectRoot/'tools/exportSdk.py')])
        with tarfile.open(str(projectRoot/'dist/jkoros-native-aarch64-sdk.tar.gz')) as compressedBundle:compressedBundle.extractall(str(resultData))
        developmentKit=resultData/'jkoros-native-sdk'
        symbolsList=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(developmentKit/'lib/libposix-kor-user.a')]).decode()
        for name in ('createEndpoint','bindAddress','sendDatagramData','receiveDatagramData','openFile','readFileData','writeFileData'):
            assert ' T '+name+'\n' in symbolsList, name
        (resultData/'korean-function-symbols.txt').write_text(symbolsList)
        validationReport['checks'].append('real-korean-c-function-symbols')
        def executeCommand(name,path,argumentArray,expected):
            dataPosition=subprocess.run(['python3',str(projectRoot/'tools/executeFile.py'),str(path)]+argumentArray,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (resultData/(name+'.log')).write_bytes(dataPosition.stdout);assert dataPosition.returncode==0,dataPosition.stdout.decode('utf-8','replace')
            assert expected.encode() in dataPosition.stdout,dataPosition.stdout;validationReport['checks'].append(name)
        for suffixValue in ('c','cpp'):
            executableFile=resultData/('Greeting-'+suffixValue+'.elf')
            subprocess.check_call(['python3',str(developmentKit/'compile.py'),str(developmentKit/'examples'/('Greeting.'+suffixValue)),'-o',str(executableFile)])
            executeCommand('korean-'+suffixValue,executableFile,[],'posix-kor invoke')
        executableFile=resultData/'streamValue.elf'
        subprocess.check_call(['python3',str(developmentKit/'compile.py'),str(developmentKit/'examples/streamValue.c'),'-o',str(executableFile)])
        executeCommand('c-stream-queues',executableFile,[],'C posix-kor 연결형 communication PASS')
        executeCommand('korean-python',projectRoot/'examples/HangulCoding/Greeting.py',['--include',str(projectRoot/'examples/HangulCoding/English.py')],'안녕하세요 누리')
        executeCommand('guest-korean-javac',projectRoot/'examples/HangulCoding/Greeting.java',[],'안녕하세요 · totalValue=42')
        validationReport['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(resultData/'report.json').write_text(json.dumps(validationReport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
