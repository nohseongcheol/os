from Melayu import 출력, 전문통신열기, 바깥전문보내기, 전문받기, Tutup_rangkaian, 밀리초
from Melayu import sistem_ralat, 다시시도오류, 글부호화, 명령인수, integer
peserta = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP ms")
    바깥전문보내기(peserta, "10.0.2.2", integer(명령인수[1]), 전문)
    Jalan = 밀리초()
    while True:
        try:
            balas, port_VALUE = 전문받기(peserta)
            break
        except sistem_ralat as RALAT:
            if RALAT.INDEX != 다시시도오류 or 밀리초() - Jalan >= 700:
                raise
    assert balas == 전문
    출력("PYTHON 네트워크 tentu_sahkan: UDP ms")
finally:
    Tutup_rangkaian(peserta)
