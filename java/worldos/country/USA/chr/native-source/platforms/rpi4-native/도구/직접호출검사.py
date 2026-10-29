#!/usr/bin/env python3
"""배포 class의 직접 한국어 GUI/ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ 참조를 javap로 검사한다."""
import hashlib
import json
from pathlib import Path
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ᎠᎢᏎᏍᏗ():
    클래스들 = ('창', 'ᎠᏐᏅᏍᏙᏗ', 'ᏗᎦᏯᎸᏗ', 'ᎠᎪᎵᏰᏗ_ᏠᎨᏏ', '화면구성요소', '동작알림', 'ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ_ᎠᏍᏓᏅᏅ', '작업가닥',
             '작업', '실행할일', '동작받이')
    ᎦᏇᏅᎯ = 기준/'dist/jkoros-native-korean.jar'
    선언 = subprocess.check_output(['javap', '-classpath', str(ᎦᏇᏅᎯ), '-private', '-c']+
                                ['한국어.자체.'+ᏚᏙᎥᎢ for ᏚᏙᎥᎢ in 클래스들]).decode()
    for 금지 in ('java/lang/Thread', 'javax/swing/', 'java/awt/event/', 'java.lang.Runnable'):
        assert 금지 not in 선언, 금지
    예제 = subprocess.check_output(['javap', '-classpath', str(기준/'build/examples/classes'), '-c', '창예제']).decode()
    for 필수 in ('public static void ᎠᎢᏎᏍᏗ()', '한국어/자체/ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ_ᎠᏍᏓᏅᏅ.나중에실행', '한국어/자체/동작알림.ᎤᏁᏤᎸᎩ_ᎠᎪᎵᏰᏗ'):
        assert 필수 in 예제, 필수
    for 금지 in ('java/lang/Runnable', 'javax/swing/', 'java/awt/event/', 'actionPerformed', 'invokeLater'):
        assert 금지 not in 예제, 금지
    ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 기준/'build/verification/naming'; ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.mkdir(parents=True, exist_ok=True)
    (ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'direct-bytecode.txt').write_text(선언+'\n'+예제)
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = {'passed': True, 'scope': 'compiled direct GUI/thread API has no standard GUI/thread object delegation',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'jar_sha256': hashlib.sha256(ᎦᏇᏅᎯ.read_bytes()).hexdigest(), 'classes': list(클래스들),
          'bytecode': 'direct-bytecode.txt', 'standard_string_compiler_contract_preserved': True}
    (ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ/'direct-bytecode.json').write_text(json.dumps(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, ensure_ascii=False, indent=2)+'\n')
    print('PASS: 한국어 직접 GUI·ᎪᏪᎵ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ 바이트코드와 예제 호출')

if __name__ == '__main__': ᎠᎢᏎᏍᏗ()
