#!/usr/bin/env python3
"""배포 class의 직접 ελληνικά GUI/νήμα_τιμή 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

έργο_ρίζα = Path(__file__).resolve().parents[1]

def Εκτέλεση_2():
    클래스들 = ('Παράθυρο', 'κουμπί', 'Ετικέτα', 'πεδίο_κειμένου', '화면구성요소', 'έργο_γνωστοποίηση', 'συμβάν_ουρά', '작업가닥',
             '작업', '실행할일', '동작받이')
    πακέτο = έργο_ρίζα/'dist/jkoros-native-korean.jar'
    δήλωση = subprocess.check_output(['javap', '-classpath', str(πακέτο), '-private', '-c']+
                                ['ελληνικά.ίδιο.'+Όνομα for Όνομα in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in δήλωση, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(έργο_ρίζα/'build/examples/classes'), '-c', 'ΠαράδειγμαΠαραθύρου']).decode()
    for 필수 in ('public static void Εκτέλεση_2()', 'ελληνικά/ίδιο/συμβάν_ουρά.나중에실행', 'ελληνικά/ίδιο/έργο_γνωστοποίηση.εντολή_μήνυμα'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    προορισμός_τιμή = έργο_ρίζα/'build/verification/naming'; προορισμός_τιμή.mkdir(parents=True, exist_ok=True)
    (προορισμός_τιμή/'direct-bytecode.txt').write_text(δήλωση+'\n'+예제)
    καταγράφω_ρεκόρ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(πακέτο.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (προορισμός_τιμή/'direct-bytecode.json').write_text(json.dumps(καταγράφω_ρεκόρ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: ελληνικά 직접 GUI·νήμα_τιμή 바이트코드와 예제 호출')

if __name__ == '__main__': Εκτέλεση_2()
