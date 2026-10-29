#include "통신규약.h"

int başlat_ulanyjy_programma(int 인수) {
    (void)인수;
    struct 인터넷통신주소 salgy = {0};
    salgy.salgy_Maşgala = bulut_Maşgala;
    salgy.접속번호 = 망차례짧은수(9260);
    salgy.Internet_salgy.salgy_baha = Tor_bitin(되돌림주소);
    int serwer_baha = 통신종단점만들기(bulut_Maşgala, Stream_Tor, 흐름전송규약);
    if (serwer_baha < 0 || BIND_salgy(serwer_baha, (struct 통신주소 *)&salgy, sizeof(salgy)) < 0 ||
        통신연결기다리기(serwer_baha, 4) < 0) return 1;
    if (kabul_et_tor_birikmesi(serwer_baha, 0, 0) != -1 || 오류번호 != 11) return 2;
    int 손님 = 통신종단점만들기(bulut_Maşgala, Stream_Tor, 흐름전송규약);
    if (손님 < 0 || Birikme_Tor(손님, (struct 통신주소 *)&salgy, sizeof(salgy)) < 0) return 3;
    int Birikme = kabul_et_tor_birikmesi(serwer_baha, 0, 0);
    if (Birikme < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int dowamlylyk_baha = ýaz_faýl_maglumat(손님, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (dowamlylyk_baha <= 0) return 5;
        보낸수 += dowamlylyk_baha;
    }
    if (ýaz_faýl_maglumat(손님, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Yza_baha EOF가 된다. */
    ýap_faýl(손님);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int dowamlylyk_baha = 파일자료읽기(Birikme, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (dowamlylyk_baha <= 0) return 7;
        받은수 += dowamlylyk_baha;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Birikme, 받은것, 1) != 0) return 9;
    if (ýaz_faýl_maglumat(Birikme, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    ýap_faýl(Birikme); ýap_faýl(serwer_baha);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    ýaz_faýl_maglumat(1, 결과, sizeof(결과) - 1);
    return 0;
}
