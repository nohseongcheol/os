#include "통신규약.h"

int Opna_notandi_forrit(int Viðföng) {
    (void)Viðföng;
    struct 인터넷통신주소 slóð = {0};
    slóð.slóð_Fjölskylda = skýið_Fjölskylda;
    slóð.tengisnúmer = 망차례짧은수(9260);
    slóð.veffang.slóð_VALUE = Net_heiltala(되돌림주소);
    int þjónn_VALUE = stofna_endastöð(skýið_Fjölskylda, Stream_Net, Stream_flutningur_samskiptaregla);
    if (þjónn_VALUE < 0 || BIND_slóð(þjónn_VALUE, (struct 통신주소 *)&slóð, sizeof(slóð)) < 0 ||
        통신연결기다리기(þjónn_VALUE, 4) < 0) return 1;
    if (samþykkja_nettenging(þjónn_VALUE, 0, 0) != -1 || villa_númer != 11) return 2;
    int gestur_VALUE = stofna_endastöð(skýið_Fjölskylda, Stream_Net, Stream_flutningur_samskiptaregla);
    if (gestur_VALUE < 0 || TENGJA_Net(gestur_VALUE, (struct 통신주소 *)&slóð, sizeof(slóð)) < 0) return 3;
    int Tengjast = samþykkja_nettenging(þjónn_VALUE, 0, 0);
    if (Tengjast < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_vara[1500];
    for (int númer = 0; númer < 1500; númer++) 보낼것[númer] = (unsigned char)númer;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int lengd_VALUE = skrifa_skrá_gögn(gestur_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (lengd_VALUE <= 0) return 5;
        보낸수 += lengd_VALUE;
    }
    if (skrifa_skrá_gögn(gestur_VALUE, 보낼것, 1) != -1 || villa_númer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 TIL_BAKA_VALUE EOF가 된다. */
    loka_skrá(gestur_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int lengd_VALUE = 파일자료읽기(Tengjast, RECEIVED_vara + RECEIVED_COUNT, sizeof(RECEIVED_vara) - RECEIVED_COUNT);
        if (lengd_VALUE <= 0) return 7;
        RECEIVED_COUNT += lengd_VALUE;
    }
    for (int númer = 0; númer < RECEIVED_COUNT; númer++) if (RECEIVED_vara[númer] != 보낼것[númer]) return 8;
    if (파일자료읽기(Tengjast, RECEIVED_vara, 1) != 0) return 9;
    if (skrifa_skrá_gögn(Tengjast, 보낼것, 1) != -1 || villa_númer != 32) return 10;
    loka_skrá(Tengjast); loka_skrá(þjónn_VALUE);
    const char NIÐURSTAÐA[] = "C posix-kor 연결형 통신 PASS\n";
    skrifa_skrá_gögn(1, NIÐURSTAÐA, sizeof(NIÐURSTAÐA) - 1);
    return 0;
}
