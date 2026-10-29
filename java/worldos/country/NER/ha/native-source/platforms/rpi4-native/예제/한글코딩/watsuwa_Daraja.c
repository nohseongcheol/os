#include "통신규약.h"

int Fara_Mai_anfani_da_kwamfuta_Shiri(int 인수) {
    (void)인수;
    struct 인터넷통신주소 imel = {0};
    imel.imel_Iyali = Intanet_Iyali;
    imel.lambar_kafa = 망차례짧은수(9260);
    imel.Adireshin_yanar_gizo.imel_Daraja = Hanyar_sadarwa_Lamba_mara(되돌림주소);
    int Saba_Daraja = 통신종단점만들기(Intanet_Iyali, watsuwa_Hanyar_sadarwa, 흐름전송규약);
    if (Saba_Daraja < 0 || BIND_imel(Saba_Daraja, (struct 통신주소 *)&imel, sizeof(imel)) < 0 ||
        통신연결기다리기(Saba_Daraja, 4) < 0) return 1;
    if (통신연결받기(Saba_Daraja, 0, 0) != -1 || 오류번호 != 11) return 2;
    int baƙo_Daraja = 통신종단점만들기(Intanet_Iyali, watsuwa_Hanyar_sadarwa, 흐름전송규약);
    if (baƙo_Daraja < 0 || HAƊI_Hanyar_sadarwa(baƙo_Daraja, (struct 통신주소 *)&imel, sizeof(imel)) < 0) return 3;
    int Haɗi = 통신연결받기(Saba_Daraja, 0, 0);
    if (Haɗi < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int Tsawo_Daraja = Rubuta_Fayil_Tarin_bayani(baƙo_Daraja, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (Tsawo_Daraja <= 0) return 5;
        보낸수 += Tsawo_Daraja;
    }
    if (Rubuta_Fayil_Tarin_bayani(baƙo_Daraja, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Baya_Daraja EOF가 된다. */
    Rufe_Fayil(baƙo_Daraja);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int Tsawo_Daraja = 파일자료읽기(Haɗi, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (Tsawo_Daraja <= 0) return 7;
        받은수 += Tsawo_Daraja;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Haɗi, 받은것, 1) != 0) return 9;
    if (Rubuta_Fayil_Tarin_bayani(Haɗi, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    Rufe_Fayil(Haɗi); Rufe_Fayil(Saba_Daraja);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    Rubuta_Fayil_Tarin_bayani(1, 결과, sizeof(결과) - 1);
    return 0;
}
