#include "통신규약.h"

int pigiarli_atuqtuq_pilirijjut(int 인수) {
    (void)인수;
    struct 인터넷통신주소 turaarut = {0};
    turaarut.turaarut_illumiuqatigiit = cloud_illumiuqatigiit;
    turaarut.접속번호 = 망차례짧은수(9260);
    turaarut.Ikiaqqivikkut_turaarut.turaarut_atuutilik = Kasuqatigiitsimajut_naasaut(되돌림주소);
    int ikiaqqitittivik_atuutilik = 통신종단점만들기(cloud_illumiuqatigiit, ingirrania_aulataup_Kasuqatigiitsimajut, 흐름전송규약);
    if (ikiaqqitittivik_atuutilik < 0 || unittilli_turaarut(ikiaqqitittivik_atuutilik, (struct 통신주소 *)&turaarut, sizeof(turaarut)) < 0 ||
        통신연결기다리기(ikiaqqitittivik_atuutilik, 4) < 0) return 1;
    if (통신연결받기(ikiaqqitittivik_atuutilik, 0, 0) != -1 || 오류번호 != 11) return 2;
    int 손님 = 통신종단점만들기(cloud_illumiuqatigiit, ingirrania_aulataup_Kasuqatigiitsimajut, 흐름전송규약);
    if (손님 < 0 || kasurli_Kasuqatigiitsimajut(손님, (struct 통신주소 *)&turaarut, sizeof(turaarut)) < 0) return 3;
    int kasurli = 통신연결받기(ikiaqqitittivik_atuutilik, 0, 0);
    if (kasurli < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int takininga_atuutilik = titiraq_ini_titiqqat(손님, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (takininga_atuutilik <= 0) return 5;
        보낸수 += takininga_atuutilik;
    }
    if (titiraq_ini_titiqqat(손님, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Utimut_atuutilik EOF가 된다. */
    matuli_ini(손님);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int takininga_atuutilik = 파일자료읽기(kasurli, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (takininga_atuutilik <= 0) return 7;
        받은수 += takininga_atuutilik;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(kasurli, 받은것, 1) != 0) return 9;
    if (titiraq_ini_titiqqat(kasurli, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    matuli_ini(kasurli); matuli_ini(ikiaqqitittivik_atuutilik);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    titiraq_ini_titiqqat(1, 결과, sizeof(결과) - 1);
    return 0;
}
