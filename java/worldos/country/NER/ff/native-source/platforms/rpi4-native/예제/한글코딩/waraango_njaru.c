#include "통신규약.h"

int huɓɓude_kuutoro_tafirde(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ñiiɓirde = {0};
    ñiiɓirde.주소갈래 = 인터넷주소갈래;
    ñiiɓirde.접속번호 = 망차례짧은수(9260);
    ñiiɓirde.ñiiɓirde_enternet.ñiiɓirde_njaru = 망차례정수(되돌림주소);
    int sarworde_njaru = 통신종단점만들기(인터넷주소갈래, waraango_laylaytol, 흐름전송규약);
    if (sarworde_njaru < 0 || seŋondir_ñiiɓirde(sarworde_njaru, (struct 통신주소 *)&ñiiɓirde, sizeof(ñiiɓirde)) < 0 ||
        통신연결기다리기(sarworde_njaru, 4) < 0) return 1;
    if (통신연결받기(sarworde_njaru, 0, 0) != -1 || 오류번호 != 11) return 2;
    int 손님 = 통신종단점만들기(인터넷주소갈래, waraango_laylaytol, 흐름전송규약);
    if (손님 < 0 || seŋaade_laylaytol(손님, (struct 통신주소 *)&ñiiɓirde, sizeof(ñiiɓirde)) < 0) return 3;
    int seŋaade = 통신연결받기(sarworde_njaru, 0, 0);
    if (seŋaade < 0) return 4;
    unsigned char 보낼것[1500], 받은것[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int njuuteendi_njaru = winndude_fiilde_keɓe(손님, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (njuuteendi_njaru <= 0) return 5;
        보낸수 += njuuteendi_njaru;
    }
    if (winndude_fiilde_keɓe(손님, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Caggal_njaru EOF가 된다. */
    uddude_fiilde(손님);
    int 받은수 = 0;
    while (받은수 < 보낸수) {
        int njuuteendi_njaru = 파일자료읽기(seŋaade, 받은것 + 받은수, sizeof(받은것) - 받은수);
        if (njuuteendi_njaru <= 0) return 7;
        받은수 += njuuteendi_njaru;
    }
    for (int 수 = 0; 수 < 받은수; 수++) if (받은것[수] != 보낼것[수]) return 8;
    if (파일자료읽기(seŋaade, 받은것, 1) != 0) return 9;
    if (winndude_fiilde_keɓe(seŋaade, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    uddude_fiilde(seŋaade); uddude_fiilde(sarworde_njaru);
    const char 결과[] = "C posix-kor 연결형 통신 PASS\n";
    winndude_fiilde_keɓe(1, 결과, sizeof(결과) - 1);
    return 0;
}
