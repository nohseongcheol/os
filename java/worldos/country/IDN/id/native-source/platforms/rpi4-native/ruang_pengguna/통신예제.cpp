#include "통신규약.h"
static 인터넷통신주소 surel(unsigned port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.surel_famili = cloud_famili;
    VALUE.nomor_port = 망차례짧은수(port_VALUE); VALUE.Alamat_internet.surel_VALUE = jaringan_bilangan_bulat(alamat_loopback); return VALUE;
}
extern "C" int Mulai_pengguna_apl(int) {
    int 보내는곳 = Buat_peserta(cloud_famili, 전문통신, 0);
    int 받는곳 = Buat_peserta(cloud_famili, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = surel(7777), 출발 = surel(7778), 보낸주소 = {};
    통신주소길이형 surel_panjang = sizeof(보낸주소);
    if (ikat_surel(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (ikat_surel(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || nomor_kesalahan != 98) return 3;
    if (ikat_surel(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Isi_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Isi_VALUE, sizeof(Isi_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Isi_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Isi_VALUE, sizeof(Isi_VALUE), 0, 0, 0) != -1 || nomor_kesalahan != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &surel_panjang) != sizeof(Isi_VALUE)) return 7;
    if (surel_panjang != sizeof(보낸주소) || 장치차례짧은수(보낸주소.nomor_port) != 7778 || Ponsel_urutan_bilangan_bulat(보낸주소.Alamat_internet.surel_VALUE) != alamat_loopback) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Isi_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Isi_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || nomor_kesalahan != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Isi_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Isi_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || nomor_kesalahan != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Isi_VALUE, sizeof(Isi_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Isi_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Isi_VALUE, sizeof(Isi_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || nomor_kesalahan != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Isi_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Alamat_internet.surel_VALUE = jaringan_bilangan_bulat(0x08080808);
    if (자료전문보내기(보내는곳, Isi_VALUE, sizeof(Isi_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || nomor_kesalahan != 101) return 17;
    if (Buat_peserta(cloud_famili, Stream_jaringan, 전문전송규약) != -1 || nomor_kesalahan != 93) return 18;
    surel_panjang = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &surel_panjang) || 장치차례짧은수(보낸주소.nomor_port) != 7777) return 19;
    if (Tutup_file(받는곳) || Tutup_file(받는곳) != -1 || nomor_kesalahan != 9) return 20;
    // 보내는곳은 열어 둔다: Keluar_apl 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    tulis_file_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
