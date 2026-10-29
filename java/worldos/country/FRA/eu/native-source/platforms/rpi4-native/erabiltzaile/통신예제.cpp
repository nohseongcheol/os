#include "통신규약.h"
static 인터넷통신주소 helbide(unsigned ataka_balio) {
    인터넷통신주소 balio = {}; balio.helbide_sorta = hodei_sorta;
    balio.ataka_zenbaki = 망차례짧은수(ataka_balio); balio.Internet_helbide.helbide_balio = sare_osoko_zenbaki(되돌림주소); return balio;
}
extern "C" int HASI_erabiltzaile_aplik(int) {
    int 보내는곳 = sortu_amaiera_puntu(hodei_sorta, 전문통신, 0);
    int 받는곳 = sortu_amaiera_puntu(hodei_sorta, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = helbide(7777), 출발 = helbide(7778), 보낸주소 = {};
    통신주소길이형 helbide_luzera = sizeof(보낸주소);
    if (lotu_helbide(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (lotu_helbide(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || errorearen_zenbaki != 98) return 3;
    if (lotu_helbide(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char eduki_balio[] = "한글 UDP loopback 😀";
    char RECEIVED_balio[64] = {};
    if (자료전문보내기(보내는곳, eduki_balio, sizeof(eduki_balio), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(eduki_balio)) return 5;
    if (자료전문받기(받는곳, (void *)eduki_balio, sizeof(eduki_balio), 0, 0, 0) != -1 || errorearen_zenbaki != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_balio, sizeof(RECEIVED_balio), 0, (통신주소 *)&보낸주소, &helbide_luzera) != sizeof(eduki_balio)) return 7;
    if (helbide_luzera != sizeof(보낸주소) || 장치차례짧은수(보낸주소.ataka_zenbaki) != 7778 || gailu_ordena_osoko_zenbaki(보낸주소.Internet_helbide.helbide_balio) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(eduki_balio); 순번++) if (RECEIVED_balio[순번] != eduki_balio[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_balio, sizeof(RECEIVED_balio), 0, 0, 0) != -1 || errorearen_zenbaki != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_balio, sizeof(eduki_balio), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(eduki_balio)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_balio, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_balio, 4, 0, 0, 0) != -1 || errorearen_zenbaki != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, eduki_balio, sizeof(eduki_balio), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(eduki_balio)) return 14;
    if (자료전문보내기(보내는곳, eduki_balio, sizeof(eduki_balio), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || errorearen_zenbaki != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_balio, sizeof(RECEIVED_balio), 0, 0, 0) != sizeof(eduki_balio)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internet_helbide.helbide_balio = sare_osoko_zenbaki(0x08080808);
    if (자료전문보내기(보내는곳, eduki_balio, sizeof(eduki_balio), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || errorearen_zenbaki != 101) return 17;
    if (sortu_amaiera_puntu(hodei_sorta, Stream_sare, 전문전송규약) != -1 || errorearen_zenbaki != 93) return 18;
    helbide_luzera = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &helbide_luzera) || 장치차례짧은수(보낸주소.ataka_zenbaki) != 7777) return 19;
    if (itxi_fitxategi(받는곳) || itxi_fitxategi(받는곳) != -1 || errorearen_zenbaki != 9) return 20;
    // 보내는곳은 열어 둔다: irten_aplik 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    idatzi_fitxategi_datuak(1, 완료, sizeof(완료) - 1);
    return 0;
}
