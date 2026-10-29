#include "통신규약.h"

int Start_cleachdaiche_ap(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_teaghlach = neul_teaghlach;
    ADDRESS.접속번호 = 망차례짧은수(9260);
    ADDRESS.Seòladh_eadar_lìn.ADDRESS_VALUE = lìonra_àireamh_shlàn(되돌림주소);
    int frithealaiche_VALUE = 통신종단점만들기(neul_teaghlach, sruth_lìonra, 흐름전송규약);
    if (frithealaiche_VALUE < 0 || BIND_ADDRESS(frithealaiche_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(frithealaiche_VALUE, 4) < 0) return 1;
    if (gabh_ris_ceangal_lìonraidh(frithealaiche_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int aoigh_VALUE = 통신종단점만들기(neul_teaghlach, sruth_lìonra, 흐름전송규약);
    if (aoigh_VALUE < 0 || CONNECT_lìonra(aoigh_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int CONNECT = gabh_ris_ceangal_lìonraidh(frithealaiche_VALUE, 0, 0);
    if (CONNECT < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_nì[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int faid_VALUE = sgrìobh_faidhle_dàta(aoigh_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (faid_VALUE <= 0) return 5;
        보낸수 += faid_VALUE;
    }
    if (sgrìobh_faidhle_dàta(aoigh_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Air_ais_VALUE EOF가 된다. */
    dùin_faidhle(aoigh_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int faid_VALUE = 파일자료읽기(CONNECT, RECEIVED_nì + RECEIVED_COUNT, sizeof(RECEIVED_nì) - RECEIVED_COUNT);
        if (faid_VALUE <= 0) return 7;
        RECEIVED_COUNT += faid_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_nì[수] != 보낼것[수]) return 8;
    if (파일자료읽기(CONNECT, RECEIVED_nì, 1) != 0) return 9;
    if (sgrìobh_faidhle_dàta(CONNECT, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    dùin_faidhle(CONNECT); dùin_faidhle(frithealaiche_VALUE);
    const char tomhas[] = "C posix-kor 연결형 통신 PASS\n";
    sgrìobh_faidhle_dàta(1, tomhas, sizeof(tomhas) - 1);
    return 0;
}
