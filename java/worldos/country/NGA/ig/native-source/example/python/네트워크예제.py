from 한국어 import 출력, 전문통신열기, 바깥전문보내기, 전문받기, mmechi_Netwọọkụ, 밀리초
from 한국어 import sistèm_mmejọ, 다시시도오류, 글부호화, 명령인수, ọnụọgụ_nzùrùòkè
종단 = 전문통신열기(0)
try:
    전문 = 글부호화("PYTHON UDP ig")
    바깥전문보내기(종단, "10.0.2.2", ọnụọgụ_nzùrùòkè(명령인수[1]), 전문)
    Bido = 밀리초()
    while True:
        try:
            nzaghachi, pọọt_valuu = 전문받기(종단)
            break
        except sistèm_mmejọ as mmejọ:
            if mmejọ.indèks != 다시시도오류 or 밀리초() - Bido >= 700:
                raise
    assert nzaghachi == 전문
    출력("PYTHON 네트워크 nkwàdo_eziokwū: UDP ig")
finally:
    mmechi_Netwọọkụ(종단)
