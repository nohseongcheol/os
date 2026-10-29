#include "통신규약.h"

int achuwalaa_ka_yataayakalü_akumajiaa(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ejepüsee = {0};
    ejepüsee.주소갈래 = 인터넷주소갈래;
    ejepüsee.접속번호 = 망차례짧은수(9260);
    ejepüsee.ejepüsee_Internet.ejepüsee_ajutuu = kusu_waneepiasü(되돌림주소);
    int 서버 = 통신종단점만들기(인터넷주소갈래, palantüsü_kusu, 흐름전송규약);
    if (서버 < 0 || alaasajaa_ejepüsee(서버, (struct 통신주소 *)&ejepüsee, sizeof(ejepüsee)) < 0 ||
        통신연결기다리기(서버, 4) < 0) return 1;
    if (통신연결받기(서버, 0, 0) != -1 || 오류번호 != 11) return 2;
    int 손님 = 통신종단점만들기(인터넷주소갈래, palantüsü_kusu, 흐름전송규약);
    if (손님 < 0 || a_ataa_kusu(손님, (struct 통신주소 *)&ejepüsee, sizeof(ejepüsee)) < 0) return 3;
    int a_ataa = 통신연결받기(서버, 0, 0);
    if (a_ataa < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int akaliaa_ajutuu = ashajaa_anaajaalaa_atijaaya(손님, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (akaliaa_ajutuu <= 0) return 5;
        보낸수 += akaliaa_ajutuu;
    }
    if (ashajaa_anaajaalaa_atijaaya(손님, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 뒤 EOF가 된다. */
    asürülaa_anaajaalaa(손님);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int akaliaa_ajutuu = 파일자료읽기(a_ataa, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (akaliaa_ajutuu <= 0) return 7;
        받은수 += akaliaa_ajutuu;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(a_ataa, 받은것, 1) != 0) return 9;
    if (ashajaa_anaajaalaa_atijaaya(a_ataa, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    asürülaa_anaajaalaa(a_ataa); asürülaa_anaajaalaa(서버);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    ashajaa_anaajaalaa_atijaaya(1, 결과, sizeof(결과) - 1);
    return 0;
}
