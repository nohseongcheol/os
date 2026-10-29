#include "통신규약.h"

int Bidu_utent_programm(int 인수) {
    (void)인수;
    struct 인터넷통신주소 ADDRESS = {0};
    ADDRESS.ADDRESS_Familja = cloud_Familja;
    ADDRESS.접속번호 = 망차례짧은수(9260);
    ADDRESS.indirizz_tal_Internet.ADDRESS_VALUE = netwerk_numru_sħiħ(되돌림주소);
    int server_VALUE = 통신종단점만들기(cloud_Familja, Stream_netwerk, 흐름전송규약);
    if (server_VALUE < 0 || BIND_ADDRESS(server_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (aċċetta_kumnikazzjoni_tan_netwerk(server_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int mistieden_VALUE = 통신종단점만들기(cloud_Familja, Stream_netwerk, 흐름전송규약);
    if (mistieden_VALUE < 0 || AQBAD_netwerk(mistieden_VALUE, (struct 통신주소 *)&ADDRESS, sizeof(ADDRESS)) < 0) return 3;
    int AQBAD = aċċetta_kumnikazzjoni_tan_netwerk(server_VALUE, 0, 0);
    if (AQBAD < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int tul_VALUE = kiteb_fajl_data(mistieden_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (tul_VALUE <= 0) return 5;
        보낸수 += tul_VALUE;
    }
    if (kiteb_fajl_data(mistieden_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Lura_VALUE EOF가 된다. */
    agħlaq_fajl(mistieden_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int tul_VALUE = 파일자료읽기(AQBAD, RECEIVED_element + RECEIVED_COUNT, sizeof(RECEIVED_element) - RECEIVED_COUNT);
        if (tul_VALUE <= 0) return 7;
        RECEIVED_COUNT += tul_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_element[수] != 보낼것[수]) return 8;
    if (파일자료읽기(AQBAD, RECEIVED_element, 1) != 0) return 9;
    if (kiteb_fajl_data(AQBAD, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    agħlaq_fajl(AQBAD); agħlaq_fajl(server_VALUE);
    const char miżura[] = "C posix-kor 연결형 통신 PASS\n";
    kiteb_fajl_data(1, miżura, sizeof(miżura) - 1);
    return 0;
}
