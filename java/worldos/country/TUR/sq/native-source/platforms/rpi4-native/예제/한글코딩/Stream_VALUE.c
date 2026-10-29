#include "통신규약.h"

int nis_përdorues_program(int Argumente) {
    (void)Argumente;
    struct 인터넷통신주소 email = {0};
    email.email_Familja = Internet_Familja;
    email.numri_i_portës = 망차례짧은수(9260);
    email.adresë_në_internet.email_VALUE = rrjet_numër_i_plotë(되돌림주소);
    int server_VALUE = 통신종단점만들기(Internet_Familja, Stream_rrjet, 흐름전송규약);
    if (server_VALUE < 0 || BIND_email(server_VALUE, (struct 통신주소 *)&email, sizeof(email)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (prano_lidhje_e_rrjetit(server_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int i_ftuar_VALUE = 통신종단점만들기(Internet_Familja, Stream_rrjet, 흐름전송규약);
    if (i_ftuar_VALUE < 0 || Lidh_rrjet(i_ftuar_VALUE, (struct 통신주소 *)&email, sizeof(email)) < 0) return 3;
    int Lidhu = prano_lidhje_e_rrjetit(server_VALUE, 0, 0);
    if (Lidhu < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_njësi[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int gjatësi_VALUE = shkruaj_skedar_të_dhëna(i_ftuar_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (gjatësi_VALUE <= 0) return 5;
        보낸수 += gjatësi_VALUE;
    }
    if (shkruaj_skedar_të_dhëna(i_ftuar_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 PAS_VALUE EOF가 된다. */
    mbyll_skedar(i_ftuar_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int gjatësi_VALUE = 파일자료읽기(Lidhu, RECEIVED_njësi + RECEIVED_COUNT, sizeof(RECEIVED_njësi) - RECEIVED_COUNT);
        if (gjatësi_VALUE <= 0) return 7;
        RECEIVED_COUNT += gjatësi_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_njësi[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Lidhu, RECEIVED_njësi, 1) != 0) return 9;
    if (shkruaj_skedar_të_dhëna(Lidhu, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    mbyll_skedar(Lidhu); mbyll_skedar(server_VALUE);
    const char llogaritje[] = "C posix-kor 연결형 통신 PASS\n";
    shkruaj_skedar_të_dhëna(1, llogaritje, sizeof(llogaritje) - 1);
    return 0;
}
