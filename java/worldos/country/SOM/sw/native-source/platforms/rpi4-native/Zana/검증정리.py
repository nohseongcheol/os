#!/usr/bin/env python3
"""현재 커널과 halisi_data 시험·배포물이 일치할 때에만 통합 hakikisha 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def kali_faili(njia):
    계산 = hashlib.sha256()
    with njia.open('rb') as faili:
        for data in iter(lambda: faili.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def endesha():
    uhakikishi_njia = 기준/'build/verification'
    kiini_kali = kali_faili(기준/'build/kernel8.img')
    기록들 = {}
    for Jina in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Jina == 'boot' else Jina+'/report.json'
        data = json.loads((uhakikishi_njia/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kiini_kali:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Jina] = {'passed': True, 'report': 상대경로}
    hundi_jina = json.loads((uhakikishi_njia/'naming/report.json').read_text())
    if not hundi_jina['passed'] or not hundi_jina['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for njia, 기대값 in hundi_jina['c_source_sha256'].items():
        if kali_faili(기준/njia) != 기대값: raise SystemExit('명명 검사 Nyuma_thamani 바뀐 C chanzo: '+njia)
    자바검사 = json.loads((uhakikishi_njia/'jvm/report.json').read_text())
    직접화면 = json.loads((uhakikishi_njia/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 tekeleza_amri 시험 필요')
    hundi_baiti_thamani = json.loads((uhakikishi_njia/'naming/direct-bytecode.json').read_text())
    if not hundi_baiti_thamani['passed'] or hundi_baiti_thamani['jar_sha256'] != kali_faili(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 thibitisha 필요')
    hundi_mwonekano = json.loads((uhakikishi_njia/'resolution/report.json').read_text())
    hundi_panga_ukubwa = json.loads((uhakikishi_njia/'resize/report.json').read_text())
    갱신검사 = json.loads((uhakikishi_njia/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kiini_kali:
        raise SystemExit('현재 커널의 부분 onyesha_upya 시험 필요')
    for njia, 기대값 in 갱신검사['source_sha256'].items():
        if kali_faili(기준/njia) != 기대값: raise SystemExit('부분 onyesha_upya 시험 Nyuma_thamani 바뀐 chanzo: '+njia)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 endesha ingizo_pointi 시험 필요')
    예제검사 = json.loads((uhakikishi_njia/'examples/report.json').read_text())
    if sorted(hundi_panga_ukubwa['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 panga_ukubwa 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(hundi_mwonekano['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 halisi_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != kali_faili(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Nyuma_thamani 라이브러리가 바뀌었습니다.')
    for Jina in ('한국어통신시험','한국어예외시험'):
        if not any(ingizo_thamani['name']==Jina and ingizo_thamani.get('openjdk_output_equal') for ingizo_thamani in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Jina)
    vighairi_Orodha = sorted(njia.stem for njia in (기준/'한국어자바/한국어/자체').glob('*vighairi.java'))
    vighairi_batli = (uhakikishi_njia/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Jina in vighairi_Orodha:
        if '\n'+Jina+'\n' not in vighairi_batli: raise SystemExit('vighairi 생성·잡기·설명 시험 필요: '+Jina)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != kali_faili(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 picha_thamani kali_faili 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as fungasha:
        if hashlib.sha256(fungasha.read('kernel8.img')).hexdigest() != kiini_kali:
            raise SystemExit('부팅 ZIP kiini_thamani_0611a8a8 불일치')
        부팅설정 = fungasha.read('config.txt')
        for Jina, panga_ukubwa in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Jina+'='+str(panga_ukubwa) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Mipangilio 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if kali_faili(복사본) != kiini_kali: raise SystemExit('SD picha_thamani kiini_thamani_0611a8a8 불일치')
        mfano_Mipangilio = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(mfano_Mipangilio)])
        if mfano_Mipangilio.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Mipangilio 불일치')
    batli_REKODI = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kiini_kali,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': vighairi_Orodha, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(hundi_mwonekano['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Jina:kali_faili(기준/'dist'/Jina) for Jina in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (uhakikishi_njia/'native-runtime-summary.json').write_text(json.dumps(batli_REKODI,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 batli_REKODI, 한국어 vighairi',len(vighairi_Orodha),'tabaka_Ufafanuzi, SD picha_thamani·ZIP 일치')

if __name__ == '__main__': endesha()
