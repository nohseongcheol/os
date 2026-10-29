#include "통신규약.h"

int BEGIN_gebruiker_program(int 인수) {
    (void)인수;
    struct 인터넷통신주소 adres = {0};
    adres.adres_Gesin = wolk_Gesin;
    adres.접속번호 = 망차례짧은수(9260);
    adres.internetadres.adres_VALUE = Netwerk_heelgetal(되돌림주소);
    int bediener_VALUE = 통신종단점만들기(wolk_Gesin, Stream_Netwerk, 흐름전송규약);
    if (bediener_VALUE < 0 || BIND_adres(bediener_VALUE, (struct 통신주소 *)&adres, sizeof(adres)) < 0 ||
        통신연결기다리기(bediener_VALUE, 4) < 0) return 1;
    if (aanvaar_netwerkverbinding(bediener_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int gas_VALUE = 통신종단점만들기(wolk_Gesin, Stream_Netwerk, 흐름전송규약);
    if (gas_VALUE < 0 || KOPPEL_Netwerk(gas_VALUE, (struct 통신주소 *)&adres, sizeof(adres)) < 0) return 3;
    int Koppel = aanvaar_netwerkverbinding(bediener_VALUE, 0, 0);
    if (Koppel < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_item[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int lengte_VALUE = skryf_lêer_data(gas_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (lengte_VALUE <= 0) return 5;
        보낸수 += lengte_VALUE;
    }
    if (skryf_lêer_data(gas_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 TERUG_VALUE EOF가 된다. */
    sluit_lêer(gas_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int lengte_VALUE = 파일자료읽기(Koppel, RECEIVED_item + RECEIVED_COUNT, sizeof(RECEIVED_item) - RECEIVED_COUNT);
        if (lengte_VALUE <= 0) return 7;
        RECEIVED_COUNT += lengte_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_item[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Koppel, RECEIVED_item, 1) != 0) return 9;
    if (skryf_lêer_data(Koppel, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    sluit_lêer(Koppel); sluit_lêer(bediener_VALUE);
    const char maatreël[] = "C posix-kor 연결형 통신 PASS\n";
    skryf_lêer_data(1, maatreël, sizeof(maatreël) - 1);
    return 0;
}
