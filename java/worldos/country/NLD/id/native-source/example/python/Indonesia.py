"""Asli 커널의 berkas·komunikasi·화면 호출과 Indonesia pengecualian. 표준 이름은 이 연결부에서만 쓴다."""
import jkoros as sistem_operasi
import sys as runtime_bahasa_umum

def keluaranTeks(*VALUE, pemisah=" ", 끝="\n", **기존인수):
    # 기존 print의 sep/end 인수도 연결부에서 호환한다.
    if "sep" not in 기존인수: 기존인수["sep"] = pemisah
    if "end" not in 기존인수: 기존인수["end"] = 끝
    print(*VALUE, **기존인수)

bilangan_bulat = int
명령인수 = runtime_bahasa_umum.argv
다시시도오류 = 11

class sistem_kesalahan(OSError):
    def __init__(자신, INDEX, 설명="sistem_operasi 작업에 실패했습니다."):
        super().__init__(INDEX, 설명)
        자신.INDEX = INDEX
        자신.설명 = 설명

def 운영호출(fungsi_VALUE, *argumen):
    try:
        return fungsi_VALUE(*argumen)
    except OSError as galat:
        INDEX = galat.args[0] if galat.args else 0
        raise sistem_kesalahan(INDEX)

def 글부호화(teks):
    return teks.encode("utf-8")

def 글해독(data):
    return data.decode("utf-8")

def 파일읽기(Nama_2):
    return 운영호출(sistem_operasi.read, Nama_2)

def tulis_file(Nama_2, data):
    return 운영호출(sistem_operasi.write, Nama_2, data)

def hapus_file(Nama_2):
    return 운영호출(sistem_operasi.remove, Nama_2)

def 전문통신열기(nomor_port):
    return 운영호출(sistem_operasi.udp_open, nomor_port)

def 전문보내기(peserta, nomor_port, data):
    return 운영호출(sistem_operasi.udp_send, peserta, nomor_port, data)

def 바깥전문보내기(peserta, surel, nomor_port, data):
    return 운영호출(sistem_operasi.udp_sendto, peserta, surel, nomor_port, data)

def 전문받기(peserta):
    return 운영호출(sistem_operasi.udp_recv, peserta)

def Tutup_jaringan(peserta):
    return 운영호출(sistem_operasi.udp_close, peserta)

def Gambar_persegi(*argumen):
    return 운영호출(sistem_operasi.rect, *argumen)

def 화면크기():
    return 운영호출(sistem_operasi.screen_size)

def 그림기다리기():
    return 운영호출(sistem_operasi.wait_key)

밀리초 = sistem_operasi.ticks_ms
