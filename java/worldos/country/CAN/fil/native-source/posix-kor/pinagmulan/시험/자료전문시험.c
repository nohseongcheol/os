#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define tiyakin_kumpirmahin(kondisyon) do { if (!(kondisyon)) { puts("POSIX UDP CHECK FAILED: " #kondisyon); return 1; } } while (0)
int main(int 인수개수, char **argumento_list) {
    tiyakin_kumpirmahin(인수개수 == 2);
    int numero_ng_port = 0;
    for (int espasyo_pagpasok = 0; argumento_list[1][espasyo_pagpasok]; espasyo_pagpasok++) {
        tiyakin_kumpirmahin(argumento_list[1][espasyo_pagpasok] >= '0' && argumento_list[1][espasyo_pagpasok] <= '9');
        numero_ng_port = numero_ng_port * 10 + argumento_list[1][espasyo_pagpasok] - '0';
        tiyakin_kumpirmahin(numero_ng_port <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    tiyakin_kumpirmahin(종단점 == 3);
    struct sockaddr_in lokal_lawak = {0}, peer_VALUE = {0}, RECEIVED_email = {0};
    lokal_lawak.sin_family = AF_INET;
    socklen_t haba_VALUE = sizeof lokal_lawak;
    tiyakin_kumpirmahin(통신주소읽기(종단점, (struct sockaddr *)&lokal_lawak, &haba_VALUE) == 0 && lokal_lawak.sin_port == 0);
    tiyakin_kumpirmahin(BIND_email(종단점, (struct sockaddr *)&lokal_lawak, sizeof lokal_lawak) == 0);
    tiyakin_kumpirmahin(통신주소읽기(종단점, (struct sockaddr *)&lokal_lawak, &haba_VALUE) == 0 && ntohs(lokal_lawak.sin_port) >= 49152);
    tiyakin_kumpirmahin(BIND_email(종단점, (struct sockaddr *)&lokal_lawak, sizeof lokal_lawak) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    tiyakin_kumpirmahin(bind(둘째, (struct sockaddr *)&lokal_lawak, sizeof lokal_lawak) == -1 && errno == EADDRINUSE);
    tiyakin_kumpirmahin(close(둘째) == 0);
    둘째 = dup(종단점);
    tiyakin_kumpirmahin(close(종단점) == 0); 종단점 = 둘째;
    peer_VALUE.sin_family = AF_INET; peer_VALUE.sin_port = 망차례짧은수(numero_ng_port);
    tiyakin_kumpirmahin(mag_parse_Network_email(AF_INET, "10.0.2.2", &peer_VALUE.sin_addr) == 1);
    struct timeval maghintay_VALUE = {0, 200000};
    tiyakin_kumpirmahin(baguhin_Network_Mga_Setting(종단점, SOL_SOCKET, SO_RCVTIMEO, &maghintay_VALUE, sizeof maghintay_VALUE) == 0);
    char data[32];
    tiyakin_kumpirmahin(자료전문받기(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tiyakin_kumpirmahin(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 9);
    haba_VALUE = sizeof RECEIVED_email;
    tiyakin_kumpirmahin(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    tiyakin_kumpirmahin(자료전문받기(종단점, data, sizeof data, 0, (struct sockaddr *)&RECEIVED_email, &haba_VALUE) == 9);
    tiyakin_kumpirmahin(memcmp(data, "posix-udp", 9) == 0 && haba_VALUE == 16);
    tiyakin_kumpirmahin(RECEIVED_email.sin_port == peer_VALUE.sin_port && RECEIVED_email.sin_addr.s_addr == peer_VALUE.sin_addr.s_addr);
    tiyakin_kumpirmahin(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 8);
    tiyakin_kumpirmahin(recvfrom(종단점, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    tiyakin_kumpirmahin(recvfrom(종단점, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    tiyakin_kumpirmahin(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&peer_VALUE, sizeof peer_VALUE) == 0);
    tiyakin_kumpirmahin(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    tiyakin_kumpirmahin(recvfrom(종단점, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    tiyakin_kumpirmahin(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
