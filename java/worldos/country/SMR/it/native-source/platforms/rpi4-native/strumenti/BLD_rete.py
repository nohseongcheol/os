from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def Crea_rete(radice_percorso, C_compilatore, Archivio_strumento, configurazione_BITS, Esegui_comando):
    원본자료 = radice_percorso / 'vendor/lwip/src'
    numero_di_porta = radice_percorso / 'rete_Pila'
    output = radice_percorso / 'build/network'
    output.mkdir(exist_ok=True)
    write_header(radice_percorso, output / 'ip_config.h')
    elenco_file = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    elenco_file += [원본자료 / 'netif/ethernet.c']
    elenco_file += sorted(numero_di_porta.glob('*.c'))
    meta_File = []
    for percorso in elenco_file:
        file_di_destinazione = output / (percorso.stem + '.o')
        Esegui_comando([C_compilatore] + configurazione_BITS + ['-include', output / 'ip_config.h', '-std=c11', '-I', numero_di_porta, '-I', 원본자료 / 'include',
             '-I', radice_percorso.parents[1] / 'posix-kor/arm64-native/dichiarazioni', '-c', percorso, '-o', file_di_destinazione])
        meta_File.append(file_di_destinazione)
    Catalogo = output / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(output)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        Esegui_comando([Archivio_strumento, 'rcs', 새라이브러리] + meta_File)
        새라이브러리.replace(Catalogo)
    return Catalogo
