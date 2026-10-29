#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define провери(услов) do { if (!(услов)) { puts("POSIX UDP CHECK FAILED: " #услов); return 1; } } while (0)
int main(int 인수개수, char **аргумент_Список) {
    провери(인수개수 == 2);
    int број_на_порта = 0;
    for (int отвор_внес = 0; аргумент_Список[1][отвор_внес]; отвор_внес++) {
        провери(аргумент_Список[1][отвор_внес] >= '0' && аргумент_Список[1][отвор_внес] <= '9');
        број_на_порта = број_на_порта * 10 + аргумент_Список[1][отвор_внес] - '0';
        провери(број_на_порта <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    провери(종단점 == 3);
    struct sockaddr_in локален_обем = {0}, рамноправен_уред_VALUE = {0}, RECEIVED_адреса = {0};
    локален_обем.sin_family = AF_INET;
    socklen_t должина_VALUE = sizeof локален_обем;
    провери(통신주소읽기(종단점, (struct sockaddr *)&локален_обем, &должина_VALUE) == 0 && локален_обем.sin_port == 0);
    провери(БИНД_адреса(종단점, (struct sockaddr *)&локален_обем, sizeof локален_обем) == 0);
    провери(통신주소읽기(종단점, (struct sockaddr *)&локален_обем, &должина_VALUE) == 0 && ntohs(локален_обем.sin_port) >= 49152);
    провери(БИНД_адреса(종단점, (struct sockaddr *)&локален_обем, sizeof локален_обем) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    провери(bind(둘째, (struct sockaddr *)&локален_обем, sizeof локален_обем) == -1 && errno == EADDRINUSE);
    провери(close(둘째) == 0);
    둘째 = dup(종단점);
    провери(close(종단점) == 0); 종단점 = 둘째;
    рамноправен_уред_VALUE.sin_family = AF_INET; рамноправен_уред_VALUE.sin_port = 망차례짧은수(број_на_порта);
    провери(разложи_Мрежа_адреса(AF_INET, "10.0.2.2", &рамноправен_уред_VALUE.sin_addr) == 1);
    struct timeval почекај_VALUE = {0, 200000};
    провери(измени_Мрежа_Параметри(종단점, SOL_SOCKET, SO_RCVTIMEO, &почекај_VALUE, sizeof почекај_VALUE) == 0);
    char податоци[32];
    провери(자료전문받기(종단점, податоци, sizeof податоци, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    провери(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&рамноправен_уред_VALUE, sizeof рамноправен_уред_VALUE) == 9);
    должина_VALUE = sizeof RECEIVED_адреса;
    провери(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    провери(자료전문받기(종단점, податоци, sizeof податоци, 0, (struct sockaddr *)&RECEIVED_адреса, &должина_VALUE) == 9);
    провери(memcmp(податоци, "posix-udp", 9) == 0 && должина_VALUE == 16);
    провери(RECEIVED_адреса.sin_port == рамноправен_уред_VALUE.sin_port && RECEIVED_адреса.sin_addr.s_addr == рамноправен_уред_VALUE.sin_addr.s_addr);
    провери(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&рамноправен_уред_VALUE, sizeof рамноправен_уред_VALUE) == 8);
    провери(recvfrom(종단점, податоци, 3, 0, NULL, NULL) == 3 && memcmp(податоци, "tru", 3) == 0);
    провери(recvfrom(종단점, податоци, sizeof податоци, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    провери(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&рамноправен_уред_VALUE, sizeof рамноправен_уред_VALUE) == 0);
    провери(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    провери(recvfrom(종단점, податоци, sizeof податоци, 0, NULL, NULL) == -1 && errno == EAGAIN);
    провери(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
