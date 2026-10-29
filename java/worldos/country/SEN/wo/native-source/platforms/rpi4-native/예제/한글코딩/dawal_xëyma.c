#include "통신규약.h"

int Door_kiy_jariñoo_internet_jëfekaay(int 인수) {
    (void)인수;
    struct 인터넷통신주소 dëkkuwaay = {0};
    dëkkuwaay.dëkkuwaay_Njaboot = net_Njaboot;
    dëkkuwaay.접속번호 = 망차례짧은수(9260);
    dëkkuwaay.dëkkuwaayu_Internet.dëkkuwaay_xëyma = mbaal_lëmm(되돌림주소);
    int dëggu_xëyma = 통신종단점만들기(net_Njaboot, dawal_mbaal, 흐름전송규약);
    if (dëggu_xëyma < 0 || BIND_dëkkuwaay(dëggu_xëyma, (struct 통신주소 *)&dëkkuwaay, sizeof(dëkkuwaay)) < 0 ||
        통신연결기다리기(dëggu_xëyma, 4) < 0) return 1;
    if (nangu_Lonkug_Mbaal(dëggu_xëyma, 0, 0) != -1 || 오류번호 != 11) return 2;
    int gan_xëyma = 통신종단점만들기(net_Njaboot, dawal_mbaal, 흐름전송규약);
    if (gan_xëyma < 0 || JOKKOO_mbaal(gan_xëyma, (struct 통신주소 *)&dëkkuwaay, sizeof(dëkkuwaay)) < 0) return 3;
    int JOKKOO = nangu_Lonkug_Mbaal(dëggu_xëyma, 0, 0);
    if (JOKKOO < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int diir_xëyma = biir_bara_denc_mbir(gan_xëyma, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (diir_xëyma <= 0) return 5;
        보낸수 += diir_xëyma;
    }
    if (biir_bara_denc_mbir(gan_xëyma, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 woñeeku_xëyma EOF가 된다. */
    Tej_bara_denc(gan_xëyma);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int diir_xëyma = 파일자료읽기(JOKKOO, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (diir_xëyma <= 0) return 7;
        받은수 += diir_xëyma;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(JOKKOO, 받은것, 1) != 0) return 9;
    if (biir_bara_denc_mbir(JOKKOO, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    Tej_bara_denc(JOKKOO); Tej_bara_denc(dëggu_xëyma);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    biir_bara_denc_mbir(1, 결과, sizeof(결과) - 1);
    return 0;
}
