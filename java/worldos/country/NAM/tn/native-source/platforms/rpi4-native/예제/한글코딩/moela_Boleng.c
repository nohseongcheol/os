#include "통신규약.h"

int simolola_modirisi_Tiriso(int 인수) {
    (void)인수;
    struct 인터넷통신주소 aterese = {0};
    aterese.aterese_Lelapa = tlelaote_Lelapa;
    aterese.접속번호 = 망차례짧은수(9260);
    aterese.aterese_ya_Inthanete.aterese_Boleng = Neteweke_Palotlalo(되돌림주소);
    int sefara_Boleng = 통신종단점만들기(tlelaote_Lelapa, moela_Neteweke, 흐름전송규약);
    if (sefara_Boleng < 0 || BIND_aterese(sefara_Boleng, (struct 통신주소 *)&aterese, sizeof(aterese)) < 0 ||
        통신연결기다리기(sefara_Boleng, 4) < 0) return 1;
    if (amogela_kgolagano_ya_neteweke(sefara_Boleng, 0, 0) != -1 || 오류번호 != 11) return 2;
    int moeng_Boleng = 통신종단점만들기(tlelaote_Lelapa, moela_Neteweke, 흐름전송규약);
    if (moeng_Boleng < 0 || Golaganya_Neteweke(moeng_Boleng, (struct 통신주소 *)&aterese, sizeof(aterese)) < 0) return 3;
    int Golaganya = amogela_kgolagano_ya_neteweke(sefara_Boleng, 0, 0);
    if (Golaganya < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int boleele_Boleng = kwala_faele_tshedimosetso(moeng_Boleng, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (boleele_Boleng <= 0) return 5;
        보낸수 += boleele_Boleng;
    }
    if (kwala_faele_tshedimosetso(moeng_Boleng, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Morago_Boleng EOF가 된다. */
    tswala_faele(moeng_Boleng);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int boleele_Boleng = 파일자료읽기(Golaganya, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (boleele_Boleng <= 0) return 7;
        받은수 += boleele_Boleng;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Golaganya, 받은것, 1) != 0) return 9;
    if (kwala_faele_tshedimosetso(Golaganya, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    tswala_faele(Golaganya); tswala_faele(sefara_Boleng);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    kwala_faele_tshedimosetso(1, 결과, sizeof(결과) - 1);
    return 0;
}
