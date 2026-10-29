#include "통신규약.h"
static 인터넷통신주소 ENDEREZO(unsigned porto_VALOR) {
    인터넷통신주소 VALOR = {}; VALOR.ENDEREZO_Familia = nube_Familia;
    VALOR.número_do_porto = 망차례짧은수(porto_VALOR); VALOR.enderezo_de_internet.ENDEREZO_VALOR = Rede_número_enteiro(되돌림주소); return VALOR;
}
extern "C" int START_usuario_apl(int) {
    int 보내는곳 = crear_extremo(nube_Familia, 전문통신, 0);
    int 받는곳 = crear_extremo(nube_Familia, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ENDEREZO(7777), 출발 = ENDEREZO(7778), 보낸주소 = {};
    통신주소길이형 ENDEREZO_duración = sizeof(보낸주소);
    if (ligar_ENDEREZO(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (ligar_ENDEREZO(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || número_de_erro != 98) return 3;
    if (ligar_ENDEREZO(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Contido_VALOR[] = "한글 UDP loopback 😀";
    char RECIBIDO_VALOR[64] = {};
    if (자료전문보내기(보내는곳, Contido_VALOR, sizeof(Contido_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Contido_VALOR)) return 5;
    if (자료전문받기(받는곳, (void *)Contido_VALOR, sizeof(Contido_VALOR), 0, 0, 0) != -1 || número_de_erro != 14) return 6;
    if (자료전문받기(받는곳, RECIBIDO_VALOR, sizeof(RECIBIDO_VALOR), 0, (통신주소 *)&보낸주소, &ENDEREZO_duración) != sizeof(Contido_VALOR)) return 7;
    if (ENDEREZO_duración != sizeof(보낸주소) || 장치차례짧은수(보낸주소.número_do_porto) != 7778 || dispositivo_orde_número_enteiro(보낸주소.enderezo_de_internet.ENDEREZO_VALOR) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Contido_VALOR); 순번++) if (RECIBIDO_VALOR[순번] != Contido_VALOR[순번]) return 9;
    if (자료전문받기(받는곳, RECIBIDO_VALOR, sizeof(RECIBIDO_VALOR), 0, 0, 0) != -1 || número_de_erro != 11) return 10;
    if (자료전문보내기(받는곳, RECIBIDO_VALOR, sizeof(Contido_VALOR), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Contido_VALOR)) return 11;
    if (자료전문받기(보내는곳, RECIBIDO_VALOR, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECIBIDO_VALOR, 4, 0, 0, 0) != -1 || número_de_erro != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Contido_VALOR, sizeof(Contido_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Contido_VALOR)) return 14;
    if (자료전문보내기(보내는곳, Contido_VALOR, sizeof(Contido_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || número_de_erro != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECIBIDO_VALOR, sizeof(RECIBIDO_VALOR), 0, 0, 0) != sizeof(Contido_VALOR)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.enderezo_de_internet.ENDEREZO_VALOR = Rede_número_enteiro(0x08080808);
    if (자료전문보내기(보내는곳, Contido_VALOR, sizeof(Contido_VALOR), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || número_de_erro != 101) return 17;
    if (crear_extremo(nube_Familia, fluxo_Rede, 전문전송규약) != -1 || número_de_erro != 93) return 18;
    ENDEREZO_duración = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &ENDEREZO_duración) || 장치차례짧은수(보낸주소.número_do_porto) != 7777) return 19;
    if (peche_Ficheiro(받는곳) || peche_Ficheiro(받는곳) != -1 || número_de_erro != 9) return 20;
    // 보내는곳은 열어 둔다: saír_apl 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    escribir_Ficheiro_datos(1, 완료, sizeof(완료) - 1);
    return 0;
}
