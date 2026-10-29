#include "통신규약.h"
static 인터넷통신주소 e_mel(unsigned port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.e_mel_Keluarga = awan_Keluarga;
    VALUE.nombor_port = 망차례짧은수(port_VALUE); VALUE.alamat_Internet.e_mel_VALUE = rangkaian_integer(되돌림주소); return VALUE;
}
extern "C" int Mula_pengguna_aplikasi(int) {
    int 보내는곳 = cipta_peserta(awan_Keluarga, 전문통신, 0);
    int 받는곳 = cipta_peserta(awan_Keluarga, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = e_mel(7777), 출발 = e_mel(7778), 보낸주소 = {};
    통신주소길이형 e_mel_kepanjangan = sizeof(보낸주소);
    if (ikat_e_mel(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (ikat_e_mel(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (ikat_e_mel(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Kandungan_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Kandungan_VALUE, sizeof(Kandungan_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Kandungan_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Kandungan_VALUE, sizeof(Kandungan_VALUE), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &e_mel_kepanjangan) != sizeof(Kandungan_VALUE)) return 7;
    if (e_mel_kepanjangan != sizeof(보낸주소) || 장치차례짧은수(보낸주소.nombor_port) != 7778 || peranti_tertib_integer(보낸주소.alamat_Internet.e_mel_VALUE) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Kandungan_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Kandungan_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Kandungan_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Kandungan_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Kandungan_VALUE, sizeof(Kandungan_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Kandungan_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Kandungan_VALUE, sizeof(Kandungan_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Kandungan_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.alamat_Internet.e_mel_VALUE = rangkaian_integer(0x08080808);
    if (자료전문보내기(보내는곳, Kandungan_VALUE, sizeof(Kandungan_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (cipta_peserta(awan_Keluarga, strim_rangkaian, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    e_mel_kepanjangan = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &e_mel_kepanjangan) || 장치차례짧은수(보낸주소.nombor_port) != 7777) return 19;
    if (Tutup_fail(받는곳) || Tutup_fail(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Keluar_aplikasi 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    tulis_fail_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
