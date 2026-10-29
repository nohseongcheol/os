#include "통신규약.h"
static 인터넷통신주소 salgy(unsigned port_baha) {
    인터넷통신주소 baha = {}; baha.salgy_Maşgala = bulut_Maşgala;
    baha.접속번호 = 망차례짧은수(port_baha); baha.Internet_salgy.salgy_baha = Tor_bitin(되돌림주소); return baha;
}
extern "C" int başlat_ulanyjy_programma(int) {
    int 보내는곳 = 통신종단점만들기(bulut_Maşgala, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(bulut_Maşgala, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = salgy(7777), 출발 = salgy(7778), 보낸주소 = {};
    통신주소길이형 salgy_dowamlylyk = sizeof(보낸주소);
    if (BIND_salgy(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_salgy(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_salgy(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Mazmun_baha[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Mazmun_baha, sizeof(Mazmun_baha), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Mazmun_baha)) return 5;
    if (자료전문받기(받는곳, (void *)Mazmun_baha, sizeof(Mazmun_baha), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &salgy_dowamlylyk) != sizeof(Mazmun_baha)) return 7;
    if (salgy_dowamlylyk != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || enjam_tertip_bitin(보낸주소.Internet_salgy.salgy_baha) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Mazmun_baha); 순번++) if (받은값[순번] != Mazmun_baha[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Mazmun_baha), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Mazmun_baha)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Mazmun_baha, sizeof(Mazmun_baha), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Mazmun_baha)) return 14;
    if (자료전문보내기(보내는곳, Mazmun_baha, sizeof(Mazmun_baha), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Mazmun_baha)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internet_salgy.salgy_baha = Tor_bitin(0x08080808);
    if (자료전문보내기(보내는곳, Mazmun_baha, sizeof(Mazmun_baha), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(bulut_Maşgala, Stream_Tor, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    salgy_dowamlylyk = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &salgy_dowamlylyk) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (ýap_faýl(받는곳) || ýap_faýl(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: çyk_programma 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    ýaz_faýl_maglumat(1, 완료, sizeof(완료) - 1);
    return 0;
}
