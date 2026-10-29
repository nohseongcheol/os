from Indonesia import keluaranTeks, 전문통신열기, 바깥전문보내기, 전문받기, Tutup_jaringan, 밀리초
from Indonesia import sistem_kesalahan, 다시시도오류, 글부호화, 명령인수, bilangan_bulat
peserta = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP Indonesian")
    바깥전문보내기(peserta, "10.0.2.2", bilangan_bulat(명령인수[1]), 전문)
    jalankan = 밀리초()
    while True:
        try:
            balas, port_VALUE = 전문받기(peserta)
            break
        except sistem_kesalahan as galat:
            if galat.INDEX != 다시시도오류 or 밀리초() - jalankan >= 700:
                raise
    assert balas == 전문
    keluaranTeks("PYTHON 네트워크 periksa: UDP Indonesian")
finally:
    Tutup_jaringan(peserta)
