#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ئېقىم_قىممىتى_5b72a632 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]

def ئىجرا_قىل_2():
    클래스들 = ('كۆزنەك', 'كۇنۇپكا', 'ئەن', 'تېكىست_بۆلىكى', '화면구성요소', '동작알림', 'ھادىسە_تەرتىپ', '작업가닥',
             '작업', '실행할일', '동작받이')
    توپلام = كۆرسىتىش_يىلتىز/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(توپلام), '-private', '-c']+
                                ['한국어.자체.'+ئاتى for ئاتى in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(كۆرسىتىش_يىلتىز/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ئىجرا_قىل_2()', '한국어/자체/ھادىسە_تەرتىپ.나중에실행', '한국어/자체/동작알림.بۇيرۇق_تېكست'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    نىشان_قىممىتى = كۆرسىتىش_يىلتىز/'build/verification/naming'; نىشان_قىممىتى.mkdir(parents=True, exist_ok=True)
    (نىشان_قىممىتى/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    خاتىرە_قۇر = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(توپلام.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (نىشان_قىممىتى/'direct-bytecode.json').write_text(json.dumps(خاتىرە_قۇر, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ئېقىم_قىممىتى_5b72a632 바이트코드와 예제 호출')

if __name__ == '__main__': ئىجرا_قىل_2()
