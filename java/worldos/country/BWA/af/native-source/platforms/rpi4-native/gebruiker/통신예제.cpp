#include "통신규약.h"
static 인터넷통신주소 adres(unsigned ombou_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.adres_Gesin = wolk_Gesin;
    VALUE.접속번호 = 망차례짧은수(ombou_VALUE); VALUE.internetadres.adres_VALUE = Netwerk_heelgetal(되돌림주소); return VALUE;
}
extern "C" int BEGIN_gebruiker_program(int) {
    int 보내는곳 = 통신종단점만들기(wolk_Gesin, 전문통신, 0);
    int 받는곳 = 통신종단점만들기(wolk_Gesin, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = adres(7777), 출발 = adres(7778), 보낸주소 = {};
    통신주소길이형 adres_lengte = sizeof(보낸주소);
    if (BIND_adres(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_adres(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 98) return 3;
    if (BIND_adres(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Inhoud_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Inhoud_VALUE, sizeof(Inhoud_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Inhoud_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Inhoud_VALUE, sizeof(Inhoud_VALUE), 0, 0, 0) != -1 || 오류번호 != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &adres_lengte) != sizeof(Inhoud_VALUE)) return 7;
    if (adres_lengte != sizeof(보낸주소) || 장치차례짧은수(보낸주소.접속번호) != 7778 || mobiel_volgorde_heelgetal(보낸주소.internetadres.adres_VALUE) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Inhoud_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Inhoud_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || 오류번호 != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Inhoud_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Inhoud_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || 오류번호 != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Inhoud_VALUE, sizeof(Inhoud_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Inhoud_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Inhoud_VALUE, sizeof(Inhoud_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Inhoud_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetadres.adres_VALUE = Netwerk_heelgetal(0x08080808);
    if (자료전문보내기(보내는곳, Inhoud_VALUE, sizeof(Inhoud_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || 오류번호 != 101) return 17;
    if (통신종단점만들기(wolk_Gesin, Stream_Netwerk, 전문전송규약) != -1 || 오류번호 != 93) return 18;
    adres_lengte = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &adres_lengte) || 장치차례짧은수(보낸주소.접속번호) != 7777) return 19;
    if (sluit_lêer(받는곳) || sluit_lêer(받는곳) != -1 || 오류번호 != 9) return 20;
    // 보내는곳은 열어 둔다: Verlaat_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    skryf_lêer_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
