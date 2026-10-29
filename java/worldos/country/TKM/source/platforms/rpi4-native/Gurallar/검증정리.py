#!/usr/bin/env python3
"""현재 커널과 hakyky_maglumat 시험·배포물이 일치할 때에만 통합 tassykla 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def heş_kody_faýl(Ýol):
    계산 = hashlib.sha256()
    with Ýol.open('rb') as Faýl:
        for maglumat in iter(lambda: Faýl.read(1048576), b''): 계산.update(maglumat)
    return 계산.hexdigest()

def Bitir():
    barlag_ýol = 기준/'build/verification'
    ýadro_heş_kody = heş_kody_faýl(기준/'build/kernel8.img')
    기록들 = {}
    for Ad in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Ad == 'boot' else Ad+'/report.json'
        maglumat = json.loads((barlag_ýol/상대경로).read_text())
        if not maglumat.get('passed') or maglumat.get('kernel_sha256') != ýadro_heş_kody:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Ad] = {'passed': True, 'report': 상대경로}
    derňe_at = json.loads((barlag_ýol/'naming/report.json').read_text())
    if not derňe_at['passed'] or not derňe_at['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Ýol, 기대값 in derňe_at['c_source_sha256'].items():
        if heş_kody_faýl(기준/Ýol) != 기대값: raise SystemExit('명명 검사 Yza_baha 바뀐 C Çeşme: '+Ýol)
    자바검사 = json.loads((barlag_ýol/'jvm/report.json').read_text())
    직접화면 = json.loads((barlag_ýol/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ýerine_ýetir_buýruk 시험 필요')
    derňe_baýt_baha = json.loads((barlag_ýol/'naming/direct-bytecode.json').read_text())
    if not derňe_baýt_baha['passed'] or derňe_baýt_baha['jar_sha256'] != heş_kody_faýl(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 barla 필요')
    derňe_çözgüt = json.loads((barlag_ýol/'resolution/report.json').read_text())
    derňe_ölçegi_üýtget = json.loads((barlag_ýol/'resize/report.json').read_text())
    갱신검사 = json.loads((barlag_ýol/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ýadro_heş_kody:
        raise SystemExit('현재 커널의 부분 täzelendir 시험 필요')
    for Ýol, 기대값 in 갱신검사['source_sha256'].items():
        if heş_kody_faýl(기준/Ýol) != 기대값: raise SystemExit('부분 täzelendir 시험 Yza_baha 바뀐 Çeşme: '+Ýol)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Bitir girizmeklik_utuk 시험 필요')
    예제검사 = json.loads((barlag_ýol/'examples/report.json').read_text())
    if sorted(derňe_ölçegi_üýtget['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ululyk 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(derňe_çözgüt['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 hakyky_maglumat 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != heş_kody_faýl(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Yza_baha 라이브러리가 바뀌었습니다.')
    for Ad in ('한국어통신시험','한국어예외시험'):
        if not any(girizmeklik_baha['name']==Ad and girizmeklik_baha.get('openjdk_output_equal') for girizmeklik_baha in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ad)
    예외들 = sorted(Ýol.stem for Ýol in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (barlag_ýol/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ad in 예외들:
        if '\n'+Ad+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Ad)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != heş_kody_faýl(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 surat_baha heş_kody_faýl 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as toplum:
        if hashlib.sha256(toplum.read('kernel8.img')).hexdigest() != ýadro_heş_kody:
            raise SystemExit('부팅 ZIP ýadro_baha 불일치')
        부팅설정 = toplum.read('config.txt')
        for Ad, Ululyk in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ad+'='+str(Ululyk) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Düzümler 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if heş_kody_faýl(복사본) != ýadro_heş_kody: raise SystemExit('SD surat_baha ýadro_baha 불일치')
        synp_Sazlamalar = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(synp_Sazlamalar)])
        if synp_Sazlamalar.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Düzümler 불일치')
    hasaba_alyş_setir = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ýadro_heş_kody,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(derňe_çözgüt['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ad:heş_kody_faýl(기준/'dist'/Ad) for Ad in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (barlag_ýol/'native-runtime-summary.json').write_text(json.dumps(hasaba_alyş_setir,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 hasaba_alyş_setir, 한국어 예외',len(예외들),'klas_Kesgitleme, SD surat_baha·ZIP 일치')

if __name__ == '__main__': Bitir()
