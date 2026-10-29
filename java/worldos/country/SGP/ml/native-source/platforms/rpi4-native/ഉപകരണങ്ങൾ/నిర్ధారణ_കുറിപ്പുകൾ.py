#!/usr/bin/env python3
"""현재 커널과 വാസ്തവമായ_ഡാറ്റാ 시험·배포물이 일치할 때에만 통합 സാധൂകരിക്കുക 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]

def ഹാഷ്_ഫയല്(വഴി):
    계산 = hashlib.sha256()
    with വഴി.open('rb') as ഫയല്:
        for ഡാറ്റാ in iter(lambda: ഫയല്.read(1048576), b''): 계산.update(ഡാറ്റാ)
    return 계산.hexdigest()

def നടപ്പിലാക്കുക():
    నిర్ధారణ_പാത = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification'
    കെര്_ണല്_ഹാഷ് = ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img')
    기록들 = {}
    for പേരു് in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        ആപേക്ഷിക_പാത = 'report.json' if പേരു് == 'boot' else പേരു്+'/report.json'
        ഡാറ്റാ = json.loads((నిర్ధారణ_പാത/ആപേക്ഷിക_പാത).read_text())
        if not ഡാറ്റാ.get('passed') or ഡാറ്റാ.get('kernel_sha256') != കെര്_ണല്_ഹാഷ്:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+ആപേക്ഷിക_പാത)
        기록들[പേരു്] = {'passed': True, 'report': ആപേക്ഷിക_പാത}
    ചെക്ക്_നാ_മം = json.loads((నిర్ధారణ_പാത/'naming/report.json').read_text())
    if not ചെക്ക്_നാ_മം['passed'] or not ചെക്ക്_നാ_മം['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for വഴി, 기대값 in ചെക്ക്_നാ_മം['c_source_sha256'].items():
        if ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/വഴി) != 기대값: raise SystemExit('명명 검사 പിന്നിലേക്ക്_മൂല്യം 바뀐 C ഉറവിടം: '+വഴി)
    자바검사 = json.loads((నిర్ధారణ_പാത/'jvm/report.json').read_text())
    직접화면 = json.loads((నిర్ధారణ_പാത/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 നടപ്പാക്കുക_കമാന്_ഡ് 시험 필요')
    ചെക്ക്_బైట్_മൂല്യം = json.loads((నిర్ధారణ_പാത/'naming/direct-bytecode.json').read_text())
    if not ചെക്ക്_బైట్_മൂല്യം['passed'] or ചെക്ക്_బైట్_മൂല്യം['jar_sha256'] != ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 പരിശോധിക്കുക 필요')
    ചെക്ക്_റെസലൂഷന് = json.loads((నిర్ధారణ_പാത/'resolution/report.json').read_text())
    ചെക്ക്_വലുപ്പം_ക്രമീകരിക്കുക = json.loads((నిర్ధారణ_പാത/'resize/report.json').read_text())
    갱신검사 = json.loads((నిర్ధారణ_പാത/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != കെര്_ണല്_ഹാഷ്:
        raise SystemExit('현재 커널의 부분 പുതുക്കിയെടുക്കുക 시험 필요')
    for വഴി, 기대값 in 갱신검사['source_sha256'].items():
        if ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/വഴി) != 기대값: raise SystemExit('부분 പുതുക്കിയെടുക്കുക 시험 പിന്നിലേക്ക്_മൂല്യം 바뀐 ഉറവിടം: '+വഴി)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 നടപ്പിലാക്കുക എന്_ട്രി_പോയിന്_റ് 시험 필요')
    예제검사 = json.loads((నిర్ధారణ_പാത/'examples/report.json').read_text())
    if sorted(ചെക്ക്_വലുപ്പം_ക്രമീകരിക്കുക['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 വലിപ്പം 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ചെക്ക്_റെസലൂഷന്['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 വാസ്തവമായ_ഡാറ്റാ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 പിന്നിലേക്ക്_മൂല്യം 라이브러리가 바뀌었습니다.')
    for പേരു് in ('한국어통신시험','한국어예외시험'):
        if not any(എന്_ട്രി_മൂല്യം['name']==പേരു് and എന്_ട്രി_മൂല്യം.get('openjdk_output_equal') for എന്_ട്രി_മൂല്യം in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+പേരു്)
    ഒഴിവാക്കൽ_ലിസ്റ്റ് = sorted(വഴി.stem for വഴി in (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'한국어자바/한국어/자체').glob('*ഒഴിവാക്കൽ.java'))
    ഒഴിവാക്കൽ_ലോഗ് = (నిర్ధారణ_പാത/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for പേരു് in ഒഴിവാക്കൽ_ലിസ്റ്റ്:
        if '\n'+പേരു്+'\n' not in ഒഴിവാക്കൽ_ലോഗ്: raise SystemExit('ഒഴിവാക്കൽ സൃഷ്_ടിക്കുക·잡기·설명 시험 필요: '+പേരു്)
    명세 = json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ഇമേജ്_മൂല്യം ഹാഷ്_ഫയല് 불일치')
    with zipfile.ZipFile(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-rpi4-boot.zip')) as ബണ്ടിൽ:
        if hashlib.sha256(ബണ്ടിൽ.read('kernel8.img')).hexdigest() != കെര്_ണല്_ഹാഷ്:
            raise SystemExit('부팅 ZIP കെര്_ണല്_മൂല്യം 불일치')
        부팅설정 = ബണ്ടിൽ.read('config.txt')
        for പേരു്, വലിപ്പം in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+പേരു്+'='+str(വലിപ്പം) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 സജ്ജീകരണം 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ഹാഷ്_ഫയല്(복사본) != കെര്_ണല്_ഹാഷ്: raise SystemExit('SD ഇമേജ്_മൂല്യം കെര്_ണല്_മൂല്യം 불일치')
        ദൃഷ്ടാന്തം_ക്രമീകരണം = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ദൃഷ്ടാന്തം_ക്രമീകരണം)])
        if ദൃഷ്ടാന്തം_ക്രമീകരണം.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 സജ്ജീകരണം 불일치')
    ലോഗ്_രേഖ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': കെര്_ണല്_ഹാഷ്,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ഒഴിവാക്കൽ_ലിസ്റ്റ്, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ചെക്ക്_റെസലൂഷന്['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {പേരു്:ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'dist'/പേരു്) for പേരു് in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (నిర్ధారణ_പാത/'native-runtime-summary.json').write_text(json.dumps(ലോഗ്_രേഖ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ലോഗ്_രേഖ, 한국어 ഒഴിവാക്കൽ',len(ഒഴിവാക്കൽ_ലിസ്റ്റ്),'ക്ലാസ്_നിർവ്വചനം, SD ഇമേജ്_മൂല്യം·ZIP 일치')

if __name__ == '__main__': നടപ്പിലാക്കുക()
