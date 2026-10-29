#include "통신규약.h"

int Thomišo_mošomiši_tirišo(int 인수) {
    (void)인수;
    struct 인터넷통신주소 atrese = {0};
    atrese.atrese_Lapa = Inthanete_Lapa;
    atrese.접속번호 = 망차례짧은수(9260);
    atrese.atrese_ya_Inthanete.atrese_boleng = Netweke_palotlalo(되돌림주소);
    int seba_boleng = 통신종단점만들기(Inthanete_Lapa, Stream_Netweke, 흐름전송규약);
    if (seba_boleng < 0 || tlama_atrese(seba_boleng, (struct 통신주소 *)&atrese, sizeof(atrese)) < 0 ||
        통신연결기다리기(seba_boleng, 4) < 0) return 1;
    if (amogela_kgokaganyo_ya_dinetweke(seba_boleng, 0, 0) != -1 || 오류번호 != 11) return 2;
    int moeng_boleng = 통신종단점만들기(Inthanete_Lapa, Stream_Netweke, 흐름전송규약);
    if (moeng_boleng < 0 || KGOKAGANYA_Netweke(moeng_boleng, (struct 통신주소 *)&atrese, sizeof(atrese)) < 0) return 3;
    int Ikgokaganye = amogela_kgokaganyo_ya_dinetweke(seba_boleng, 0, 0);
    if (Ikgokaganye < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int botelele_boleng = ngwala_faele_data(moeng_boleng, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (botelele_boleng <= 0) return 5;
        보낸수 += botelele_boleng;
    }
    if (ngwala_faele_data(moeng_boleng, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Morago_boleng EOF가 된다. */
    tswalela_faele(moeng_boleng);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int botelele_boleng = 파일자료읽기(Ikgokaganye, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (botelele_boleng <= 0) return 7;
        받은수 += botelele_boleng;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Ikgokaganye, 받은것, 1) != 0) return 9;
    if (ngwala_faele_data(Ikgokaganye, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    tswalela_faele(Ikgokaganye); tswalela_faele(seba_boleng);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    ngwala_faele_data(1, 결과, sizeof(결과) - 1);
    return 0;
}
