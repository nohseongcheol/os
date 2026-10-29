#include "통신규약.h"
static 인터넷통신주소 aterese(unsigned gorogisetsa_Boleng) {
    인터넷통신주소 Boleng = {}; Boleng.aterese_Lelapa = tlelaote_Lelapa;
    Boleng.접속번호 = 망차례짧은수(gorogisetsa_Boleng); Boleng.aterese_ya_Inthanete.aterese_Boleng = Neteweke_Palotlalo(되돌림주소); return Boleng;
}
extern "C" int simolola_modirisi_Tiriso(int) {
    int 보내는곳 = 통신종단점만들기(tlelaote_Lelapa, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(tlelaote_Lelapa, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = aterese(7777), 출발 = aterese(7778), 보낸주소 = {};
    통신주소길이형 aterese_boleele = sizeof(보낸주소);
    if (BIND_aterese(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_aterese(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_aterese(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Diteng_Boleng[] = "한글 UDP loopback 😀";
    char 받은값[64] = {};
    if (자료전문보내기(보내는곳, Diteng_Boleng, sizeof(Diteng_Boleng), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Diteng_Boleng)) return 5;
    if (자료전문받기(받는곳, (void *)Diteng_Boleng, sizeof(Diteng_Boleng), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, (통신주소 *)&보낸주소, &aterese_boleele) != sizeof(Diteng_Boleng)) return 7;
    if (aterese_boleele != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || mobaele_thulaganyo_Palotlalo(보낸주소.aterese_ya_Inthanete.aterese_Boleng) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Diteng_Boleng); 순번++) if (받은값[순번] != Diteng_Boleng[순번]) return 9;
    if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, 받은값, sizeof(Diteng_Boleng), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Diteng_Boleng)) return 11;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, 받은값, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Diteng_Boleng, sizeof(Diteng_Boleng), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Diteng_Boleng)) return 14;
    if (자료전문보내기(보내는곳, Diteng_Boleng, sizeof(Diteng_Boleng), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, 받은값, sizeof(받은값), 0, 0, 0) != sizeof(Diteng_Boleng)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.aterese_ya_Inthanete.aterese_Boleng = Neteweke_Palotlalo(0x08080808);
    if (자료전문보내기(보내는곳, Diteng_Boleng, sizeof(Diteng_Boleng), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(tlelaote_Lelapa, moela_Neteweke, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    aterese_boleele = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &aterese_boleele) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (tswala_faele(받는곳) || tswala_faele(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: tswaya_Tiriso 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    kwala_faele_tshedimosetso(1, 완료, sizeof(완료) - 1);
    return 0;
}
