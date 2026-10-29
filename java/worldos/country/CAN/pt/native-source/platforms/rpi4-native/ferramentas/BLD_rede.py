from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def Criar_rede(raiz_caminho, C_compilador, arquivo_ferramenta, Configuração_BITS, Executar_comando):
    원본자료 = raiz_caminho / 'vendor/lwip/src'
    número_da_porta = raiz_caminho / 'rede_pilha'
    saída = raiz_caminho / 'build/network'
    saída.mkdir(exist_ok=True)
    write_header(raiz_caminho, saída / 'ip_config.h')
    lista_de_arquivos = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    lista_de_arquivos += [원본자료 / 'netif/ethernet.c']
    lista_de_arquivos += sorted(número_da_porta.glob('*.c'))
    destino_Arquivos = []
    for caminho in lista_de_arquivos:
        arquivo_de_destino = saída / (caminho.stem + '.o')
        Executar_comando([C_compilador] + Configuração_BITS + ['-include', saída / 'ip_config.h', '-std=c11', '-I', número_da_porta, '-I', 원본자료 / 'include',
             '-I', raiz_caminho.parents[1] / 'posix-kor/arm64-native/declarações', '-c', caminho, '-o', arquivo_de_destino])
        destino_Arquivos.append(arquivo_de_destino)
    biblioteca = saída / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(saída)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        Executar_comando([arquivo_ferramenta, 'rcs', 새라이브러리] + destino_Arquivos)
        새라이브러리.replace(biblioteca)
    return biblioteca
