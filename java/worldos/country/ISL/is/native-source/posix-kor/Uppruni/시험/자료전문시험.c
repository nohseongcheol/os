#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define sannprófa(skilyrði) do { if (!(skilyrði)) { puts("POSIX UDP CHECK FAILED: " #skilyrði); return 1; } } while (0)
int main(int 인수개수, char **frumbreyta_Listi) {
    sannprófa(인수개수 == 2);
    int tengisnúmer = 0;
    for (int rauf_færsla = 0; frumbreyta_Listi[1][rauf_færsla]; rauf_færsla++) {
        sannprófa(frumbreyta_Listi[1][rauf_færsla] >= '0' && frumbreyta_Listi[1][rauf_færsla] <= '9');
        tengisnúmer = tengisnúmer * 10 + frumbreyta_Listi[1][rauf_færsla] - '0';
        sannprófa(tengisnúmer <= 65535);
    }
    int endastöð_VALUE = stofna_endastöð(AF_INET, SOCK_DGRAM, 0);
    sannprófa(endastöð_VALUE == 3);
    struct sockaddr_in staðbundið_umfang = {0}, jafningi_VALUE = {0}, RECEIVED_slóð = {0};
    staðbundið_umfang.sin_family = AF_INET;
    socklen_t lengd_VALUE = sizeof staðbundið_umfang;
    sannprófa(통신주소읽기(endastöð_VALUE, (struct sockaddr *)&staðbundið_umfang, &lengd_VALUE) == 0 && staðbundið_umfang.sin_port == 0);
    sannprófa(BIND_slóð(endastöð_VALUE, (struct sockaddr *)&staðbundið_umfang, sizeof staðbundið_umfang) == 0);
    sannprófa(통신주소읽기(endastöð_VALUE, (struct sockaddr *)&staðbundið_umfang, &lengd_VALUE) == 0 && ntohs(staðbundið_umfang.sin_port) >= 49152);
    sannprófa(BIND_slóð(endastöð_VALUE, (struct sockaddr *)&staðbundið_umfang, sizeof staðbundið_umfang) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    sannprófa(bind(둘째, (struct sockaddr *)&staðbundið_umfang, sizeof staðbundið_umfang) == -1 && errno == EADDRINUSE);
    sannprófa(close(둘째) == 0);
    둘째 = dup(endastöð_VALUE);
    sannprófa(close(endastöð_VALUE) == 0); endastöð_VALUE = 둘째;
    jafningi_VALUE.sin_family = AF_INET; jafningi_VALUE.sin_port = 망차례짧은수(tengisnúmer);
    sannprófa(þátta_Net_slóð(AF_INET, "10.0.2.2", &jafningi_VALUE.sin_addr) == 1);
    struct timeval Bíddu_VALUE = {0, 200000};
    sannprófa(breyta_Net_Stillingar(endastöð_VALUE, SOL_SOCKET, SO_RCVTIMEO, &Bíddu_VALUE, sizeof Bíddu_VALUE) == 0);
    char gögn[32];
    sannprófa(자료전문받기(endastöð_VALUE, gögn, sizeof gögn, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    sannprófa(자료전문보내기(endastöð_VALUE, "posix-udp", 9, 0, (struct sockaddr *)&jafningi_VALUE, sizeof jafningi_VALUE) == 9);
    lengd_VALUE = sizeof RECEIVED_slóð;
    sannprófa(recvfrom(endastöð_VALUE, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    sannprófa(자료전문받기(endastöð_VALUE, gögn, sizeof gögn, 0, (struct sockaddr *)&RECEIVED_slóð, &lengd_VALUE) == 9);
    sannprófa(memcmp(gögn, "posix-udp", 9) == 0 && lengd_VALUE == 16);
    sannprófa(RECEIVED_slóð.sin_port == jafningi_VALUE.sin_port && RECEIVED_slóð.sin_addr.s_addr == jafningi_VALUE.sin_addr.s_addr);
    sannprófa(sendto(endastöð_VALUE, "truncate", 8, 0, (struct sockaddr *)&jafningi_VALUE, sizeof jafningi_VALUE) == 8);
    sannprófa(recvfrom(endastöð_VALUE, gögn, 3, 0, NULL, NULL) == 3 && memcmp(gögn, "tru", 3) == 0);
    sannprófa(recvfrom(endastöð_VALUE, gögn, sizeof gögn, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    sannprófa(sendto(endastöð_VALUE, NULL, 0, 0, (struct sockaddr *)&jafningi_VALUE, sizeof jafningi_VALUE) == 0);
    sannprófa(recvfrom(endastöð_VALUE, NULL, 0, 0, NULL, NULL) == 0);
    sannprófa(recvfrom(endastöð_VALUE, gögn, sizeof gögn, 0, NULL, NULL) == -1 && errno == EAGAIN);
    sannprófa(close(endastöð_VALUE) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
