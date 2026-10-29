#!/usr/bin/env python3
"""geçerli_öğe 커널과 fiili_veri sınamalar·배포물이 일치할 때에만 통합 doğrulamak_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

işlem_kök = Path(__file__).resolve().parents[1]

def özet_Dosya(yol):
    계산 = hashlib.sha256()
    with yol.open('rb') as dosya:
        for veri in iter(lambda: dosya.read(1048576), b''): 계산.update(veri)
    return 계산.hexdigest()

def çalıştır():
    doğrulama_yol = işlem_kök/'build/verification'
    çekirdek_özet = özet_Dosya(işlem_kök/'build/kernel8.img')
    기록들 = {}
    for İsim in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        göreli_yol = 'report.json' if İsim == 'boot' else İsim+'/report.json'
        veri = json.loads((doğrulama_yol/göreli_yol).read_text())
        if not veri.get('passed') or veri.get('kernel_sha256') != çekirdek_özet:
            raise SystemExit('geçerli_öğe 커널에 대한 성공 기록이 필요합니다: '+göreli_yol)
        기록들[İsim] = {'passed': True, 'report': göreli_yol}
    çek_ad = json.loads((doğrulama_yol/'naming/report.json').read_text())
    if not çek_ad['passed'] or not çek_ad['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for yol, 기대값 in çek_ad['c_source_sha256'].items():
        if özet_Dosya(işlem_kök/yol) != 기대값: raise SystemExit('명명 검사 BACK_değer 바뀐 C kaynakKod: '+yol)
    자바검사 = json.loads((doğrulama_yol/'jvm/report.json').read_text())
    직접화면 = json.loads((doğrulama_yol/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Türkçe 직접 화면 yürütmek_komut sınamalar 필요')
    çek_bayt_değer = json.loads((doğrulama_yol/'naming/direct-bytecode.json').read_text())
    if not çek_bayt_değer['passed'] or çek_bayt_değer['jar_sha256'] != özet_Dosya(işlem_kök/'dist/jkoros-native-korean.jar'):
        raise SystemExit('geçerli_öğe Türkçe 라이브러리의 직접 호출 바이트코드 doğrulamak 필요')
    çek_çözme = json.loads((doğrulama_yol/'resolution/report.json').read_text())
    çek_boyutlandırmak = json.loads((doğrulama_yol/'resize/report.json').read_text())
    갱신검사 = json.loads((doğrulama_yol/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != çekirdek_özet:
        raise SystemExit('geçerli_öğe 커널의 부분 yenilemek sınamalar 필요')
    for yol, 기대값 in 갱신검사['source_sha256'].items():
        if özet_Dosya(işlem_kök/yol) != 기대값: raise SystemExit('부분 yenilemek sınamalar BACK_değer 바뀐 kaynakKod: '+yol)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Türkçe 직접 가닥과 çalıştır giriş_noktası sınamalar 필요')
    예제검사 = json.loads((doğrulama_yol/'examples/report.json').read_text())
    if sorted(çek_boyutlandırmak['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Boyut 조절 sınamalar 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Türkçe Swing 창을 포함한 예제 13개 sınamalar 필요')
    if sorted(çek_çözme['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 fiili_veri 화면 sınamalar 필요')
    if 자바검사['korean_library_sha256'] != özet_Dosya(işlem_kök/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 sınamalar BACK_değer 라이브러리가 바뀌었습니다.')
    for İsim in ('한국어통신시험','한국어예외시험'):
        if not any(girdi_değer['name']==İsim and girdi_değer.get('openjdk_output_equal') for girdi_değer in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 sınamalar 필요: '+İsim)
    özel_durum_Liste = sorted(yol.stem for yol in (işlem_kök/'한국어자바/Türkçe/Öz').glob('*özel_durum.java'))
    özel_durum_LOG = (doğrulama_yol/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for İsim in özel_durum_Liste:
        if '\n'+İsim+'\n' not in özel_durum_LOG: raise SystemExit('özel_durum oluşturmak·잡기·설명 sınamalar 필요: '+İsim)
    명세 = json.loads((işlem_kök/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != özet_Dosya(işlem_kök/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('dağıtım_değer RESİM_değer özet_Dosya 불일치')
    with zipfile.ZipFile(str(işlem_kök/'dist/jkoros-native-rpi4-boot.zip')) as paket_iş:
        if hashlib.sha256(paket_iş.read('kernel8.img')).hexdigest() != çekirdek_özet:
            raise SystemExit('makine_başlatma ZIP çekirdek_değer 불일치')
        부팅설정 = paket_iş.read('config.txt')
        for İsim, Boyut in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+İsim+'='+str(Boyut) not in 부팅설정.decode().splitlines():
                raise SystemExit('makine_başlatma ZIP 화면 Ayarlar 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(işlem_kök/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(işlem_kök/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if özet_Dosya(복사본) != çekirdek_özet: raise SystemExit('SD RESİM_değer çekirdek_değer 불일치')
        örnek_Ayarlar = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(işlem_kök/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(örnek_Ayarlar)])
        if örnek_Ayarlar.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Ayarlar 불일치')
    LOG_KAYIT = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': çekirdek_özet,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': özel_durum_Liste, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(çek_çözme['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {İsim:özet_Dosya(işlem_kök/'dist'/İsim) for İsim in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (doğrulama_yol/'native-runtime-summary.json').write_text(json.dumps(LOG_KAYIT,ensure_ascii=False,indent=2)+'\n')
    print('PASS: geçerli_öğe 커널의',len(기록들),'개 통합 sınamalar LOG_KAYIT, Türkçe özel_durum',len(özel_durum_Liste),'Sınıf_Tanım, SD RESİM_değer·ZIP 일치')

if __name__ == '__main__': çalıştır()
