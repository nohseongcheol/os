from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def ສ້າງ_ເຄືອຂ່າຍ_48d29d6d(ເລກຮາກ_ທາງໂຄຈອນ, 시언어번역기, ການສໍາເນົາ_ເຄື່ອງມື, ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ, ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ):
    원본자료 = ເລກຮາກ_ທາງໂຄຈອນ / 'vendor/lwip/src'
    ຫມາຍເລກພອດ = ເລກຮາກ_ທາງໂຄຈອນ / 'ເຄືອຂ່າຍ_ກຸ່ມບັດ'
    출력결과 = ເລກຮາກ_ທາງໂຄຈອນ / 'build/network'
    출력결과.mkdir(exist_ok=True)
    write_header(ເລກຮາກ_ທາງໂຄຈອນ, 출력결과 / 'ip_config.h')
    ຟາຍ_ລາຍຊື່ = sorted((원본자료 / 'core').glob('*.c')) + sorted((원본자료 / 'core/ipv4').glob('*.c'))
    ຟາຍ_ລາຍຊື່ += [원본자료 / 'netif/ethernet.c']
    ຟາຍ_ລາຍຊື່ += sorted(ຫມາຍເລກພອດ.glob('*.c'))
    ປາຍທາງ_ໄຟລ໌ = []
    for ທາງໂຄຈອນ in ຟາຍ_ລາຍຊື່:
        ຟາຍປາຍທາງ = 출력결과 / (ທາງໂຄຈອນ.stem + '.o')
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([시언어번역기] + ການຕັ້ງຄ່າເຊື່ອມຕໍ່_ບໍລິການໂອນຍ້າຍອັດສະລິຍະໃນພື້ນຫຼັງ + ['-include', 출력결과 / 'ip_config.h', '-std=c11', '-I', ຫມາຍເລກພອດ, '-I', 원본자료 / 'include',
             '-I', ເລກຮາກ_ທາງໂຄຈອນ.parents[1] / 'posix-kor/arm64-native/포함', '-c', ທາງໂຄຈອນ, '-o', ຟາຍປາຍທາງ])
        ປາຍທາງ_ໄຟລ໌.append(ຟາຍປາຍທາງ)
    ຫໍສະຫມຸດ = 출력결과 / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(출력결과)) as 임시경로:
        새라이브러리=Path(임시경로)/'libnetwork.a'
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ([ການສໍາເນົາ_ເຄື່ອງມື, 'rcs', 새라이브러리] + ປາຍທາງ_ໄຟລ໌)
        새라이브러리.replace(ຫໍສະຫມຸດ)
    return ຫໍສະຫມຸດ
