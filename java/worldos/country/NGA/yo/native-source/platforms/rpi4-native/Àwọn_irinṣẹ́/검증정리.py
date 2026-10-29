#!/usr/bin/env python3
"""현재 커널과 gangan_détà 시험·배포물이 일치할 때에만 통합 ìfọwọ́síìwé 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def burú_fáìlì(ọ̀nà):
    계산 = hashlib.sha256()
    with ọ̀nà.open('rb') as Fáìlì:
        for détà in iter(lambda: Fáìlì.read(1048576), b''): 계산.update(détà)
    return 계산.hexdigest()

def Rọ́ọ̀nù():
    Àfọwọ́sí_ọ̀nà = 기준/'build/verification'
    kánẹ́ẹ̀lì_burú = burú_fáìlì(기준/'build/kernel8.img')
    기록들 = {}
    for Orúkọ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Orúkọ == 'boot' else Orúkọ+'/report.json'
        détà = json.loads((Àfọwọ́sí_ọ̀nà/상대경로).read_text())
        if not détà.get('passed') or détà.get('kernel_sha256') != kánẹ́ẹ̀lì_burú:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Orúkọ] = {'passed': True, 'report': 상대경로}
    ṣàyẹ̀wò_orúkọ = json.loads((Àfọwọ́sí_ọ̀nà/'naming/report.json').read_text())
    if not ṣàyẹ̀wò_orúkọ['passed'] or not ṣàyẹ̀wò_orúkọ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ọ̀nà, 기대값 in ṣàyẹ̀wò_orúkọ['c_source_sha256'].items():
        if burú_fáìlì(기준/ọ̀nà) != 기대값: raise SystemExit('명명 검사 Padà_sẹ́yìn_iye 바뀐 C orísun: '+ọ̀nà)
    자바검사 = json.loads((Àfọwọ́sí_ọ̀nà/'jvm/report.json').read_text())
    직접화면 = json.loads((Àfọwọ́sí_ọ̀nà/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ṣiṣẹ́_àṣẹ 시험 필요')
    ṣàyẹ̀wò_báìtì_iye = json.loads((Àfọwọ́sí_ọ̀nà/'naming/direct-bytecode.json').read_text())
    if not ṣàyẹ̀wò_báìtì_iye['passed'] or ṣàyẹ̀wò_báìtì_iye['jar_sha256'] != burú_fáìlì(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 ridájú 필요')
    ṣàyẹ̀wò_ìmúsí_àwòrán = json.loads((Àfọwọ́sí_ọ̀nà/'resolution/report.json').read_text())
    ṣàyẹ̀wò_ìwọn = json.loads((Àfọwọ́sí_ọ̀nà/'resize/report.json').read_text())
    갱신검사 = json.loads((Àfọwọ́sí_ọ̀nà/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kánẹ́ẹ̀lì_burú:
        raise SystemExit('현재 커널의 부분 sọdọ̀tun 시험 필요')
    for ọ̀nà, 기대값 in 갱신검사['source_sha256'].items():
        if burú_fáìlì(기준/ọ̀nà) != 기대값: raise SystemExit('부분 sọdọ̀tun 시험 Padà_sẹ́yìn_iye 바뀐 orísun: '+ọ̀nà)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Rọ́ọ̀nù ìgbéwọlé_kókó 시험 필요')
    예제검사 = json.loads((Àfọwọ́sí_ọ̀nà/'examples/report.json').read_text())
    if sorted(ṣàyẹ̀wò_ìwọn['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ìwọ̀n 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ṣàyẹ̀wò_ìmúsí_àwòrán['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 gangan_détà 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != burú_fáìlì(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Padà_sẹ́yìn_iye 라이브러리가 바뀌었습니다.')
    for Orúkọ in ('한국어통신시험','한국어예외시험'):
        if not any(ìgbéwọlé_iye['name']==Orúkọ and ìgbéwọlé_iye.get('openjdk_output_equal') for ìgbéwọlé_iye in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Orúkọ)
    예외들 = sorted(ọ̀nà.stem for ọ̀nà in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (Àfọwọ́sí_ọ̀nà/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Orúkọ in 예외들:
        if '\n'+Orúkọ+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Orúkọ)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != burú_fáìlì(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 àwòrán_iye burú_fáìlì 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as àkópọ̀:
        if hashlib.sha256(àkópọ̀.read('kernel8.img')).hexdigest() != kánẹ́ẹ̀lì_burú:
            raise SystemExit('부팅 ZIP kánẹ́ẹ̀lì_iye 불일치')
        부팅설정 = àkópọ̀.read('config.txt')
        for Orúkọ, Ìwọ̀n in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Orúkọ+'='+str(Ìwọ̀n) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Àwọn_ààtò 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if burú_fáìlì(복사본) != kánẹ́ẹ̀lì_burú: raise SystemExit('SD àwòrán_iye kánẹ́ẹ̀lì_iye 불일치')
        ṣẹ̀dà_Àwọn_ààtò = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ṣẹ̀dà_Àwọn_ààtò)])
        if ṣẹ̀dà_Àwọn_ààtò.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Àwọn_ààtò 불일치')
    àkọsílẹ̀_ìṣe_ìlà_ìbú = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kánẹ́ẹ̀lì_burú,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ṣàyẹ̀wò_ìmúsí_àwòrán['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Orúkọ:burú_fáìlì(기준/'dist'/Orúkọ) for Orúkọ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (Àfọwọ́sí_ọ̀nà/'native-runtime-summary.json').write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 àkọsílẹ̀_ìṣe_ìlà_ìbú, 한국어 예외',len(예외들),'ọ̀wọ́_Ìsọ̀tumọ̀, SD àwòrán_iye·ZIP 일치')

if __name__ == '__main__': Rọ́ọ̀nù()
