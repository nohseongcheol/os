"""Asli 커널의 Fail·통신·화면 호출과 Melayu pengecualian. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistem_pengendalian
import sys as masa_jalan_bahasa_biasa

def 출력(*VALUE, pemisah=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = pemisah
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

integer = int
명령인수 = masa_jalan_bahasa_biasa.argv
다시시도오류 = 11

class sistem_ralat(OSError):
    def __init__(자신, INDEX, 설명="sistem_pengendalian 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(fungsi_VALUE, *인수):
    try:
        return fungsi_VALUE(*인수)
    except OSError as RALAT:
        INDEX = RALAT.args[0] if RALAT.args else 0
        raise sistem_ralat(INDEX)

def 글부호화(Teks):
    return Teks.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Nama):
    return 운영호출(sistem_pengendalian.read, Nama)

def tulis_fail(Nama, data):
    return 운영호출(sistem_pengendalian.write, Nama, data)

def alih_keluar_fail(Nama):
    return 운영호출(sistem_pengendalian.remove, Nama)

def 전문통신열기(nombor_port):
    return 운영호출(sistem_pengendalian.udp_open, nombor_port)

def 전문보내기(peserta, nombor_port, data):
    return 운영호출(sistem_pengendalian.udp_send, peserta, nombor_port, data)

def 바깥전문보내기(peserta, e_mel, nombor_port, data):
    return 운영호출(sistem_pengendalian.udp_sendto, peserta, e_mel, nombor_port, data)

def 전문받기(peserta):
    return 운영호출(sistem_pengendalian.udp_recv, peserta)

def Tutup_rangkaian(peserta):
    return 운영호출(sistem_pengendalian.udp_close, peserta)

def Lukis_segi_empat_tepat(*인수):
    return 운영호출(sistem_pengendalian.rect, *인수)

def 화면크기():
    return 운영호출(sistem_pengendalian.screen_size)

def 그림기다리기():
    return 운영호출(sistem_pengendalian.wait_key)

밀리초 = sistem_pengendalian.ticks_ms
