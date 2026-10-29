#include "통신규약.h"
static 인터넷통신주소 Adreça(unsigned port_VALOR) {
    인터넷통신주소 VALOR = {}; VALOR.ADREÇA_Família = núvol_Família;
    VALOR.número_de_port = 망차례짧은수(port_VALOR); VALOR.adreça_d_Internet.ADREÇA_VALOR = 망차례정수(되돌림주소); return VALOR;
}
extern "C" int Inici_usuari_programa(int) {
    int 보내는곳 = Crear_extrem(núvol_Família, 전문통신, 0);
    int 받는곳 = Crear_extrem(núvol_Família, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = Adreça(7777), 출발 = Adreça(7778), 보낸주소 = {};
    통신주소길이형 ADREÇA_durada = sizeof(보낸주소);
    if (enllaçar_ADREÇA(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (enllaçar_ADREÇA(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || número_d_error != 98) return 3;
    if (enllaçar_ADREÇA(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char contingut_VALOR[] = "한글 UDP loopback 😀";
    char CANTIDAD_RECIBIDA_VALOR[64] = {};
    if (자료전문보내기(보내는곳, contingut_VALOR, sizeof(contingut_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(contingut_VALOR)) return 5;
    if (자료전문받기(받는곳, (void *)contingut_VALOR, sizeof(contingut_VALOR), 0, 0, 0) != -1 || número_d_error != 14) return 6;
    if (자료전문받기(받는곳, CANTIDAD_RECIBIDA_VALOR, sizeof(CANTIDAD_RECIBIDA_VALOR), 0, (통신주소 *)&보낸주소, &ADREÇA_durada) != sizeof(contingut_VALOR)) return 7;
    if (ADREÇA_durada != sizeof(보낸주소) || 장치차례짧은수(보낸주소.número_de_port) != 7778 || 장치차례정수(보낸주소.adreça_d_Internet.ADREÇA_VALOR) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(contingut_VALOR); 순번++) if (CANTIDAD_RECIBIDA_VALOR[순번] != contingut_VALOR[순번]) return 9;
    if (자료전문받기(받는곳, CANTIDAD_RECIBIDA_VALOR, sizeof(CANTIDAD_RECIBIDA_VALOR), 0, 0, 0) != -1 || número_d_error != 11) return 10;
    if (자료전문보내기(받는곳, CANTIDAD_RECIBIDA_VALOR, sizeof(contingut_VALOR), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(contingut_VALOR)) return 11;
    if (자료전문받기(보내는곳, CANTIDAD_RECIBIDA_VALOR, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, CANTIDAD_RECIBIDA_VALOR, 4, 0, 0, 0) != -1 || número_d_error != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, contingut_VALOR, sizeof(contingut_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(contingut_VALOR)) return 14;
    if (자료전문보내기(보내는곳, contingut_VALOR, sizeof(contingut_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || número_d_error != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, CANTIDAD_RECIBIDA_VALOR, sizeof(CANTIDAD_RECIBIDA_VALOR), 0, 0, 0) != sizeof(contingut_VALOR)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.adreça_d_Internet.ADREÇA_VALOR = 망차례정수(0x08080808);
    if (자료전문보내기(보내는곳, contingut_VALOR, sizeof(contingut_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || número_d_error != 101) return 17;
    if (Crear_extrem(núvol_Família, flux_xarxa, 전문전송규약) != -1 || número_d_error != 93) return 18;
    ADREÇA_durada = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ADREÇA_durada) || 장치차례짧은수(보낸주소.número_de_port) != 7777) return 19;
    if (Tanca_arxiu(받는곳) || Tanca_arxiu(받는곳) != -1 || número_d_error != 9) return 20;
    // 보내는곳은 열어 둔다: Surt_programa 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    escriure_arxiu_dades(1, 완료, sizeof(완료) - 1);
    return 0;
}
