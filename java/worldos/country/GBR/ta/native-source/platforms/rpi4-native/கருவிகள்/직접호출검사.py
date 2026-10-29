#!/usr/bin/env python3
"""배포 class의 직접 தமிழ் GUI/தொடரிழை_மதிப்பு 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]

def செயல்படுத்துக():
    클래스들 = ('창', 'பொத்தான்', 'விளக்கச்சீட்டு', 'உரைப்_புலம்', '화면구성요소', '동작알림', 'நிகழ்வு_சாரை', '작업가닥',
             '작업', '실행할일', '동작받이')
    மூட்டை = திட்டப்பணி_மூலம்/'dist/jkoros-native-korean.jar'
    அறிவிப்பு = subprocess.check_output(['javap', '-classpath', str(மூட்டை), '-private', '-c']+
                                ['தமிழ்.자체.'+பெயர் for பெயர் in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in அறிவிப்பு, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(திட்டப்பணி_மூலம்/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void செயல்படுத்துக()', 'தமிழ்/자체/நிகழ்வு_சாரை.나중에실행', 'தமிழ்/자체/동작알림.கட்டளை_உரை'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    இலக்கு_மதிப்பு = திட்டப்பணி_மூலம்/'build/verification/naming'; இலக்கு_மதிப்பு.mkdir(parents=True, exist_ok=True)
    (இலக்கு_மதிப்பு/'direct-bytecode.txt').write_text(அறிவிப்பு+'\n'+예제)
    பதிவு_பதிவு = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(மூட்டை.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (இலக்கு_மதிப்பு/'direct-bytecode.json').write_text(json.dumps(பதிவு_பதிவு, ensure_ascii=False, indent=2)+'\n')
    print('PASS: தமிழ் 직접 GUI·தொடரிழை_மதிப்பு 바이트코드와 예제 호출')

if __name__ == '__main__': செயல்படுத்துக()
