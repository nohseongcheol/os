#!/usr/bin/env python3
"""PyPI HTTPS·압축을 맡는 localhost relé_VALOR. 게스트는 TCP로 받은 소스를 직접 instalar_VALOR·실행한다."""
import argparse
import email.parser
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import socketserver
import struct
import tarfile
import threading
import urllib.request
import zipfile

ação_raiz = Path(__file__).resolve().parents[1]


def analisar_solicitação(solicitação):
    맞음 = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9._-]{0,63})(?:==([A-Za-z0-9][A-Za-z0-9._-]{0,23}))?', solicitação)
    if not 맞음:
        raise ValueError('grupo Nome 또는 Nome==버전을 지정하십시오.')
    return re.sub(r'[-_.]+', '-', 맞음[1]).lower(), 맞음[2]


def validar_caminho(Nome, instalação_caminho=True):
    caminho = PurePosixPath(Nome)
    if caminho.is_absolute() or any(부분 in ('', '.', '..') or 부분.startswith('.') for 부분 in Nome.split('/')):
        raise ValueError('허용하지 않는 grupo caminho: ' + Nome)
    if '\\' in Nome or any(ord(caractere_VALOR) < 32 or ord(caractere_VALOR) == 127 for caractere_VALOR in Nome):
        raise ValueError('잘못된 grupo caminho 문자')
    if instalação_caminho and (len(('/lib/' + Nome).encode()) > 63 or Nome in ('Português.py', 'grupo.py')):
        raise ValueError('grupo caminho 제한 또는 valor_padrão biblioteca 충돌: ' + Nome)
    return Nome


def descompactar(Arquivo_entrada_nome, dados, Nome, versão_VALOR):
    파일들 = {}
    명세들 = []
    def Acrescentar_entrada(caminho, Conteúdo_VALOR):
        validar_caminho(caminho)
        if caminho in 파일들:
            raise ValueError('중복 grupo caminho: ' + caminho)
        if len(Conteúdo_VALOR) > 16384:
            raise ValueError('파일당 16 KiB 제한 초과: ' + caminho)
        Conteúdo_VALOR.decode('utf-8')
        파일들[caminho] = Conteúdo_VALOR
        if len(파일들) > 16 or sum(map(len, 파일들.values())) > 65536:
            raise ValueError('꾸러미는 fonte_árvore 16개·total_VALOR 64 KiB 이하여야 합니다.')
    if Arquivo_entrada_nome.endswith('.whl'):
        with zipfile.ZipFile(io.BytesIO(dados)) as grupo:
            항목들 = grupo.infolist()
            if len(항목들) > 256 or sum(entrada_VALOR_962f286b.file_size for entrada_VALOR_962f286b in 항목들) > 1048576:
                raise ValueError('arquivo_VALOR lançar_Armazenamento Tamanho 제한 초과')
            contrato_Lista = [entrada_VALOR_962f286b for entrada_VALOR_962f286b in 항목들 if entrada_VALOR_962f286b.filename.endswith('.dist-info/WHEEL')]
            if len(contrato_Lista) != 1:
                raise ValueError('wheel valor_do_contrato 명세가 필요합니다.')
            valor_do_contrato = email.parser.Parser().parsestr(grupo.read(contrato_Lista[0]).decode())
            if valor_do_contrato.get('Root-Is-Purelib', '').lower() != 'true' or not Arquivo_entrada_nome.endswith('-none-any.whl'):
                raise ValueError('C extensão_VALOR·플랫폼 전용 wheel은 지원하지 않습니다.')
            for entrada_VALOR_962f286b in 항목들:
                caminho = entrada_VALOR_962f286b.filename.rstrip('/')
                validar_caminho(caminho, False)
                if (entrada_VALOR_962f286b.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError('심볼릭 링크는 설치할 número 없습니다.')
                if entrada_VALOR_962f286b.filename.endswith('/'):
                    continue
                if '.dist-info/' in caminho:
                    if caminho.endswith('/METADATA'):
                        명세들.append(grupo.read(entrada_VALOR_962f286b).decode())
                    continue
                if not caminho.endswith('.py') or '.data/' in caminho:
                    raise ValueError('현재는 .py 소스만 지원합니다: ' + caminho)
                Acrescentar_entrada(caminho, grupo.read(entrada_VALOR_962f286b))
    elif Arquivo_entrada_nome.endswith('.tar.gz') and Nome.startswith('micropython-'):
        # 구형 micropython-lib의 upip 배포형: setup.py Executar_comando 없이 .py와 PKG-INFO만 읽는다.
        with tarfile.open(fileobj=io.BytesIO(dados), mode='r|gz') as grupo:
            뿌리들 = set()
            entrada_CONT_NÚM_8f7753a1 = 0
            total_dimensionar = 0
            for entrada_VALOR_962f286b in grupo:
                entrada_CONT_NÚM_8f7753a1 += 1
                total_dimensionar += entrada_VALOR_962f286b.size
                if entrada_CONT_NÚM_8f7753a1 > 256 or total_dimensionar > 1048576:
                    raise ValueError('arquivo_VALOR lançar_Armazenamento Tamanho 제한 초과')
                validar_caminho(entrada_VALOR_962f286b.name, False)
                부분들 = entrada_VALOR_962f286b.name.split('/')
                뿌리들.add(부분들[0])
                if entrada_VALOR_962f286b.isdir():
                    continue
                if not entrada_VALOR_962f286b.isfile() or len(부분들) < 2:
                    raise ValueError('잘못된 MicroPython fonte_árvore 배포형')
                caminho = '/'.join(부분들[1:])
                Conteúdo_VALOR = grupo.extractfile(entrada_VALOR_962f286b).read()
                if caminho.endswith('PKG-INFO'):
                    명세들.append(Conteúdo_VALOR.decode())
                elif caminho.endswith('.py') and caminho not in ('setup.py',):
                    Acrescentar_entrada(caminho, Conteúdo_VALOR)
                elif '.egg-info/' not in caminho and not caminho.upper().startswith(('LICENSE', 'COPYING', 'README')):
                    raise ValueError('일반 sdist 빌드는 지원하지 않습니다: ' + caminho)
            if len(뿌리들) != 1:
                raise ValueError('MicroPython 소스의 raiz_VALOR 폴더가 하나여야 합니다.')
    else:
        raise ValueError('순수 Python wheel 또는 micropython-* fonte_árvore 배포형이 필요합니다.')
    if not 파일들 or len(명세들) != 1:
        raise ValueError('소스와 distribuição_VALOR 메타데이터가 필요합니다.')
    especificação = email.parser.Parser().parsestr(명세들[0])
    if analisar_solicitação(especificação.get('Name', ''))[0] != Nome or especificação.get('Version') != versão_VALOR:
        raise ValueError('distribuição_VALOR 메타데이터의 Nome·버전 불일치')
    if especificação.get_all('Requires-Dist') or especificação.get_all('Requires'):
        raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다. 의존성 없는 호환 꾸러미를 사용하십시오.')
    return 파일들


def leitura_W3(Endereço, 한도):
    if not Endereço.startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
        raise ValueError('PyPI HTTPS distribuição_VALOR 주소만 허용합니다.')
    with urllib.request.urlopen(Endereço, timeout=30) as resposta:
        if not resposta.geturl().startswith(('https://pypi.org/', 'https://files.pythonhosted.org/')):
            raise ValueError('예상하지 않은 distribuição_VALOR Endereço mover_VALOR')
        dados = resposta.read(한도 + 1)
    if len(dados) > 한도:
        raise ValueError('distribuição_VALOR ficheiro Tamanho 제한 초과')
    return dados


def Transferir_grupo(Nome, versão_VALOR, 파일들, origem_VALOR):
    especificação = {'name': Nome, 'version': versão_VALOR, 'source': origem_VALOR, 'files': [
        {'path': caminho, 'size': len(dados), 'sha256': hashlib.sha256(dados).hexdigest()}
        for caminho, dados in sorted(파일들.items())]}
    HEAD_VALOR = json.dumps(especificação, ensure_ascii=False).encode()
    if len(HEAD_VALOR) > 8192:
        raise ValueError('grupo especificação Tamanho 초과')
    return b'JKP1' + struct.pack('>I', len(HEAD_VALOR)) + HEAD_VALOR + b''.join(파일들[entrada_VALOR_962f286b['path']] for entrada_VALOR_962f286b in especificação['files'])


class grupo_repositório:
    def __init__(자신, caminho, TI_Offline=False):
        자신.caminho = Path(caminho)
        자신.caminho.mkdir(parents=True, exist_ok=True)
        자신.TI_Offline = TI_Offline

    def Preparar(자신, solicitação):
        Nome, versão_VALOR = analisar_solicitação(solicitação)
        Chave_material = Nome + ('==' + versão_VALOR if versão_VALOR else '')
        LOG_caminho = 자신.caminho / (Chave_material + '.json')
        distribuição_caminho = 자신.caminho / (Chave_material + '.archive')
        if LOG_caminho.is_file() and distribuição_caminho.is_file():
            LOG_linha = json.loads(LOG_caminho.read_text())
            dados = distribuição_caminho.read_bytes()
            if hashlib.sha256(dados).hexdigest() != LOG_linha['sha256']:
                raise ValueError('저장된 distribuição_VALOR 파일의 SHA-256 불일치')
        else:
            if 자신.TI_Offline:
                raise ValueError('TI_Offline 저장소에 없는 grupo: ' + solicitação)
            Endereço = 'https://pypi.org/pypi/' + Nome + ('/' + versão_VALOR if versão_VALOR else '') + '/json'
            msinfo32_exe = json.loads(leitura_W3(Endereço, 4194304).decode())
            if msinfo32_exe['info'].get('requires_dist'):
                raise ValueError('자동 의존성 해결은 아직 지원하지 않습니다.')
            candidato = [entrada_VALOR_962f286b for entrada_VALOR_962f286b in msinfo32_exe['urls'] if not entrada_VALOR_962f286b.get('yanked') and entrada_VALOR_962f286b['filename'].endswith('-none-any.whl')]
            if not candidato and Nome.startswith('micropython-'):
                candidato = [entrada_VALOR_962f286b for entrada_VALOR_962f286b in msinfo32_exe['urls'] if not entrada_VALOR_962f286b.get('yanked') and entrada_VALOR_962f286b['filename'].endswith('.tar.gz')]
            if not candidato:
                raise ValueError('지원되는 순수 Python distribuição_VALOR 파일이 없습니다.')
            seleção_VALOR = candidato[0]
            dados = leitura_W3(seleção_VALOR['url'], 4194304)
            if hashlib.sha256(dados).hexdigest() != seleção_VALOR['digests']['sha256']:
                raise ValueError('PyPI distribuição_VALOR ficheiro SHA-256 불일치')
            LOG_linha = {'name': Nome, 'version': msinfo32_exe['info']['version'], 'filename': seleção_VALOR['filename'],
                    'url': seleção_VALOR['url'], 'sha256': seleção_VALOR['digests']['sha256']}
            # 검사가 끝나기 전에는 저장하지 않는다.
            descompactar(LOG_linha['filename'], dados, Nome, LOG_linha['version'])
            distribuição_caminho.write_bytes(dados)
            LOG_caminho.write_text(json.dumps(LOG_linha, ensure_ascii=False, indent=2) + '\n')
        if LOG_linha['name'] != Nome or versão_VALOR and LOG_linha['version'] != versão_VALOR:
            raise ValueError('repositório_raiz Nome·버전 불일치')
        파일들 = descompactar(LOG_linha['filename'], dados, Nome, LOG_linha['version'])
        return Transferir_grupo(Nome, LOG_linha['version'], 파일들, LOG_linha['url'])


class grupo_solicitação(socketserver.BaseRequestHandler):
    def handle(자신):
        자신.request.settimeout(10)
        try:
            solicitação = bytearray()
            while b'\n' not in solicitação and len(solicitação) < 100:
                fragmento_VALOR = 자신.request.recv(100 - len(solicitação))
                if not fragmento_VALOR:
                    return
                solicitação.extend(fragmento_VALOR)
            if not solicitação.endswith(b'\n') or solicitação.count(b'\n') != 1:
                raise ValueError('잘못된 grupo solicitação')
            resposta = 자신.server.repositório_raiz.Preparar(solicitação[:-1].decode('ascii'))
        except Exception as erro:
            HEAD_VALOR = json.dumps({'error': str(erro)[:500]}, ensure_ascii=False).encode()
            resposta = b'JKP1' + struct.pack('>I', len(HEAD_VALOR)) + HEAD_VALOR
        try:
            자신.request.sendall(resposta)
        except OSError:
            pass


class grupo_relé:
    def __init__(자신, número_da_porta=8027, caminho=None, TI_Offline=False):
        자신.servidor_VALOR = socketserver.TCPServer(('127.0.0.1', número_da_porta), grupo_solicitação, bind_and_activate=False)
        자신.servidor_VALOR.allow_reuse_address = True
        자신.servidor_VALOR.server_bind()
        자신.servidor_VALOR.server_activate()
        자신.servidor_VALOR.repositório_raiz = grupo_repositório(caminho or ação_raiz/'build/pip-cache', TI_Offline)
        자신.número_da_porta = 자신.servidor_VALOR.server_address[1]
        자신.thread_VALOR = threading.Thread(target=자신.servidor_VALOR.serve_forever, kwargs={'poll_interval': .1}, daemon=True)

    def __enter__(자신):
        자신.thread_VALOR.start()
        return 자신

    def __exit__(자신, *argumentos):
        자신.servidor_VALOR.shutdown()
        자신.servidor_VALOR.server_close()
        자신.thread_VALOR.join(timeout=2)


def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--port', type=int, default=8027)
    analisador_48ee4b1b.add_argument('--cache', type=Path, default=ação_raiz/'build/pip-cache')
    analisador_48ee4b1b.add_argument('--offline', action='store_true')
    analisador_48ee4b1b.add_argument('--fetch', help='Executar_comando 없이 호환 distribuição_VALOR 파일을 내려받아 검사·Store_VALOR')
    argumentos = analisador_48ee4b1b.parse_args()
    if argumentos.fetch:
        dados = grupo_repositório(argumentos.cache, argumentos.offline).Preparar(argumentos.fetch)
        print('grupo Preparar 완료:', argumentos.fetch, len(dados), 'byte_VALOR')
        return
    with grupo_relé(argumentos.port, argumentos.cache, argumentos.offline) as relé_VALOR:
        print('grupo relé_VALOR: 127.0.0.1:' + str(relé_VALOR.número_da_porta), flush=True)
        try:
            relé_VALOR.thread_VALOR.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    iniciar()
