#include "통신규약.h"
static 인터넷통신주소 slóð(unsigned gátt_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.slóð_Fjölskylda = skýið_Fjölskylda;
    VALUE.tengisnúmer = 망차례짧은수(gátt_VALUE); VALUE.veffang.slóð_VALUE = Net_heiltala(되돌림주소); return VALUE;
}
extern "C" int Opna_notandi_forrit(int) {
    int 보내는곳 = stofna_endastöð(skýið_Fjölskylda, 전문통신, 0);
    int 받는곳 = stofna_endastöð(skýið_Fjölskylda, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = slóð(7777), 출발 = slóð(7778), 보낸주소 = {};
    통신주소길이형 slóð_lengd_6e50507f = sizeof(보낸주소);
    if (BIND_slóð(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_slóð(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || villa_númer != 98) return 3;
    if (BIND_slóð(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Efni_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Efni_VALUE, sizeof(Efni_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Efni_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Efni_VALUE, sizeof(Efni_VALUE), 0, 0, 0) != -1 || villa_númer != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &slóð_lengd_6e50507f) != sizeof(Efni_VALUE)) return 7;
    if (slóð_lengd_6e50507f != sizeof(보낸주소) || 장치차례짧은수(보낸주소.tengisnúmer) != 7778 || tæki_röð_heiltala(보낸주소.veffang.slóð_VALUE) != 되돌림주소) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Efni_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Efni_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || villa_númer != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Efni_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Efni_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || villa_númer != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Efni_VALUE, sizeof(Efni_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Efni_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Efni_VALUE, sizeof(Efni_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || villa_númer != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Efni_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.veffang.slóð_VALUE = Net_heiltala(0x08080808);
    if (자료전문보내기(보내는곳, Efni_VALUE, sizeof(Efni_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || villa_númer != 101) return 17;
    if (stofna_endastöð(skýið_Fjölskylda, Stream_Net, 전문전송규약) != -1 || villa_númer != 93) return 18;
    slóð_lengd_6e50507f = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &slóð_lengd_6e50507f) || 장치차례짧은수(보낸주소.tengisnúmer) != 7777) return 19;
    if (loka_skrá(받는곳) || loka_skrá(받는곳) != -1 || villa_númer != 9) return 20;
    // 보내는곳은 열어 둔다: loka_forrit 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    skrifa_skrá_gögn(1, 완료, sizeof(완료) - 1);
    return 0;
}
