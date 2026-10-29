#include "통신규약.h"

int START_brukar_app(int Argument) {
    (void)Argument;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Familie = sky_Familie;
    ADDRESS.portnummer = 망차례짧은수(9260);
    ADDRESS.Internett_adresse.ADDRESS_VALUE = Nettverk_heiltal(되돌림주소);
    int tenar_VALUE = Opprett_endepunkt(sky_Familie, Stream_Nettverk, 흐름전송규약);
    if (tenar_VALUE < 0 || BIND_ADDRESS(tenar_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(tenar_VALUE, 4) < 0) return 1;
    if (godta_nettverkstilkopling(tenar_VALUE, 0, 0) != -1 || feilnummer != 11) return 2;
    int gjest_VALUE = Opprett_endepunkt(sky_Familie, Stream_Nettverk, 흐름전송규약);
    if (gjest_VALUE < 0 || KOPLE_TIL_Nettverk(gjest_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int Kopla_til = godta_nettverkstilkopling(tenar_VALUE, 0, 0);
    if (Kopla_til < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_vare[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int lengd_VALUE = skrive_fil_data(gjest_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (lengd_VALUE <= 0) return 5;
        보낸수 += lengd_VALUE;
    }
    if (skrive_fil_data(gjest_VALUE, 보낼것, 1) != -1 || feilnummer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 TILBAKE_VALUE EOF가 된다. */
    Lukk_fil(gjest_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int lengd_VALUE = 파일자료읽기(Kopla_til, RECEIVED_vare + RECEIVED_COUNT, sizeof(RECEIVED_vare) - RECEIVED_COUNT);
        if (lengd_VALUE <= 0) return 7;
        RECEIVED_COUNT += lengd_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_vare[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Kopla_til, RECEIVED_vare, 1) != 0) return 9;
    if (skrive_fil_data(Kopla_til, 보낼것, 1) != -1 || feilnummer != 32) return 10;
    Lukk_fil(Kopla_til); Lukk_fil(tenar_VALUE);
    const char forretningsmål[] = "C posix-kor 연결형 통신 PASS\n";
    skrive_fil_data(1, forretningsmål, sizeof(forretningsmål) - 1);
    return 0;
}
