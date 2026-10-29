#include "통신규약.h"

int Start_gumagamit_app(int 인수) {
    (void)인수;
    struct 인터넷통신주소 email = {0};
    email.email_Pamilya = cloud_Pamilya;
    email.numero_ng_port = 망차례짧은수(9260);
    email.Internet_address.email_VALUE = Network_integer_buong_numero(되돌림주소);
    int server_VALUE = 통신종단점만들기(cloud_Pamilya, Stream_Network, 흐름전송규약);
    if (server_VALUE < 0 || BIND_email(server_VALUE, (struct 통신주소 *)&email, sizeof(email)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (tanggapin_koneksyon_sa_network(server_VALUE, 0, 0) != -1 || 오류번호 != 11) return 2;
    int bisita_VALUE = 통신종단점만들기(cloud_Pamilya, Stream_Network, 흐름전송규약);
    if (bisita_VALUE < 0 || CONNECT_Network(bisita_VALUE, (struct 통신주소 *)&email, sizeof(email)) < 0) return 3;
    int CONNECT = tanggapin_koneksyon_sa_network(server_VALUE, 0, 0);
    if (CONNECT < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_item[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int haba_VALUE = sumulat_file_data(bisita_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (haba_VALUE <= 0) return 5;
        보낸수 += haba_VALUE;
    }
    if (sumulat_file_data(bisita_VALUE, 보낼것, 1) != -1 || 오류번호 != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 Bumalik_VALUE EOF가 된다. */
    isara_file(bisita_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int haba_VALUE = 파일자료읽기(CONNECT, RECEIVED_item + RECEIVED_COUNT, sizeof(RECEIVED_item) - RECEIVED_COUNT);
        if (haba_VALUE <= 0) return 7;
        RECEIVED_COUNT += haba_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_item[수] != 보낼것[수]) return 8;
    if (파일자료읽기(CONNECT, RECEIVED_item, 1) != 0) return 9;
    if (sumulat_file_data(CONNECT, 보낼것, 1) != -1 || 오류번호 != 32) return 10;
    isara_file(CONNECT); isara_file(server_VALUE);
    const char sukat[] = "C posix-kor 연결형 통신 PASS\n";
    sumulat_file_data(1, sukat, sizeof(sukat) - 1);
    return 0;
}
