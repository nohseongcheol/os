#!/usr/bin/env python3
"""נוכחי_פריט 커널과 בפועל_נתונים 시험·배포물이 일치할 때에만 통합 לאמת 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

לשקף_בסיס = Path(__file__).resolve().parents[1]

def קוד_Hash_קובץ(נתיב):
    계산 = hashlib.sha256()
    with נתיב.open('rb') as קובץ:
        for נתונים in iter(lambda: קובץ.read(1048576), b''): 계산.update(נתונים)
    return 계산.hexdigest()

def הפעלה():
    אימות_נתיב = לשקף_בסיס/'build/verification'
    ליבה_קוד_Hash = קוד_Hash_קובץ(לשקף_בסיס/'build/kernel8.img')
    기록들 = {}
    for שם in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        נתיב_יחסי = 'report.json' if שם == 'boot' else שם+'/report.json'
        נתונים = json.loads((אימות_נתיב/נתיב_יחסי).read_text())
        if not נתונים.get('passed') or נתונים.get('kernel_sha256') != ליבה_קוד_Hash:
            raise SystemExit('נוכחי_פריט 커널에 대한 성공 기록이 필요합니다: '+נתיב_יחסי)
        기록들[שם] = {'passed': True, 'report': נתיב_יחסי}
    שיק_שם = json.loads((אימות_נתיב/'naming/report.json').read_text())
    if not שיק_שם['passed'] or not שיק_שם['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for נתיב, 기대값 in שיק_שם['c_source_sha256'].items():
        if קוד_Hash_קובץ(לשקף_בסיס/נתיב) != 기대값: raise SystemExit('명명 검사 הקודם_ערך 바뀐 C קודמקור: '+נתיב)
    자바검사 = json.loads((אימות_נתיב/'jvm/report.json').read_text())
    직접화면 = json.loads((אימות_נתיב/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('עברית 직접 화면 לבצע_פקודה 시험 필요')
    שיק_בית_ערך = json.loads((אימות_נתיב/'naming/direct-bytecode.json').read_text())
    if not שיק_בית_ערך['passed'] or שיק_בית_ערך['jar_sha256'] != קוד_Hash_קובץ(לשקף_בסיס/'dist/jkoros-native-korean.jar'):
        raise SystemExit('נוכחי_פריט עברית 라이브러리의 직접 호출 바이트코드 ודא_אמת 필요')
    שיק_רזולוציה = json.loads((אימות_נתיב/'resolution/report.json').read_text())
    שיק_גודל = json.loads((אימות_נתיב/'resize/report.json').read_text())
    갱신검사 = json.loads((אימות_נתיב/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ליבה_קוד_Hash:
        raise SystemExit('נוכחי_פריט 커널의 부분 רענן 시험 필요')
    for נתיב, 기대값 in 갱신검사['source_sha256'].items():
        if קוד_Hash_קובץ(לשקף_בסיס/נתיב) != 기대값: raise SystemExit('부분 רענן 시험 הקודם_ערך 바뀐 קודמקור: '+נתיב)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('עברית 직접 가닥과 הפעלה נקודת_כניסה 시험 필요')
    예제검사 = json.loads((אימות_נתיב/'examples/report.json').read_text())
    if sorted(שיק_גודל['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 גודל 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('עברית Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(שיק_רזולוציה['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 בפועל_נתונים 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != קוד_Hash_קובץ(לשקף_בסיס/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 הקודם_ערך 라이브러리가 바뀌었습니다.')
    for שם in ('한국어통신시험','한국어예외시험'):
        if not any(ערך_ערך['name']==שם and ערך_ערך.get('openjdk_output_equal') for ערך_ערך in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+שם)
    חריגה_רשימה = sorted(נתיב.stem for נתיב in (לשקף_בסיס/'한국어자바/עברית/עצמי').glob('*חריגה.java'))
    חריגה_לרשום = (אימות_נתיב/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for שם in חריגה_רשימה:
        if '\n'+שם+'\n' not in חריגה_לרשום: raise SystemExit('חריגה יצר·잡기·설명 시험 필요: '+שם)
    מפרט = json.loads((לשקף_בסיס/'dist/manifest.json').read_text())
    if מפרט['image_sha256'] != קוד_Hash_קובץ(לשקף_בסיס/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('הפצה_ערך תמונה_ערך קוד_Hash_קובץ 불일치')
    with zipfile.ZipFile(str(לשקף_בסיס/'dist/jkoros-native-rpi4-boot.zip')) as חבילה:
        if hashlib.sha256(חבילה.read('kernel8.img')).hexdigest() != ליבה_קוד_Hash:
            raise SystemExit('부팅 ZIP ליבה_ערך 불일치')
        부팅설정 = חבילה.read('config.txt')
        for שם, גודל in zip(('width', 'height'), מפרט['framebuffer_resolution']):
            if 'framebuffer_'+שם+'='+str(גודל) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 הגדרות 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(לשקף_בסיס/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(לשקף_בסיס/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if קוד_Hash_קובץ(복사본) != ליבה_קוד_Hash: raise SystemExit('SD תמונה_ערך ליבה_ערך 불일치')
        מופע_הגדרות = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(לשקף_בסיס/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(מופע_הגדרות)])
        if מופע_הגדרות.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 הגדרות 불일치')
    לרשום_שיא = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ליבה_קוד_Hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': חריגה_רשימה, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(שיק_רזולוציה['resolutions']),
            'sd_framebuffer_resolution': מפרט['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {שם:קוד_Hash_קובץ(לשקף_בסיס/'dist'/שם) for שם in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (אימות_נתיב/'native-runtime-summary.json').write_text(json.dumps(לרשום_שיא,ensure_ascii=False,indent=2)+'\n')
    print('PASS: נוכחי_פריט 커널의',len(기록들),'개 통합 시험 לרשום_שיא, עברית חריגה',len(חריגה_רשימה),'כיתה_הגדרה, SD תמונה_ערך·ZIP 일치')

if __name__ == '__main__': הפעלה()
