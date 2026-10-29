#include "통신규약.h"
static 인터넷통신주소 ADDRESS(unsigned port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.ADDRESS_Familie = sky_Familie;
    VALUE.portnummer = 망차례짧은수(port_VALUE); VALUE.Internett_adresse.ADDRESS_VALUE = Nettverk_heiltal(되돌림주소); return VALUE;
}
extern "C" int START_brukar_app(int) {
    int 보내는곳 = Opprett_endepunkt(sky_Familie, 전문통신, 0);
    int 받는곳 = Opprett_endepunkt(sky_Familie, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ADDRESS(7777), 출발 = ADDRESS(7778), 보낸주소 = {};
    통신주소길이형 ADDRESS_lengd = sizeof(보낸주소);
    if (BIND_ADDRESS(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || feilnummer != 98) return 3;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Innhald_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Innhald_VALUE, sizeof(Innhald_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Innhald_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Innhald_VALUE, sizeof(Innhald_VALUE), 0, 0, 0) != -1 || feilnummer != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &ADDRESS_lengd) != sizeof(Innhald_VALUE)) return 7;
    if (ADDRESS_lengd != sizeof(보낸주소) || 장치차례짧은수(보낸주소.portnummer) != 7778 || mobil_rekkjefølgje_heiltal(보낸주소.Internett_adresse.ADDRESS_VALUE) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Innhald_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Innhald_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || feilnummer != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Innhald_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Innhald_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || feilnummer != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Innhald_VALUE, sizeof(Innhald_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Innhald_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Innhald_VALUE, sizeof(Innhald_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || feilnummer != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Innhald_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internett_adresse.ADDRESS_VALUE = Nettverk_heiltal(0x08080808);
    if (자료전문보내기(보내는곳, Innhald_VALUE, sizeof(Innhald_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || feilnummer != 101) return 17;
    if (Opprett_endepunkt(sky_Familie, Stream_Nettverk, 전문전송규약) != -1 || feilnummer != 93) return 18;
    ADDRESS_lengd = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ADDRESS_lengd) || 장치차례짧은수(보낸주소.portnummer) != 7777) return 19;
    if (Lukk_fil(받는곳) || Lukk_fil(받는곳) != -1 || feilnummer != 9) return 20;
    // 보내는곳은 열어 둔다: Utgang_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    skrive_fil_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
