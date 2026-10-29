#include "통신규약.h"
static 인터넷통신주소 ADDRESS(unsigned port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.ADDRESS_Pere = pilv_Pere;
    VALUE.pordinumber = 망차례짧은수(port_VALUE); VALUE.Interneti_aadress.ADDRESS_VALUE = võrk_täisarv(tagasisideaadress); return VALUE;
}
extern "C" int START_kasutaja_programm(int) {
    int 보내는곳 = avama_osaleja(pilv_Pere, datagrammisokkel, 0);
    int 받는곳 = avama_osaleja(pilv_Pere, datagrammisokkel, datagramm_protokoll);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = ADDRESS(7777), 출발 = ADDRESS(7778), 보낸주소 = {};
    통신주소길이형 주소길이 = sizeof(보낸주소);
    if (BIND_ADDRESS(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || tõrke_number != 98) return 3;
    if (BIND_ADDRESS(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Sisu_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (saatma_datagramm_andmed(보내는곳, Sisu_VALUE, sizeof(Sisu_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Sisu_VALUE)) return 5;
    if (saama_datagramm_andmed(받는곳, (void *)Sisu_VALUE, sizeof(Sisu_VALUE), 0, 0, 0) != -1 || tõrke_number != 14) return 6;
    if (saama_datagramm_andmed(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &주소길이) != sizeof(Sisu_VALUE)) return 7;
    if (주소길이 != sizeof(보낸주소) || 장치차례짧은수(보낸주소.pordinumber) != 7778 || seade_tellimus_täisarv(보낸주소.Interneti_aadress.ADDRESS_VALUE) != tagasisideaadress) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Sisu_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Sisu_VALUE[순번]) return 9;
    if (saama_datagramm_andmed(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || tõrke_number != 11) return 10;
    if (saatma_datagramm_andmed(받는곳, RECEIVED_VALUE, sizeof(Sisu_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Sisu_VALUE)) return 11;
    if (saama_datagramm_andmed(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (saama_datagramm_andmed(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || tõrke_number != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (saatma_datagramm_andmed(보내는곳, Sisu_VALUE, sizeof(Sisu_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Sisu_VALUE)) return 14;
    if (saatma_datagramm_andmed(보내는곳, Sisu_VALUE, sizeof(Sisu_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || tõrke_number != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (saama_datagramm_andmed(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Sisu_VALUE)) return 16;
    if (saatma_datagramm_andmed(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        saama_datagramm_andmed(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Interneti_aadress.ADDRESS_VALUE = võrk_täisarv(0x08080808);
    if (saatma_datagramm_andmed(보내는곳, Sisu_VALUE, sizeof(Sisu_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || tõrke_number != 101) return 17;
    if (avama_osaleja(pilv_Pere, voog_võrk, datagramm_protokoll) != -1 || tõrke_number != 93) return 18;
    주소길이 = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &주소길이) || 장치차례짧은수(보낸주소.pordinumber) != 7777) return 19;
    if (Sule_Fail(받는곳) || Sule_Fail(받는곳) != -1 || tõrke_number != 9) return 20;
    // 보내는곳은 열어 둔다: Välju_programm 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    kirjutamine_Fail_andmed(1, 완료, sizeof(완료) - 1);
    return 0;
}
