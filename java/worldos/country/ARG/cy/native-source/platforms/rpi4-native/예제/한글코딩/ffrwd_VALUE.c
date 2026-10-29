#include "통신규약.h"

int START_defnyddiwr_Rhaglen(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Teulu = cwmwl_Teulu;
    ADDRESS.rhif_porth = 망차례짧은수(9260);
    ADDRESS.cyfeiriad_rhyngrwyd.ADDRESS_VALUE = Rhwydwaith_cyfanrif(cyfeiriad_modd_cylchu);
    int gweinydd_VALUE = 통신종단점만들기(cwmwl_Teulu, ffrwd_Rhwydwaith, 흐름전송규약);
    if (gweinydd_VALUE < 0 || BIND_ADDRESS(gweinydd_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(gweinydd_VALUE, 4) < 0) return 1;
    if (derbyn_cysylltiad_rhwydwaith(gweinydd_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int gwestai_VALUE = 통신종단점만들기(cwmwl_Teulu, ffrwd_Rhwydwaith, 흐름전송규약);
    if (gwestai_VALUE < 0 || Cysylltu_Rhwydwaith(gwestai_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int Cysylltu = derbyn_cysylltiad_rhwydwaith(gweinydd_VALUE, 0, 0);
    if (Cysylltu < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_eitem[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int hyd_VALUE = ysgrifennu_ffeil_data(gwestai_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (hyd_VALUE <= 0) return 5;
        보낸수 += hyd_VALUE;
    }
    if (ysgrifennu_ffeil_data(gwestai_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VALUE EOF가 된다. */
    cau_ffeil(gwestai_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int hyd_VALUE = 파일자료읽기(Cysylltu, RECEIVED_eitem + RECEIVED_COUNT, sizeof(RECEIVED_eitem) - RECEIVED_COUNT);
        if (hyd_VALUE <= 0) return 7;
        RECEIVED_COUNT += hyd_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_eitem[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Cysylltu, RECEIVED_eitem, 1) != 0) return 9;
    if (ysgrifennu_ffeil_data(Cysylltu, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    cau_ffeil(Cysylltu); cau_ffeil(gweinydd_VALUE);
    const char mesur[] = "C posix-kor 연결형 통신 PASS\n";
    ysgrifennu_ffeil_data(1, mesur, sizeof(mesur) - 1);
    return 0;
}
