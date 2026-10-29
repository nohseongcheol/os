#!/usr/bin/env python3
"""현재 커널과 ھەقىقىي_مەلۇمات 시험·배포물이 일치할 때에만 통합 دەلىللەش 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]

def چاچما_ھۆججەت(يول):
    계산 = hashlib.sha256()
    with يول.open('rb') as ھۆججەت:
        for مەلۇمات in iter(lambda: ھۆججەت.read(1048576), b''): 계산.update(مەلۇمات)
    return 계산.hexdigest()

def ئىجرا_قىل_2():
    دەلىللەش_يول = كۆرسىتىش_يىلتىز/'build/verification'
    يادرو_چاچما = چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/'build/kernel8.img')
    기록들 = {}
    for ئاتى in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ئاتى == 'boot' else ئاتى+'/report.json'
        مەلۇمات = json.loads((دەلىللەش_يول/상대경로).read_text())
        if not مەلۇمات.get('passed') or مەلۇمات.get('kernel_sha256') != يادرو_چاچما:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ئاتى] = {'passed': True, 'report': 상대경로}
    تەكشۈرۈش_نامى = json.loads((دەلىللەش_يول/'naming/report.json').read_text())
    if not تەكشۈرۈش_نامى['passed'] or not تەكشۈرۈش_نامى['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for يول, 기대값 in تەكشۈرۈش_نامى['c_source_sha256'].items():
        if چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/يول) != 기대값: raise SystemExit('명명 검사 ئارقىغا_قىممىتى 바뀐 C مەنبە: '+يول)
    자바검사 = json.loads((دەلىللەش_يول/'jvm/report.json').read_text())
    직접화면 = json.loads((دەلىللەش_يول/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ئىجرا_قىلىش_بۇيرۇق 시험 필요')
    تەكشۈرۈش_بايت_قىممىتى = json.loads((دەلىللەش_يول/'naming/direct-bytecode.json').read_text())
    if not تەكشۈرۈش_بايت_قىممىتى['passed'] or تەكشۈرۈش_بايت_قىممىتى['jar_sha256'] != چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 دەلىللىمەك 필요')
    تەكشۈرۈش_ئېنىقلىق = json.loads((دەلىللەش_يول/'resolution/report.json').read_text())
    تەكشۈرۈش_ئۆزگەرتمەك = json.loads((دەلىللەش_يول/'resize/report.json').read_text())
    갱신검사 = json.loads((دەلىللەش_يول/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != يادرو_چاچما:
        raise SystemExit('현재 커널의 부분 يېڭىلىماق 시험 필요')
    for يول, 기대값 in 갱신검사['source_sha256'].items():
        if چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/يول) != 기대값: raise SystemExit('부분 يېڭىلىماق 시험 ئارقىغا_قىممىتى 바뀐 مەنبە: '+يول)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ئىجرا_قىل_2 كىرگۈزۈش_نوقتا 시험 필요')
    예제검사 = json.loads((دەلىللەش_يول/'examples/report.json').read_text())
    if sorted(تەكشۈرۈش_ئۆزگەرتمەك['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 چوڭلۇقى 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(تەكشۈرۈش_ئېنىقلىق['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ھەقىقىي_مەلۇمات 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ئارقىغا_قىممىتى 라이브러리가 바뀌었습니다.')
    for ئاتى in ('한국어통신시험','한국어예외시험'):
        if not any(كىرگۈزۈش_قىممىتى['name']==ئاتى and كىرگۈزۈش_قىممىتى.get('openjdk_output_equal') for كىرگۈزۈش_قىممىتى in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ئاتى)
    예외들 = sorted(يول.stem for يول in (كۆرسىتىش_يىلتىز/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (دەلىللەش_يول/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ئاتى in 예외들:
        if '\n'+ئاتى+'\n' not in 예외기록: raise SystemExit('예외 ھاسىل_قىلىش·잡기·설명 시험 필요: '+ئاتى)
    명세 = json.loads((كۆرسىتىش_يىلتىز/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 رەسىم_قىممىتى چاچما_ھۆججەت 불일치')
    with zipfile.ZipFile(str(كۆرسىتىش_يىلتىز/'dist/jkoros-native-rpi4-boot.zip')) as توپلام:
        if hashlib.sha256(توپلام.read('kernel8.img')).hexdigest() != يادرو_چاچما:
            raise SystemExit('부팅 ZIP يادرو_قىممىتى 불일치')
        부팅설정 = توپلام.read('config.txt')
        for ئاتى, چوڭلۇقى in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ئاتى+'='+str(چوڭلۇقى) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 تەڭشەكلەر 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(كۆرسىتىش_يىلتىز/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(كۆرسىتىش_يىلتىز/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if چاچما_ھۆججەت(복사본) != يادرو_چاچما: raise SystemExit('SD رەسىم_قىممىتى يادرو_قىممىتى 불일치')
        مىسال_تەڭشەك = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(كۆرسىتىش_يىلتىز/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(مىسال_تەڭشەك)])
        if مىسال_تەڭشەك.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 تەڭشەكلەر 불일치')
    خاتىرە_قۇر = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': يادرو_چاچما,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(تەكشۈرۈش_ئېنىقلىق['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ئاتى:چاچما_ھۆججەت(كۆرسىتىش_يىلتىز/'dist'/ئاتى) for ئاتى in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (دەلىللەش_يول/'native-runtime-summary.json').write_text(json.dumps(خاتىرە_قۇر,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 خاتىرە_قۇر, 한국어 예외',len(예외들),'تۈركۈم_ئېنىقلىما, SD رەسىم_قىممىتى·ZIP 일치')

if __name__ == '__main__': ئىجرا_قىل_2()
