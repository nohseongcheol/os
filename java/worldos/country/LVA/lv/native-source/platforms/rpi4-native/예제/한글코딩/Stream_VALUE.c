#include "통신규약.h"

int Sākt_lietotājs_programma(int Parametri) {
    (void)Parametri;
    struct 인터넷통신주소 adrese = {0};
    adrese.adrese_saime = mākonis_saime;
    adrese.porta_numurs = 망차례짧은수(9260);
    adrese.interneta_adrese.adrese_VALUE = tīkls_vesels_skaitlis(atgriezeniskās_cilpas_adrese);
    int serveris_VALUE = atvērt_dalībnieks(mākonis_saime, Stream_tīkls, Stream_transporta_protokols);
    if (serveris_VALUE < 0 || BIND_adrese(serveris_VALUE, (struct 통신주소 *)&adrese, sizeof(adrese)) < 0 ||
        통신연결기다리기(serveris_VALUE, 4) < 0) return 1;
    if (akceptēt_tīkla_savienojums(serveris_VALUE, 0, 0) != -1 || kļūdas_numurs != 11) return 2;
    int viesis_VALUE = atvērt_dalībnieks(mākonis_saime, Stream_tīkls, Stream_transporta_protokols);
    if (viesis_VALUE < 0 || saziņa_tīkls(viesis_VALUE, (struct 통신주소 *)&adrese, sizeof(adrese)) < 0) return 3;
    int Savienoties = akceptēt_tīkla_savienojums(serveris_VALUE, 0, 0);
    if (Savienoties < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_krājums[1500];
    for (int numurs = 0; numurs < 1500; numurs++) 보낼것[numurs] = (unsigned char)numurs;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int 길이 = rakstīšana_Fails_dati(viesis_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (길이 <= 0) return 5;
        보낸수 += 길이;
    }
    if (rakstīšana_Fails_dati(viesis_VALUE, 보낼것, 1) != -1 || kļūdas_numurs != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ATPAKAĻ_VALUE EOF가 된다. */
    Aizvērt_Fails(viesis_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int 길이 = 파일자료읽기(Savienoties, RECEIVED_krājums + RECEIVED_COUNT, sizeof(RECEIVED_krājums) - RECEIVED_COUNT);
        if (길이 <= 0) return 7;
        RECEIVED_COUNT += 길이;
    }
    for (int numurs = 0; numurs < RECEIVED_COUNT; numurs++) if (RECEIVED_krājums[numurs] != 보낼것[numurs]) return 8;
    if (파일자료읽기(Savienoties, RECEIVED_krājums, 1) != 0) return 9;
    if (rakstīšana_Fails_dati(Savienoties, 보낼것, 1) != -1 || kļūdas_numurs != 32) return 10;
    Aizvērt_Fails(Savienoties); Aizvērt_Fails(serveris_VALUE);
    const char mērs[] = "C posix-kor 연결형 통신 PASS\n";
    rakstīšana_Fails_dati(1, mērs, sizeof(mērs) - 1);
    return 0;
}
