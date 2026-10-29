#!/usr/bin/env python3
"""em_dia_item 커널과 real_dados testes·배포물이 일치할 때에만 통합 validar 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ação_raiz = Path(__file__).resolve().parents[1]

def hash_Arquivo(caminho):
    계산 = hashlib.sha256()
    with caminho.open('rb') as ficheiro:
        for dados in iter(lambda: ficheiro.read(1048576), b''): 계산.update(dados)
    return 계산.hexdigest()

def iniciar():
    validação_caminho = ação_raiz/'build/verification'
    kernel_hash = hash_Arquivo(ação_raiz/'build/kernel8.img')
    기록들 = {}
    for Nome in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        caminho_relativo = 'report.json' if Nome == 'boot' else Nome+'/report.json'
        dados = json.loads((validação_caminho/caminho_relativo).read_text())
        if not dados.get('passed') or dados.get('kernel_sha256') != kernel_hash:
            raise SystemExit('em_dia_item 커널에 대한 성공 기록이 필요합니다: '+caminho_relativo)
        기록들[Nome] = {'passed': True, 'report': caminho_relativo}
    cheque_nome = json.loads((validação_caminho/'naming/report.json').read_text())
    if not cheque_nome['passed'] or not cheque_nome['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for caminho, 기대값 in cheque_nome['c_source_sha256'].items():
        if hash_Arquivo(ação_raiz/caminho) != 기대값: raise SystemExit('명명 검사 BACK_VALOR 바뀐 C códigoFonte: '+caminho)
    자바검사 = json.loads((validação_caminho/'jvm/report.json').read_text())
    직접화면 = json.loads((validação_caminho/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Português 직접 tela Executar_comando testes 필요')
    cheque_byte_VALOR = json.loads((validação_caminho/'naming/direct-bytecode.json').read_text())
    if not cheque_byte_VALOR['passed'] or cheque_byte_VALOR['jar_sha256'] != hash_Arquivo(ação_raiz/'dist/jkoros-native-korean.jar'):
        raise SystemExit('em_dia_item Português 라이브러리의 직접 호출 바이트코드 verificar 필요')
    cheque_resolução = json.loads((validação_caminho/'resolution/report.json').read_text())
    cheque_dimensionar = json.loads((validação_caminho/'resize/report.json').read_text())
    갱신검사 = json.loads((validação_caminho/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('em_dia_item 커널의 부분 renovar testes 필요')
    for caminho, 기대값 in 갱신검사['source_sha256'].items():
        if hash_Arquivo(ação_raiz/caminho) != 기대값: raise SystemExit('부분 renovar testes BACK_VALOR 바뀐 códigoFonte: '+caminho)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Português 직접 가닥과 iniciar ponto_de_entrada testes 필요')
    예제검사 = json.loads((validação_caminho/'examples/report.json').read_text())
    if sorted(cheque_dimensionar['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Tamanho 조절 testes 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Português Swing 창을 포함한 예제 13개 testes 필요')
    if sorted(cheque_resolução['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 real_dados tela testes 필요')
    if 자바검사['korean_library_sha256'] != hash_Arquivo(ação_raiz/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 testes BACK_VALOR 라이브러리가 바뀌었습니다.')
    for Nome in ('한국어통신시험','한국어예외시험'):
        if not any(entrada_VALOR_962f286b['name']==Nome and entrada_VALOR_962f286b.get('openjdk_output_equal') for entrada_VALOR_962f286b in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 testes 필요: '+Nome)
    exceção_Lista = sorted(caminho.stem for caminho in (ação_raiz/'한국어자바/Português/nativo').glob('*exceção.java'))
    exceção_LOG = (validação_caminho/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nome in exceção_Lista:
        if '\n'+Nome+'\n' not in exceção_LOG: raise SystemExit('exceção gerar·잡기·설명 testes 필요: '+Nome)
    especificação = json.loads((ação_raiz/'dist/manifest.json').read_text())
    if especificação['image_sha256'] != hash_Arquivo(ação_raiz/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distribuição_VALOR foto_VALOR hash_Arquivo 불일치')
    with zipfile.ZipFile(str(ação_raiz/'dist/jkoros-native-rpi4-boot.zip')) as grupo:
        if hashlib.sha256(grupo.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('arranque_da_máquina ZIP kernel_VALOR 불일치')
        부팅설정 = grupo.read('config.txt')
        for Nome, Tamanho in zip(('width', 'height'), especificação['framebuffer_resolution']):
            if 'framebuffer_'+Nome+'='+str(Tamanho) not in 부팅설정.decode().splitlines():
                raise SystemExit('arranque_da_máquina ZIP tela Definições 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(ação_raiz/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(ação_raiz/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_Arquivo(복사본) != kernel_hash: raise SystemExit('SD foto_VALOR kernel_VALOR 불일치')
        copiar_Configurações = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(ação_raiz/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copiar_Configurações)])
        if copiar_Configurações.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP tela Definições 불일치')
    LOG_linha = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': exceção_Lista, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(cheque_resolução['resolutions']),
            'sd_framebuffer_resolution': especificação['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nome:hash_Arquivo(ação_raiz/'dist'/Nome) for Nome in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validação_caminho/'native-runtime-summary.json').write_text(json.dumps(LOG_linha,ensure_ascii=False,indent=2)+'\n')
    print('PASS: em_dia_item 커널의',len(기록들),'개 통합 testes LOG_linha, Português exceção',len(exceção_Lista),'aula_Definição, SD foto_VALOR·ZIP 일치')

if __name__ == '__main__': iniciar()
