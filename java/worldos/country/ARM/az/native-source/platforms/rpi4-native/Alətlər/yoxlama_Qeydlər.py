#!/usr/bin/env python3
"""현재 커널과 faktiki_verilənlər 시험·배포물이 일치할 때에만 통합 təsdiqlə 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_kök = Path(__file__).resolve().parents[1]

def heş_fayl(Cığır):
    계산 = hashlib.sha256()
    with Cığır.open('rb') as FAYL:
        for verilənlər in iter(lambda: FAYL.read(1048576), b''): 계산.update(verilənlər)
    return 계산.hexdigest()

def İcra_Et():
    yoxlama_yol = Project_kök/'build/verification'
    nüvə_heş = heş_fayl(Project_kök/'build/kernel8.img')
    기록들 = {}
    for Ad in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Ad == 'boot' else Ad+'/report.json'
        verilənlər = json.loads((yoxlama_yol/상대경로).read_text())
        if not verilənlər.get('passed') or verilənlər.get('kernel_sha256') != nüvə_heş:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Ad] = {'passed': True, 'report': 상대경로}
    çek_ad = json.loads((yoxlama_yol/'naming/report.json').read_text())
    if not çek_ad['passed'] or not çek_ad['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Cığır, 기대값 in çek_ad['c_source_sha256'].items():
        if heş_fayl(Project_kök/Cığır) != 기대값: raise SystemExit('명명 검사 GERİ_VALUE 바뀐 C QAYNAQ: '+Cığır)
    자바검사 = json.loads((yoxlama_yol/'jvm/report.json').read_text())
    직접화면 = json.loads((yoxlama_yol/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 icra_etmək_əmr 시험 필요')
    çek_bayt_VALUE = json.loads((yoxlama_yol/'naming/direct-bytecode.json').read_text())
    if not çek_bayt_VALUE['passed'] or çek_bayt_VALUE['jar_sha256'] != heş_fayl(Project_kök/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 yoxlamaq 필요')
    çek_əksetmə_qabiliyyəti = json.loads((yoxlama_yol/'resolution/report.json').read_text())
    çek_ölçünü_dəyişmək = json.loads((yoxlama_yol/'resize/report.json').read_text())
    갱신검사 = json.loads((yoxlama_yol/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != nüvə_heş:
        raise SystemExit('현재 커널의 부분 təzələmək 시험 필요')
    for Cığır, 기대값 in 갱신검사['source_sha256'].items():
        if heş_fayl(Project_kök/Cığır) != 기대값: raise SystemExit('부분 təzələmək 시험 GERİ_VALUE 바뀐 QAYNAQ: '+Cığır)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 İcra_Et daxiletmə_p 시험 필요')
    예제검사 = json.loads((yoxlama_yol/'examples/report.json').read_text())
    if sorted(çek_ölçünü_dəyişmək['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Böyüklük 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(çek_əksetmə_qabiliyyəti['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 faktiki_verilənlər 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != heş_fayl(Project_kök/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 GERİ_VALUE 라이브러리가 바뀌었습니다.')
    for Ad in ('한국어통신시험','한국어예외시험'):
        if not any(daxiletmə_VALUE['name']==Ad and daxiletmə_VALUE.get('openjdk_output_equal') for daxiletmə_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ad)
    istisna_Siyahı = sorted(Cığır.stem for Cığır in (Project_kök/'한국어자바/한국어/자체').glob('*istisna.java'))
    istisna_LOG = (yoxlama_yol/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ad in istisna_Siyahı:
        if '\n'+Ad+'\n' not in istisna_LOG: raise SystemExit('istisna yarat·잡기·설명 시험 필요: '+Ad)
    명세 = json.loads((Project_kök/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != heş_fayl(Project_kök/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE heş_fayl 불일치')
    with zipfile.ZipFile(str(Project_kök/'dist/jkoros-native-rpi4-boot.zip')) as paket:
        if hashlib.sha256(paket.read('kernel8.img')).hexdigest() != nüvə_heş:
            raise SystemExit('부팅 ZIP nüvə_VALUE 불일치')
        부팅설정 = paket.read('config.txt')
        for Ad, Böyüklük in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ad+'='+str(Böyüklük) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Sazlama 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_kök/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_kök/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if heş_fayl(복사본) != nüvə_heş: raise SystemExit('SD IMAGE_VALUE nüvə_VALUE 불일치')
        nümunə_Parametrlər = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_kök/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(nümunə_Parametrlər)])
        if nümunə_Parametrlər.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Sazlama 불일치')
    LOG_yaz = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': nüvə_heş,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': istisna_Siyahı, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(çek_əksetmə_qabiliyyəti['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ad:heş_fayl(Project_kök/'dist'/Ad) for Ad in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (yoxlama_yol/'native-runtime-summary.json').write_text(json.dumps(LOG_yaz,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_yaz, 한국어 istisna',len(istisna_Siyahı),'Sinif_Tərif, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': İcra_Et()
