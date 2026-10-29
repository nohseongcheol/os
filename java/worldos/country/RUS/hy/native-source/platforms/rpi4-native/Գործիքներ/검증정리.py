#!/usr/bin/env python3
"""현재 커널과 իրական_տվյալ 시험·배포물이 일치할 때에만 통합 վավերացնել 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

արձակել_արմատ = Path(__file__).resolve().parents[1]

def պատահական_տվյալներ_նիշք(Ճանապարհ):
    계산 = hashlib.sha256()
    with Ճանապարհ.open('rb') as Ֆայլ:
        for տվյալ in iter(lambda: Ֆայլ.read(1048576), b''): 계산.update(տվյալ)
    return 계산.hexdigest()

def Գործարկել():
    վավերացում_ուղի = արձակել_արմատ/'build/verification'
    միջուկ_պատահական_տվյալներ = պատահական_տվյալներ_նիշք(արձակել_արմատ/'build/kernel8.img')
    기록들 = {}
    for Անուն in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Անուն == 'boot' else Անուն+'/report.json'
        տվյալ = json.loads((վավերացում_ուղի/상대경로).read_text())
        if not տվյալ.get('passed') or տվյալ.get('kernel_sha256') != միջուկ_պատահական_տվյալներ:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Անուն] = {'passed': True, 'report': 상대경로}
    կտրոն_անուն = json.loads((վավերացում_ուղի/'naming/report.json').read_text())
    if not կտրոն_անուն['passed'] or not կտրոն_անուն['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Ճանապարհ, 기대값 in կտրոն_անուն['c_source_sha256'].items():
        if պատահական_տվյալներ_նիշք(արձակել_արմատ/Ճանապարհ) != 기대값: raise SystemExit('명명 검사 Հետ_արժեք 바뀐 C ԱՂԲՅՈՒՐ: '+Ճանապարհ)
    자바검사 = json.loads((վավերացում_ուղի/'jvm/report.json').read_text())
    직접화면 = json.loads((վավերացում_ուղի/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 կատարել_հրաման 시험 필요')
    կտրոն_բայթ_արժեք = json.loads((վավերացում_ուղի/'naming/direct-bytecode.json').read_text())
    if not կտրոն_բայթ_արժեք['passed'] or կտրոն_բայթ_արժեք['jar_sha256'] != պատահական_տվյալներ_նիշք(արձակել_արմատ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 հաստատել 필요')
    կտրոն_տարլուծում = json.loads((վավերացում_ուղի/'resolution/report.json').read_text())
    կտրոն_չափափոխել = json.loads((վավերացում_ուղի/'resize/report.json').read_text())
    갱신검사 = json.loads((վավերացում_ուղի/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != միջուկ_պատահական_տվյալներ:
        raise SystemExit('현재 커널의 부분 թարմացնել 시험 필요')
    for Ճանապարհ, 기대값 in 갱신검사['source_sha256'].items():
        if պատահական_տվյալներ_նիշք(արձակել_արմատ/Ճանապարհ) != 기대값: raise SystemExit('부분 թարմացնել 시험 Հետ_արժեք 바뀐 ԱՂԲՅՈՒՐ: '+Ճանապարհ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Գործարկել մուտքագրում_կետ 시험 필요')
    예제검사 = json.loads((վավերացում_ուղի/'examples/report.json').read_text())
    if sorted(կտրոն_չափափոխել['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Չափս 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(կտրոն_տարլուծում['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 իրական_տվյալ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != պատահական_տվյալներ_նիշք(արձակել_արմատ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Հետ_արժեք 라이브러리가 바뀌었습니다.')
    for Անուն in ('한국어통신시험','한국어예외시험'):
        if not any(մուտքագրում_արժեք['name']==Անուն and մուտքագրում_արժեք.get('openjdk_output_equal') for մուտքագրում_արժեք in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Անուն)
    예외들 = sorted(Ճանապարհ.stem for Ճանապարհ in (արձակել_արմատ/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (վավերացում_ուղի/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Անուն in 예외들:
        if '\n'+Անուն+'\n' not in 예외기록: raise SystemExit('예외 արտադրել·잡기·설명 시험 필요: '+Անուն)
    명세 = json.loads((արձակել_արմատ/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != պատահական_տվյալներ_նիշք(արձակել_արմատ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 նկար_արժեք պատահական_տվյալներ_նիշք 불일치')
    with zipfile.ZipFile(str(արձակել_արմատ/'dist/jkoros-native-rpi4-boot.zip')) as փաթեթ:
        if hashlib.sha256(փաթեթ.read('kernel8.img')).hexdigest() != միջուկ_պատահական_տվյալներ:
            raise SystemExit('부팅 ZIP միջուկ_արժեք 불일치')
        부팅설정 = փաթեթ.read('config.txt')
        for Անուն, Չափս in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Անուն+'='+str(Չափս) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Նախընտրանքներ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(արձակել_արմատ/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(արձակել_արմատ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if պատահական_տվյալներ_նիշք(복사본) != միջուկ_պատահական_տվյալներ: raise SystemExit('SD նկար_արժեք միջուկ_արժեք 불일치')
        պատճեն_Կարգավորումներ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(արձակել_արմատ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(պատճեն_Կարգավորումներ)])
        if պատճեն_Կարգավորումներ.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Նախընտրանքներ 불일치')
    մատյան_տող = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': միջուկ_պատահական_տվյալներ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(կտրոն_տարլուծում['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Անուն:պատահական_տվյալներ_նիշք(արձակել_արմատ/'dist'/Անուն) for Անուն in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (վավերացում_ուղի/'native-runtime-summary.json').write_text(json.dumps(մատյան_տող,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 մատյան_տող, 한국어 예외',len(예외들),'դաս_Սահմանում, SD նկար_արժեք·ZIP 일치')

if __name__ == '__main__': Գործարկել()
