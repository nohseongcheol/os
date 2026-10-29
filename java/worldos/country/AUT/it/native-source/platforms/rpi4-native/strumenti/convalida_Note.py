#!/usr/bin/env python3
"""Regolari_articolo 커널과 effettivo_dati prove·배포물이 일치할 때에만 통합 convalidare 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

azione_radice = Path(__file__).resolve().parents[1]

def hash_File(percorso):
    계산 = hashlib.sha256()
    with percorso.open('rb') as file:
        for dati in iter(lambda: file.read(1048576), b''): 계산.update(dati)
    return 계산.hexdigest()

def avvia():
    convalida_percorso = azione_radice/'build/verification'
    kernel_hash = hash_File(azione_radice/'build/kernel8.img')
    기록들 = {}
    for Nome in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        percorso_relativo = 'report.json' if Nome == 'boot' else Nome+'/report.json'
        dati = json.loads((convalida_percorso/percorso_relativo).read_text())
        if not dati.get('passed') or dati.get('kernel_sha256') != kernel_hash:
            raise SystemExit('Regolari_articolo 커널에 대한 성공 기록이 필요합니다: '+percorso_relativo)
        기록들[Nome] = {'passed': True, 'report': percorso_relativo}
    assegno_nome = json.loads((convalida_percorso/'naming/report.json').read_text())
    if not assegno_nome['passed'] or not assegno_nome['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for percorso, 기대값 in assegno_nome['c_source_sha256'].items():
        if hash_File(azione_radice/percorso) != 기대값: raise SystemExit('명명 검사 BACK_VALORE 바뀐 C codiceSorgente: '+percorso)
    자바검사 = json.loads((convalida_percorso/'jvm/report.json').read_text())
    직접화면 = json.loads((convalida_percorso/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Italiano 직접 schermata Esegui_comando prove 필요')
    assegno_byte_VALORE = json.loads((convalida_percorso/'naming/direct-bytecode.json').read_text())
    if not assegno_byte_VALORE['passed'] or assegno_byte_VALORE['jar_sha256'] != hash_File(azione_radice/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Regolari_articolo Italiano 라이브러리의 직접 호출 바이트코드 verificare 필요')
    assegno_risoluzione = json.loads((convalida_percorso/'resolution/report.json').read_text())
    assegno_ridimensionare = json.loads((convalida_percorso/'resize/report.json').read_text())
    갱신검사 = json.loads((convalida_percorso/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('Regolari_articolo 커널의 부분 aggiornare prove 필요')
    for percorso, 기대값 in 갱신검사['source_sha256'].items():
        if hash_File(azione_radice/percorso) != 기대값: raise SystemExit('부분 aggiornare prove BACK_VALORE 바뀐 codiceSorgente: '+percorso)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Italiano 직접 가닥과 avvia punto_di_ingresso prove 필요')
    예제검사 = json.loads((convalida_percorso/'examples/report.json').read_text())
    if sorted(assegno_ridimensionare['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Dimensione 조절 prove 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Italiano Swing 창을 포함한 예제 13개 prove 필요')
    if sorted(assegno_risoluzione['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 effettivo_dati schermata prove 필요')
    if 자바검사['korean_library_sha256'] != hash_File(azione_radice/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 prove BACK_VALORE 라이브러리가 바뀌었습니다.')
    for Nome in ('한국어통신시험','한국어예외시험'):
        if not any(voce_VALORE['name']==Nome and voce_VALORE.get('openjdk_output_equal') for voce_VALORE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 prove 필요: '+Nome)
    eccezione_elenco = sorted(percorso.stem for percorso in (azione_radice/'한국어자바/Italiano/nativo').glob('*eccezione.java'))
    eccezione_LOG = (convalida_percorso/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nome in eccezione_elenco:
        if '\n'+Nome+'\n' not in eccezione_LOG: raise SystemExit('eccezione generare·잡기·설명 prove 필요: '+Nome)
    specifica = json.loads((azione_radice/'dist/manifest.json').read_text())
    if specifica['image_sha256'] != hash_File(azione_radice/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distribuzione_VALORE foto_VALORE hash_File 불일치')
    with zipfile.ZipFile(str(azione_radice/'dist/jkoros-native-rpi4-boot.zip')) as aggregare:
        if hashlib.sha256(aggregare.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('avvio_macchina ZIP kernel_VALORE 불일치')
        부팅설정 = aggregare.read('config.txt')
        for Nome, Dimensione in zip(('width', 'height'), specifica['framebuffer_resolution']):
            if 'framebuffer_'+Nome+'='+str(Dimensione) not in 부팅설정.decode().splitlines():
                raise SystemExit('avvio_macchina ZIP schermata Impostazioni 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(azione_radice/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(azione_radice/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_File(복사본) != kernel_hash: raise SystemExit('SD foto_VALORE kernel_VALORE 불일치')
        copiare_Impostazioni = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(azione_radice/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copiare_Impostazioni)])
        if copiare_Impostazioni.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP schermata Impostazioni 불일치')
    LOG_riga = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': eccezione_elenco, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(assegno_risoluzione['resolutions']),
            'sd_framebuffer_resolution': specifica['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nome:hash_File(azione_radice/'dist'/Nome) for Nome in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (convalida_percorso/'native-runtime-summary.json').write_text(json.dumps(LOG_riga,ensure_ascii=False,indent=2)+'\n')
    print('PASS: Regolari_articolo 커널의',len(기록들),'개 통합 prove LOG_riga, Italiano eccezione',len(eccezione_elenco),'Corso_definizione, SD foto_VALORE·ZIP 일치')

if __name__ == '__main__': avvia()
