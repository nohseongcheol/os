#!/usr/bin/env python3
"""현재 커널과 воқеӣ_иттилоот 시험·배포물이 일치할 때에만 통합 санҷидани_эътибор 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def ҳэш_файл(масир):
    계산 = hashlib.sha256()
    with масир.open('rb') as Файл:
        for иттилоот in iter(lambda: Файл.read(1048576), b''): 계산.update(иттилоот)
    return 계산.hexdigest()

def порча():
    санҷиши_эътибор_масир = 기준/'build/verification'
    ҳаста_ҳэш = ҳэш_файл(기준/'build/kernel8.img')
    기록들 = {}
    for Ном in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Ном == 'boot' else Ном+'/report.json'
        иттилоот = json.loads((санҷиши_эътибор_масир/상대경로).read_text())
        if not иттилоот.get('passed') or иттилоот.get('kernel_sha256') != ҳаста_ҳэш:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Ном] = {'passed': True, 'report': 상대경로}
    санҷиш_ном = json.loads((санҷиши_эътибор_масир/'naming/report.json').read_text())
    if not санҷиш_ном['passed'] or not санҷиш_ном['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for масир, 기대값 in санҷиш_ном['c_source_sha256'].items():
        if ҳэш_файл(기준/масир) != 기대값: raise SystemExit('명명 검사 Бозгашт_қимат 바뀐 C манбаъ: '+масир)
    자바검사 = json.loads((санҷиши_эътибор_масир/'jvm/report.json').read_text())
    직접화면 = json.loads((санҷиши_эътибор_масир/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 иҷро_кардан_фармон 시험 필요')
    санҷиш_байт_қимат = json.loads((санҷиши_эътибор_масир/'naming/direct-bytecode.json').read_text())
    if not санҷиш_байт_қимат['passed'] or санҷиш_байт_қимат['jar_sha256'] != ҳэш_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 тасдиқ_кардан 필요')
    санҷиш_возеҳӣ = json.loads((санҷиши_эътибор_масир/'resolution/report.json').read_text())
    санҷиш_андоза_кардан = json.loads((санҷиши_эътибор_масир/'resize/report.json').read_text())
    갱신검사 = json.loads((санҷиши_эътибор_масир/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ҳаста_ҳэш:
        raise SystemExit('현재 커널의 부분 навсозӣ 시험 필요')
    for масир, 기대값 in 갱신검사['source_sha256'].items():
        if ҳэш_файл(기준/масир) != 기대값: raise SystemExit('부분 навсозӣ 시험 Бозгашт_қимат 바뀐 манбаъ: '+масир)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 порча ворида_нуқта 시험 필요')
    예제검사 = json.loads((санҷиши_эътибор_масир/'examples/report.json').read_text())
    if sorted(санҷиш_андоза_кардан['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 андоза_кардан 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(санҷиш_возеҳӣ['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 воқеӣ_иттилоот 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ҳэш_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Бозгашт_қимат 라이브러리가 바뀌었습니다.')
    for Ном in ('한국어통신시험','한국어예외시험'):
        if not any(ворида_қимат['name']==Ном and ворида_қимат.get('openjdk_output_equal') for ворида_қимат in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ном)
    예외들 = sorted(масир.stem for масир in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (санҷиши_эътибор_масир/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ном in 예외들:
        if '\n'+Ном+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Ном)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ҳэш_файл(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 расм_қимат ҳэш_файл 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as баста:
        if hashlib.sha256(баста.read('kernel8.img')).hexdigest() != ҳаста_ҳэш:
            raise SystemExit('부팅 ZIP ҳаста_қимат 불일치')
        부팅설정 = баста.read('config.txt')
        for Ном, андоза_кардан in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ном+'='+str(андоза_кардан) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Танзимот 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ҳэш_файл(복사본) != ҳаста_ҳэш: raise SystemExit('SD расм_қимат ҳаста_қимат 불일치')
        ҳолат_Танзимот = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ҳолат_Танзимот)])
        if ҳолат_Танзимот.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Танзимот 불일치')
    сабт_кардан_сабт = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ҳаста_ҳэш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(санҷиш_возеҳӣ['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ном:ҳэш_файл(기준/'dist'/Ном) for Ном in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (санҷиши_эътибор_масир/'native-runtime-summary.json').write_text(json.dumps(сабт_кардан_сабт,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 сабт_кардан_сабт, 한국어 예외',len(예외들),'синф_Тавсиф, SD расм_қимат·ZIP 일치')

if __name__ == '__main__': порча()
