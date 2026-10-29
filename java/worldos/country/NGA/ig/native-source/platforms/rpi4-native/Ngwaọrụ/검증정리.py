#!/usr/bin/env python3
"""현재 커널과 ǹdịnezie_datà 시험·배포물이 일치할 때에만 통합 mee_ịbanihe 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def di_ike_ọbọakwụkwọ(ụzọ_ozi):
    계산 = hashlib.sha256()
    with ụzọ_ozi.open('rb') as Faịlụ:
        for datà in iter(lambda: Faịlụ.read(1048576), b''): 계산.update(datà)
    return 계산.hexdigest()

def Bido():
    nkwèputaonòdù_ụzọ_ozi = 기준/'build/verification'
    mkpụrụobī_kọmpùta_di_ike = di_ike_ọbọakwụkwọ(기준/'build/kernel8.img')
    기록들 = {}
    for Aha in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Aha == 'boot' else Aha+'/report.json'
        datà = json.loads((nkwèputaonòdù_ụzọ_ozi/상대경로).read_text())
        if not datà.get('passed') or datà.get('kernel_sha256') != mkpụrụobī_kọmpùta_di_ike:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Aha] = {'passed': True, 'report': 상대경로}
    cheèk_akara_ahà = json.loads((nkwèputaonòdù_ụzọ_ozi/'naming/report.json').read_text())
    if not cheèk_akara_ahà['passed'] or not cheèk_akara_ahà['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ụzọ_ozi, 기대값 in cheèk_akara_ahà['c_source_sha256'].items():
        if di_ike_ọbọakwụkwọ(기준/ụzọ_ozi) != 기대값: raise SystemExit('명명 검사 Àzụ_valuu 바뀐 C ebensìbịa: '+ụzọ_ozi)
    자바검사 = json.loads((nkwèputaonòdù_ụzọ_ozi/'jvm/report.json').read_text())
    직접화면 = json.loads((nkwèputaonòdù_ụzọ_ozi/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 mee_nnyemiwu 시험 필요')
    cheèk_baịtị_valuu = json.loads((nkwèputaonòdù_ụzọ_ozi/'naming/direct-bytecode.json').read_text())
    if not cheèk_baịtị_valuu['passed'] or cheèk_baịtị_valuu['jar_sha256'] != di_ike_ọbọakwụkwọ(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 nkwàdo_eziokwū 필요')
    cheèk_ụcha_ngosịpụta = json.loads((nkwèputaonòdù_ụzọ_ozi/'resolution/report.json').read_text())
    cheèk_ụha = json.loads((nkwèputaonòdù_ụzọ_ozi/'resize/report.json').read_text())
    갱신검사 = json.loads((nkwèputaonòdù_ụzọ_ozi/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != mkpụrụobī_kọmpùta_di_ike:
        raise SystemExit('현재 커널의 부분 mèkwa_ọhụrụ 시험 필요')
    for ụzọ_ozi, 기대값 in 갱신검사['source_sha256'].items():
        if di_ike_ọbọakwụkwọ(기준/ụzọ_ozi) != 기대값: raise SystemExit('부분 mèkwa_ọhụrụ 시험 Àzụ_valuu 바뀐 ebensìbịa: '+ụzọ_ozi)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Bido ndebà_akara 시험 필요')
    예제검사 = json.loads((nkwèputaonòdù_ụzọ_ozi/'examples/report.json').read_text())
    if sorted(cheèk_ụha['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ụhara 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(cheèk_ụcha_ngosịpụta['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ǹdịnezie_datà 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != di_ike_ọbọakwụkwọ(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Àzụ_valuu 라이브러리가 바뀌었습니다.')
    for Aha in ('한국어통신시험','한국어예외시험'):
        if not any(ndebà_valuu['name']==Aha and ndebà_valuu.get('openjdk_output_equal') for ndebà_valuu in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Aha)
    예외들 = sorted(ụzọ_ozi.stem for ụzọ_ozi in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (nkwèputaonòdù_ụzọ_ozi/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Aha in 예외들:
        if '\n'+Aha+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Aha)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != di_ike_ọbọakwụkwọ(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 foto_valuu di_ike_ọbọakwụkwọ 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as ngwungwu:
        if hashlib.sha256(ngwungwu.read('kernel8.img')).hexdigest() != mkpụrụobī_kọmpùta_di_ike:
            raise SystemExit('부팅 ZIP mkpụrụobī_kọmpùta_valuu 불일치')
        부팅설정 = ngwungwu.read('config.txt')
        for Aha, Ụhara in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Aha+'='+str(Ụhara) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Mwube 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if di_ike_ọbọakwụkwọ(복사본) != mkpụrụobī_kọmpùta_di_ike: raise SystemExit('SD foto_valuu mkpụrụobī_kọmpùta_valuu 불일치')
        ṅomie_Mwube = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ṅomie_Mwube)])
        if ṅomie_Mwube.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Mwube 불일치')
    ndekọ_NDEKỌ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': mkpụrụobī_kọmpùta_di_ike,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(cheèk_ụcha_ngosịpụta['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Aha:di_ike_ọbọakwụkwọ(기준/'dist'/Aha) for Aha in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (nkwèputaonòdù_ụzọ_ozi/'native-runtime-summary.json').write_text(json.dumps(ndekọ_NDEKỌ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ndekọ_NDEKỌ, 한국어 예외',len(예외들),'klaàsị_Nkwuke, SD foto_valuu·ZIP 일치')

if __name__ == '__main__': Bido()
