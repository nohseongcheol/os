#include "통신규약.h"

int START_kasutaja_programm(int Argumendid) {
    (void)Argumendid;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Pere = pilv_Pere;
    ADDRESS.pordinumber = 망차례짧은수(9260);
    ADDRESS.Interneti_aadress.ADDRESS_VALUE = võrk_täisarv(tagasisideaadress);
    int server_VALUE = avama_osaleja(pilv_Pere, voog_võrk, voog_transpordiprotokoll);
    if (server_VALUE < 0 || BIND_ADDRESS(server_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (aktsepteerima_võrguühendus(server_VALUE, 0, 0) != -1 || tõrke_number != 11) return 2;
    int külaline_VALUE = avama_osaleja(pilv_Pere, voog_võrk, voog_transpordiprotokoll);
    if (külaline_VALUE < 0 || Ühenda_võrk(külaline_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int Ühendu = aktsepteerima_võrguühendus(server_VALUE, 0, 0);
    if (Ühendu < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_kaup[1500];
    for (int number = 0; number < 1500; number++) 보낼것[number] = (unsigned char)number;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int 길이 = kirjutamine_Fail_andmed(külaline_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (길이 <= 0) return 5;
        보낸수 += 길이;
    }
    if (kirjutamine_Fail_andmed(külaline_VALUE, 보낼것, 1) != -1 || tõrke_number != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Tagasi_VALUE EOF가 된다. */
    Sule_Fail(külaline_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int 길이 = 파일자료읽기(Ühendu, RECEIVED_kaup + RECEIVED_COUNT, sizeof(RECEIVED_kaup) - RECEIVED_COUNT);
        if (길이 <= 0) return 7;
        RECEIVED_COUNT += 길이;
    }
    for (int number = 0; number < RECEIVED_COUNT; number++) if (RECEIVED_kaup[number] != 보낼것[number]) return 8;
    if (파일자료읽기(Ühendu, RECEIVED_kaup, 1) != 0) return 9;
    if (kirjutamine_Fail_andmed(Ühendu, 보낼것, 1) != -1 || tõrke_number != 32) return 10;
    Sule_Fail(Ühendu); Sule_Fail(server_VALUE);
    const char TULEMUS[] = "C posix-kor 연결형 통신 PASS\n";
    kirjutamine_Fail_andmed(1, TULEMUS, sizeof(TULEMUS) - 1);
    return 0;
}
