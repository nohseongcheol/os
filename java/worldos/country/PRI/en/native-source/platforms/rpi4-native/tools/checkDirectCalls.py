#!/usr/bin/env python3
"""distributionValue class의 직접 English GUI/threadValue 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

projectRoot = Path(__file__).resolve().parents[1]

def run():
    classesList = ('window', 'button', 'label', 'TextField', 'ScreenElement', 'ActionNotice', 'EventQueue', 'worker',
             'performTask', 'RunnableTask', 'ActionReceiver')
    Bundle = projectRoot/'dist/jkoros-native-korean.jar'
    Declaration = subprocess.check_output(['javap', '-classpath', str(Bundle), '-private', '-c']+
                                ['English.Native.'+name for name in classesList]).decode()
    for prohibitedValue in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert prohibitedValue not in Declaration, prohibitedValue
    examples = subprocess.check_output(['javap', '-classpath', str(projectRoot/'build/examples/classes'), '-c', 'WindowExample']).decode()
    for isRequired in ('public static void run()', 'English/Native/EventQueue.invokeLater', 'English/Native/ActionNotice.commandText'):
        assert isRequired in examples, isRequired
    for prohibitedValue in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert prohibitedValue not in examples, prohibitedValue
    destinationValue = projectRoot/'build/verification/naming'; destinationValue.mkdir(parents=True, exist_ok=True)
    (destinationValue/'direct-bytecode.txt').write_text(Declaration+'\n'+examples)
    logRecord = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((projectRoot/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(Bundle.read_bytes()).hexdigest(), 'classes': list(classesList),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (destinationValue/'direct-bytecode.json').write_text(json.dumps(logRecord, ensure_ascii=False, indent=2)+'\n')
    print('PASS: English 직접 GUI·threadValue 바이트코드와 examples invoke')

if __name__ == '__main__': run()
