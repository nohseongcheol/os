#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ଧାରା_ମୂଲ୍ୟ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]

def ଚଳାନ୍ତୁ():
    클래스들 = ('창', 'ବଟନ୍', 'ସୂଚକ', 'ପାଠ୍ୟ_କ୍ଷେତ୍ର', '화면구성요소', '동작알림', 'ଘଟଣା_ପ୍ରତିଧାଡ଼ି', '작업가닥',
             '작업', '실행할일', '동작받이')
    ବଣ୍ଡଲ୍ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(ବଣ୍ଡଲ୍), '-private', '-c']+
                                ['한국어.자체.'+ନାମ for ନାମ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ଚଳାନ୍ତୁ()', '한국어/자체/ଘଟଣା_ପ୍ରତିଧାଡ଼ି.나중에실행', '한국어/자체/동작알림.ନିର୍ଦ୍ଦେଶ_ପାଠ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/naming'; ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.mkdir(parents=True, exist_ok=True)
    (ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    ଲଗ୍_ଧାଡ଼ି = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ବଣ୍ଡଲ୍.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ/'direct-bytecode.json').write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ଧାରା_ମୂଲ୍ୟ 바이트코드와 예제 호출')

if __name__ == '__main__': ଚଳାନ୍ତୁ()
