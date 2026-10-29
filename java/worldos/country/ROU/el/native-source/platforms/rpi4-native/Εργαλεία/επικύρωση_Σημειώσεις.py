#!/usr/bin/env python3
"""τρέχων_στοιχείο 커널과 πραγματικός_δεδομένα 시험·배포물이 일치할 때에만 통합 επικυρώνω 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

έργο_ρίζα = Path(__file__).resolve().parents[1]

def κατακερματισμός_Αρχείο(ΔΙΑΔΡΟΜΗ):
    계산 = hashlib.sha256()
    with ΔΙΑΔΡΟΜΗ.open('rb') as Αρχείο:
        for δεδομένα in iter(lambda: Αρχείο.read(1048576), b''): 계산.update(δεδομένα)
    return 계산.hexdigest()

def Εκτέλεση_2():
    επικύρωση_διαδρομή = έργο_ρίζα/'build/verification'
    πυρήνας_κατακερματισμός = κατακερματισμός_Αρχείο(έργο_ρίζα/'build/kernel8.img')
    기록들 = {}
    for Όνομα in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        σχετική_διαδρομή = 'report.json' if Όνομα == 'boot' else Όνομα+'/report.json'
        δεδομένα = json.loads((επικύρωση_διαδρομή/σχετική_διαδρομή).read_text())
        if not δεδομένα.get('passed') or δεδομένα.get('kernel_sha256') != πυρήνας_κατακερματισμός:
            raise SystemExit('τρέχων_στοιχείο 커널에 대한 성공 기록이 필요합니다: '+σχετική_διαδρομή)
        기록들[Όνομα] = {'passed': True, 'report': σχετική_διαδρομή}
    ελέγχω_όνομα = json.loads((επικύρωση_διαδρομή/'naming/report.json').read_text())
    if not ελέγχω_όνομα['passed'] or not ελέγχω_όνομα['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ΔΙΑΔΡΟΜΗ, 기대값 in ελέγχω_όνομα['c_source_sha256'].items():
        if κατακερματισμός_Αρχείο(έργο_ρίζα/ΔΙΑΔΡΟΜΗ) != 기대값: raise SystemExit('명명 검사 Πίσω_τιμή 바뀐 C ΠΗΓΗ: '+ΔΙΑΔΡΟΜΗ)
    자바검사 = json.loads((επικύρωση_διαδρομή/'jvm/report.json').read_text())
    직접화면 = json.loads((επικύρωση_διαδρομή/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('ελληνικά 직접 화면 εκτελώ_εντολή 시험 필요')
    바이트검사 = json.loads((επικύρωση_διαδρομή/'naming/direct-bytecode.json').read_text())
    if not 바이트검사['passed'] or 바이트검사['jar_sha256'] != κατακερματισμός_Αρχείο(έργο_ρίζα/'dist/jkoros-native-korean.jar'):
        raise SystemExit('τρέχων_στοιχείο ελληνικά 라이브러리의 직접 호출 바이트코드 επαληθεύω 필요')
    ελέγχω_ανάλυση = json.loads((επικύρωση_διαδρομή/'resolution/report.json').read_text())
    ελέγχω_αλλάζω_μέγεθος = json.loads((επικύρωση_διαδρομή/'resize/report.json').read_text())
    갱신검사 = json.loads((επικύρωση_διαδρομή/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != πυρήνας_κατακερματισμός:
        raise SystemExit('τρέχων_στοιχείο 커널의 부분 ανανεώνω 시험 필요')
    for ΔΙΑΔΡΟΜΗ, 기대값 in 갱신검사['source_sha256'].items():
        if κατακερματισμός_Αρχείο(έργο_ρίζα/ΔΙΑΔΡΟΜΗ) != 기대값: raise SystemExit('부분 ανανεώνω 시험 Πίσω_τιμή 바뀐 ΠΗΓΗ: '+ΔΙΑΔΡΟΜΗ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('ελληνικά 직접 가닥과 Εκτέλεση_2 σημείο_εισόδου 시험 필요')
    예제검사 = json.loads((επικύρωση_διαδρομή/'examples/report.json').read_text())
    if sorted(ελέγχω_αλλάζω_μέγεθος['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Μέγεθος 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('ελληνικά Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ελέγχω_ανάλυση['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 πραγματικός_δεδομένα 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != κατακερματισμός_Αρχείο(έργο_ρίζα/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Πίσω_τιμή 라이브러리가 바뀌었습니다.')
    for Όνομα in ('한국어통신시험','한국어예외시험'):
        if not any(καταχώρηση_τιμή['name']==Όνομα and καταχώρηση_τιμή.get('openjdk_output_equal') for καταχώρηση_τιμή in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Όνομα)
    εξαίρεση_Λίστα = sorted(ΔΙΑΔΡΟΜΗ.stem for ΔΙΑΔΡΟΜΗ in (έργο_ρίζα/'한국어자바/ελληνικά/ίδιο').glob('*εξαίρεση.java'))
    εξαίρεση_καταγράφω = (επικύρωση_διαδρομή/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Όνομα in εξαίρεση_Λίστα:
        if '\n'+Όνομα+'\n' not in εξαίρεση_καταγράφω: raise SystemExit('εξαίρεση δημιουργώ·잡기·설명 시험 필요: '+Όνομα)
    명세 = json.loads((έργο_ρίζα/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != κατακερματισμός_Αρχείο(έργο_ρίζα/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 εικόνα_τιμή κατακερματισμός_Αρχείο 불일치')
    with zipfile.ZipFile(str(έργο_ρίζα/'dist/jkoros-native-rpi4-boot.zip')) as πακέτο:
        if hashlib.sha256(πακέτο.read('kernel8.img')).hexdigest() != πυρήνας_κατακερματισμός:
            raise SystemExit('부팅 ZIP πυρήνας_τιμή 불일치')
        부팅설정 = πακέτο.read('config.txt')
        for Όνομα, Μέγεθος in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Όνομα+'='+str(Μέγεθος) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Ρυθμίσεις 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(έργο_ρίζα/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(έργο_ρίζα/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if κατακερματισμός_Αρχείο(복사본) != πυρήνας_κατακερματισμός: raise SystemExit('SD εικόνα_τιμή πυρήνας_τιμή 불일치')
        παρουσία_Ρυθμίσεις = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(έργο_ρίζα/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(παρουσία_Ρυθμίσεις)])
        if παρουσία_Ρυθμίσεις.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Ρυθμίσεις 불일치')
    καταγράφω_ρεκόρ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': πυρήνας_κατακερματισμός,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': εξαίρεση_Λίστα, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ελέγχω_ανάλυση['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Όνομα:κατακερματισμός_Αρχείο(έργο_ρίζα/'dist'/Όνομα) for Όνομα in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (επικύρωση_διαδρομή/'native-runtime-summary.json').write_text(json.dumps(καταγράφω_ρεκόρ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: τρέχων_στοιχείο 커널의',len(기록들),'개 통합 시험 καταγράφω_ρεκόρ, ελληνικά εξαίρεση',len(εξαίρεση_Λίστα),'Τάξη_Ορισμός, SD εικόνα_τιμή·ZIP 일치')

if __name__ == '__main__': Εκτέλεση_2()
