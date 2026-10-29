from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def tạoMạng(đườngDẫnGốcCây, TrìnhBiênDịchC, côngCụKhoLưuTrữ, cácBitCấuHình, thựcThiLệnh):
    dữLiệuNguyênBản = đườngDẫnGốcCây / 'vendor/lwip/src'
    sốCổng = đườngDẫnGốcCây / 'NgănXếpMạng'
    đầuRa = đườngDẫnGốcCây / 'build/network'
    đầuRa.mkdir(exist_ok=True)
    write_header(đườngDẫnGốcCây, đầuRa / 'ip_config.h')
    danhSáchTệp = sorted((dữLiệuNguyênBản / 'core').glob('*.c')) + sorted((dữLiệuNguyênBản / 'core/ipv4').glob('*.c'))
    danhSáchTệp += [dữLiệuNguyênBản / 'netif/ethernet.c']
    danhSáchTệp += sorted(sốCổng.glob('*.c'))
    cácTệpĐích = []
    for đườngDẫn in danhSáchTệp:
        tệpĐích = đầuRa / (đườngDẫn.stem + '.o')
        thựcThiLệnh([TrìnhBiênDịchC] + cácBitCấuHình + ['-include', đầuRa / 'ip_config.h', '-std=c11', '-I', sốCổng, '-I', dữLiệuNguyênBản / 'include',
             '-I', đườngDẫnGốcCây.parents[1] / 'posix-kor/arm64-native/TệpĐầuMục', '-c', đườngDẫn, '-o', tệpĐích])
        cácTệpĐích.append(tệpĐích)
    thưViện = đầuRa / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(đầuRa)) as đườngDẫnTạm:
        thưViệnMới=Path(đườngDẫnTạm)/'libnetwork.a'
        thựcThiLệnh([côngCụKhoLưuTrữ, 'rcs', thưViệnMới] + cácTệpĐích)
        thưViệnMới.replace(thưViện)
    return thưViện
