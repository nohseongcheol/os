#include "통신규약.h"
static 인터넷통신주소 adrese(unsigned ports_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.adrese_saime = mākonis_saime;
    VALUE.porta_numurs = 망차례짧은수(ports_VALUE); VALUE.interneta_adrese.adrese_VALUE = tīkls_vesels_skaitlis(atgriezeniskās_cilpas_adrese); return VALUE;
}
extern "C" int Sākt_lietotājs_programma(int) {
    int 보내는곳 = atvērt_dalībnieks(mākonis_saime, datogrammas_ligzda, 0);
    int 받는곳 = atvērt_dalībnieks(mākonis_saime, datogrammas_ligzda, datogramma_protokols);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = adrese(7777), 출발 = adrese(7778), 보낸주소 = {};
    통신주소길이형 주소길이 = sizeof(보낸주소);
    if (BIND_adrese(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_adrese(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || kļūdas_numurs != 98) return 3;
    if (BIND_adrese(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Saturs_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (sūtīt_datogramma_dati(보내는곳, Saturs_VALUE, sizeof(Saturs_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Saturs_VALUE)) return 5;
    if (saņemt_datogramma_dati(받는곳, (void *)Saturs_VALUE, sizeof(Saturs_VALUE), 0, 0, 0) != -1 || kļūdas_numurs != 14) return 6;
    if (saņemt_datogramma_dati(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &주소길이) != sizeof(Saturs_VALUE)) return 7;
    if (주소길이 != sizeof(보낸주소) || 장치차례짧은수(보낸주소.porta_numurs) != 7778 || ierīce_secība_vesels_skaitlis(보낸주소.interneta_adrese.adrese_VALUE) != atgriezeniskās_cilpas_adrese) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Saturs_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Saturs_VALUE[순번]) return 9;
    if (saņemt_datogramma_dati(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || kļūdas_numurs != 11) return 10;
    if (sūtīt_datogramma_dati(받는곳, RECEIVED_VALUE, sizeof(Saturs_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Saturs_VALUE)) return 11;
    if (saņemt_datogramma_dati(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (saņemt_datogramma_dati(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || kļūdas_numurs != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (sūtīt_datogramma_dati(보내는곳, Saturs_VALUE, sizeof(Saturs_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Saturs_VALUE)) return 14;
    if (sūtīt_datogramma_dati(보내는곳, Saturs_VALUE, sizeof(Saturs_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || kļūdas_numurs != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (saņemt_datogramma_dati(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Saturs_VALUE)) return 16;
    if (sūtīt_datogramma_dati(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        saņemt_datogramma_dati(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.interneta_adrese.adrese_VALUE = tīkls_vesels_skaitlis(0x08080808);
    if (sūtīt_datogramma_dati(보내는곳, Saturs_VALUE, sizeof(Saturs_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || kļūdas_numurs != 101) return 17;
    if (atvērt_dalībnieks(mākonis_saime, Stream_tīkls, datogramma_protokols) != -1 || kļūdas_numurs != 93) return 18;
    주소길이 = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &주소길이) || 장치차례짧은수(보낸주소.porta_numurs) != 7777) return 19;
    if (Aizvērt_Fails(받는곳) || Aizvērt_Fails(받는곳) != -1 || kļūdas_numurs != 9) return 20;
    // 보내는곳은 열어 둔다: Iziet_programma 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    rakstīšana_Fails_dati(1, 완료, sizeof(완료) - 1);
    return 0;
}
