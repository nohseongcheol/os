#!/usr/bin/env python3
"""현재 커널과 ትኽክለኛ_ሓበሬታ 시험·배포물이 일치할 때에만 통합 አረጋግፅ 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def 해시(መገዲ):
    계산 = hashlib.sha256()
    with መገዲ.open('rb') as ፋይል:
        for ሓበሬታ in iter(lambda: ፋይል.read(1048576), b''): 계산.update(ሓበሬታ)
    return 계산.hexdigest()

def ኣኺድ():
    ምርግጋፅ_መገዲ = 기준/'build/verification'
    커널해시 = 해시(기준/'build/kernel8.img')
    기록들 = {}
    for ሽም in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ሽም == 'boot' else ሽም+'/report.json'
        ሓበሬታ = json.loads((ምርግጋፅ_መገዲ/상대경로).read_text())
        if not ሓበሬታ.get('passed') or ሓበሬታ.get('kernel_sha256') != 커널해시:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ሽም] = {'passed': True, 'report': 상대경로}
    ፈትሽ_ሽም = json.loads((ምርግጋፅ_መገዲ/'naming/report.json').read_text())
    if not ፈትሽ_ሽም['passed'] or not ፈትሽ_ሽም['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for መገዲ, 기대값 in ፈትሽ_ሽም['c_source_sha256'].items():
        if 해시(기준/መገዲ) != 기대값: raise SystemExit('명명 검사 ድሕሪት_ዋጋ 바뀐 C ምንጪ: '+መገዲ)
    자바검사 = json.loads((ምርግጋፅ_መገዲ/'jvm/report.json').read_text())
    직접화면 = json.loads((ምርግጋፅ_መገዲ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('ትግርኛ 직접 화면 ተግብር_ትእዛዝ 시험 필요')
    ፈትሽ_ባይት_ዋጋ = json.loads((ምርግጋፅ_መገዲ/'naming/direct-bytecode.json').read_text())
    if not ፈትሽ_ባይት_ዋጋ['passed'] or ፈትሽ_ባይት_ዋጋ['jar_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 ትግርኛ 라이브러리의 직접 호출 바이트코드 ኣረጋግጽ 필요')
    ፈትሽ_ንጹርነት = json.loads((ምርግጋፅ_መገዲ/'resolution/report.json').read_text())
    ፈትሽ_መጠን = json.loads((ምርግጋፅ_መገዲ/'resize/report.json').read_text())
    갱신검사 = json.loads((ምርግጋፅ_መገዲ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != 커널해시:
        raise SystemExit('현재 커널의 부분 ኣሐድስ 시험 필요')
    for መገዲ, 기대값 in 갱신검사['source_sha256'].items():
        if 해시(기준/መገዲ) != 기대값: raise SystemExit('부분 ኣሐድስ 시험 ድሕሪት_ዋጋ 바뀐 ምንጪ: '+መገዲ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('ትግርኛ 직접 가닥과 ኣኺድ ምእታው_ነጥቢ 시험 필요')
    예제검사 = json.loads((ምርግጋፅ_መገዲ/'examples/report.json').read_text())
    if sorted(ፈትሽ_መጠን['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 መጠን 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('ትግርኛ Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ፈትሽ_ንጹርነት['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ትኽክለኛ_ሓበሬታ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ድሕሪት_ዋጋ 라이브러리가 바뀌었습니다.')
    for ሽም in ('한국어통신시험','한국어예외시험'):
        if not any(ምእታው_ዋጋ['name']==ሽም and ምእታው_ዋጋ.get('openjdk_output_equal') for ምእታው_ዋጋ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ሽም)
    예외들 = sorted(መገዲ.stem for መገዲ in (기준/'한국어자바/ትግርኛ/자체').glob('*예외.java'))
    예외기록 = (ምርግጋፅ_መገዲ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ሽም in 예외들:
        if '\n'+ሽም+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+ሽም)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != 해시(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ምስሊ_ዋጋ 해시 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as ጥማር:
        if hashlib.sha256(ጥማር.read('kernel8.img')).hexdigest() != 커널해시:
            raise SystemExit('부팅 ZIP ፍረ_ዋጋ 불일치')
        부팅설정 = ጥማር.read('config.txt')
        for ሽም, መጠን in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ሽም+'='+str(መጠን) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ኣቀማምጣታት 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if 해시(복사본) != 커널해시: raise SystemExit('SD ምስሊ_ዋጋ ፍረ_ዋጋ 불일치')
        ቅዳሕ_ኣቀማምጣታት = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ቅዳሕ_ኣቀማምጣታት)])
        if ቅዳሕ_ኣቀማምጣታት.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ኣቀማምጣታት 불일치')
    ምዝጉብ_ሪጋ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 커널해시,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ፈትሽ_ንጹርነት['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ሽም:해시(기준/'dist'/ሽም) for ሽም in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ምርግጋፅ_መገዲ/'native-runtime-summary.json').write_text(json.dumps(ምዝጉብ_ሪጋ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ምዝጉብ_ሪጋ, ትግርኛ 예외',len(예외들),'ክፍሊ_መግለጺ, SD ምስሊ_ዋጋ·ZIP 일치')

if __name__ == '__main__': ኣኺድ()
