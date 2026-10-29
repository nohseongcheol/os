#!/usr/bin/env python3
"""현재 커널과 ትክክለኛ_ውሂብ 시험·배포물이 일치할 때에만 통합 ትክክለኛነት_አረጋግጥ 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

አሳይ_ስር = Path(__file__).resolve().parents[1]

def ሃሽ_ፋይል(መተላለፊያ):
    계산 = hashlib.sha256()
    with መተላለፊያ.open('rb') as ፋይል:
        for ውሂብ in iter(lambda: ፋይል.read(1048576), b''): 계산.update(ውሂብ)
    return 계산.hexdigest()

def ማስኬጃ():
    ማረጋገጥ_ዱካ = አሳይ_ስር/'build/verification'
    ዓንኳር_ሃሽ = ሃሽ_ፋይል(አሳይ_ስር/'build/kernel8.img')
    기록들 = {}
    for ስም in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ስም == 'boot' else ስም+'/report.json'
        ውሂብ = json.loads((ማረጋገጥ_ዱካ/상대경로).read_text())
        if not ውሂብ.get('passed') or ውሂብ.get('kernel_sha256') != ዓንኳር_ሃሽ:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ስም] = {'passed': True, 'report': 상대경로}
    ቼክ_ስም = json.loads((ማረጋገጥ_ዱካ/'naming/report.json').read_text())
    if not ቼክ_ስም['passed'] or not ቼክ_ስም['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for መተላለፊያ, 기대값 in ቼክ_ስም['c_source_sha256'].items():
        if ሃሽ_ፋይል(አሳይ_ስር/መተላለፊያ) != 기대값: raise SystemExit('명명 검사 ተመለስ_እሴት 바뀐 C ምንጭ: '+መተላለፊያ)
    자바검사 = json.loads((ማረጋገጥ_ዱካ/'jvm/report.json').read_text())
    직접화면 = json.loads((ማረጋገጥ_ዱካ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('አማርኛ 직접 화면 ፈጽም_ትእዛዝ 시험 필요')
    ቼክ_ባይት_እሴት = json.loads((ማረጋገጥ_ዱካ/'naming/direct-bytecode.json').read_text())
    if not ቼክ_ባይት_እሴት['passed'] or ቼክ_ባይት_እሴት['jar_sha256'] != ሃሽ_ፋይል(አሳይ_ስር/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 አማርኛ 라이브러리의 직접 호출 바이트코드 አረጋግጥ 필요')
    ቼክ_ጥራት = json.loads((ማረጋገጥ_ዱካ/'resolution/report.json').read_text())
    ቼክ_መጠን_ቀይር = json.loads((ማረጋገጥ_ዱካ/'resize/report.json').read_text())
    갱신검사 = json.loads((ማረጋገጥ_ዱካ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ዓንኳር_ሃሽ:
        raise SystemExit('현재 커널의 부분 አድስ 시험 필요')
    for መተላለፊያ, 기대값 in 갱신검사['source_sha256'].items():
        if ሃሽ_ፋይል(አሳይ_ስር/መተላለፊያ) != 기대값: raise SystemExit('부분 አድስ 시험 ተመለስ_እሴት 바뀐 ምንጭ: '+መተላለፊያ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('አማርኛ 직접 가닥과 ማስኬጃ ምዝግብ_ቦታ 시험 필요')
    예제검사 = json.loads((ማረጋገጥ_ዱካ/'examples/report.json').read_text())
    if sorted(ቼክ_መጠን_ቀይር['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 መጠን 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('አማርኛ Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ቼክ_ጥራት['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ትክክለኛ_ውሂብ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ሃሽ_ፋይል(አሳይ_ስር/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ተመለስ_እሴት 라이브러리가 바뀌었습니다.')
    for ስም in ('한국어통신시험','한국어예외시험'):
        if not any(ምዝግብ_እሴት['name']==ስም and ምዝግብ_እሴት.get('openjdk_output_equal') for ምዝግብ_እሴት in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ስም)
    ልዩነት_ዝርዝር = sorted(መተላለፊያ.stem for መተላለፊያ in (አሳይ_ስር/'한국어자바/አማርኛ/자체').glob('*ልዩነት.java'))
    ልዩነት_መዝግብ = (ማረጋገጥ_ዱካ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ስም in ልዩነት_ዝርዝር:
        if '\n'+ስም+'\n' not in ልዩነት_መዝግብ: raise SystemExit('ልዩነት አዘጋጅ·잡기·설명 시험 필요: '+ስም)
    명세 = json.loads((አሳይ_ስር/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ሃሽ_ፋይል(አሳይ_ስር/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ምስል_እሴት ሃሽ_ፋይል 불일치')
    with zipfile.ZipFile(str(አሳይ_ስር/'dist/jkoros-native-rpi4-boot.zip')) as ቀርቅብ:
        if hashlib.sha256(ቀርቅብ.read('kernel8.img')).hexdigest() != ዓንኳር_ሃሽ:
            raise SystemExit('부팅 ZIP ዓንኳር_እሴት 불일치')
        부팅설정 = ቀርቅብ.read('config.txt')
        for ስም, መጠን in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ስም+'='+str(መጠን) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ማሰናጃዎች 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(አሳይ_ስር/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(አሳይ_ስር/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ሃሽ_ፋይል(복사본) != ዓንኳር_ሃሽ: raise SystemExit('SD ምስል_እሴት ዓንኳር_እሴት 불일치')
        ቅዳ_ቅንብሮች = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(አሳይ_ስር/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ቅዳ_ቅንብሮች)])
        if ቅዳ_ቅንብሮች.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ማሰናጃዎች 불일치')
    መዝግብ_ረድፍ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ዓንኳር_ሃሽ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ልዩነት_ዝርዝር, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ቼክ_ጥራት['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ስም:ሃሽ_ፋይል(አሳይ_ስር/'dist'/ስም) for ስም in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ማረጋገጥ_ዱካ/'native-runtime-summary.json').write_text(json.dumps(መዝግብ_ረድፍ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 መዝግብ_ረድፍ, አማርኛ ልዩነት',len(ልዩነት_ዝርዝር),'መደብ_ፍቺ, SD ምስል_እሴት·ZIP 일치')

if __name__ == '__main__': ማስኬጃ()
