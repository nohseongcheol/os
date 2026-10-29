#include "통신규약.h"

int Start_kaiwhakamahi_kaupapa(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Whānau = kapua_Whānau;
    ADDRESS.접속번호 = 망차례짧은수(9260);
    ADDRESS.Wāhitau_ipurangi.ADDRESS_uara = whatunga_tau_tōpū(되돌림주소);
    int tūmau_uara = 통신종단점만들기(kapua_Whānau, roma_whatunga, 흐름전송규약);
    if (tūmau_uara < 0 || BIND_ADDRESS(tūmau_uara, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(tūmau_uara, 4) < 0) return 1;
    if (whakaae_tūhononga_whatunga(tūmau_uara, 0, 0) != -1 || 오류번호 != 11) return 2;
    int manuhiri_uara = 통신종단점만들기(kapua_Whānau, roma_whatunga, 흐름전송규약);
    if (manuhiri_uara < 0 || TŪHONO_whatunga(manuhiri_uara, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int TŪHONO = whakaae_tūhononga_whatunga(tūmau_uara, 0, 0);
    if (TŪHONO < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_tuemi[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int roa_uara = tuhi_kōnae_raraunga(manuhiri_uara, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (roa_uara <= 0) return 5;
        보낸수 += roa_uara;
    }
    if (tuhi_kōnae_raraunga(manuhiri_uara, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Hoki_uara EOF가 된다. */
    kati_kōnae(manuhiri_uara);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int roa_uara = 파일자료읽기(TŪHONO, RECEIVED_tuemi + RECEIVED_COUNT, sizeof(RECEIVED_tuemi) - RECEIVED_COUNT);
        if (roa_uara <= 0) return 7;
        RECEIVED_COUNT += roa_uara;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_tuemi[수] != 보낼것[수]) return 8;
    if (파일자료읽기(TŪHONO, RECEIVED_tuemi, 1) != 0) return 9;
    if (tuhi_kōnae_raraunga(TŪHONO, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    kati_kōnae(TŪHONO); kati_kōnae(tūmau_uara);
    const char mēhua[] = "C posix-kor 연결형 통신 PASS\n";
    tuhi_kōnae_raraunga(1, mēhua, sizeof(mēhua) - 1);
    return 0;
}
