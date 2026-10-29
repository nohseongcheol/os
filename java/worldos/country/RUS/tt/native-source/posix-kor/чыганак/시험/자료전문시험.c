#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define раслау(шарт) do { if (!(шарт)) { puts("POSIX UDP CHECK FAILED: " #шарт); return 1; } } while (0)
int main(int 인수개수, char **аргумент_Исемлек) {
    раслау(인수개수 == 2);
    int 접속번호 = 0;
    for (int оя_кертү = 0; аргумент_Исемлек[1][оя_кертү]; оя_кертү++) {
        раслау(аргумент_Исемлек[1][оя_кертү] >= '0' && аргумент_Исемлек[1][оя_кертү] <= '9');
        접속번호 = 접속번호 * 10 + аргумент_Исемлек[1][оя_кертү] - '0';
        раслау(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    раслау(종단점 == 3);
    struct sockaddr_in локаль_даирә = {0}, тиңдәш_VALUE = {0}, RECEIVED_адрес = {0};
    локаль_даирә.sin_family = AF_INET;
    socklen_t озынлык_VALUE = sizeof локаль_даирә;
    раслау(통신주소읽기(종단점, (struct sockaddr *)&локаль_даирә, &озынлык_VALUE) == 0 && локаль_даирә.sin_port == 0);
    раслау(BIND_адрес(종단점, (struct sockaddr *)&локаль_даирә, sizeof локаль_даирә) == 0);
    раслау(통신주소읽기(종단점, (struct sockaddr *)&локаль_даирә, &озынлык_VALUE) == 0 && ntohs(локаль_даирә.sin_port) >= 49152);
    раслау(BIND_адрес(종단점, (struct sockaddr *)&локаль_даирә, sizeof локаль_даирә) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    раслау(bind(둘째, (struct sockaddr *)&локаль_даирә, sizeof локаль_даирә) == -1 && errno == EADDRINUSE);
    раслау(close(둘째) == 0);
    둘째 = dup(종단점);
    раслау(close(종단점) == 0); 종단점 = 둘째;
    тиңдәш_VALUE.sin_family = AF_INET; тиңдәш_VALUE.sin_port = 망차례짧은수(접속번호);
    раслау(бүлү_Челтәр_адрес(AF_INET, "10.0.2.2", &тиңдәш_VALUE.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    раслау(үзгәртү_Челтәр_Параметрлар(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char мәгълүмат[32];
    раслау(자료전문받기(종단점, мәгълүмат, sizeof мәгълүмат, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    раслау(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&тиңдәш_VALUE, sizeof тиңдәш_VALUE) == 9);
    озынлык_VALUE = sizeof RECEIVED_адрес;
    раслау(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    раслау(자료전문받기(종단점, мәгълүмат, sizeof мәгълүмат, 0, (struct sockaddr *)&RECEIVED_адрес, &озынлык_VALUE) == 9);
    раслау(memcmp(мәгълүмат, "posix-udp", 9) == 0 && озынлык_VALUE == 16);
    раслау(RECEIVED_адрес.sin_port == тиңдәш_VALUE.sin_port && RECEIVED_адрес.sin_addr.s_addr == тиңдәш_VALUE.sin_addr.s_addr);
    раслау(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&тиңдәш_VALUE, sizeof тиңдәш_VALUE) == 8);
    раслау(recvfrom(종단점, мәгълүмат, 3, 0, NULL, NULL) == 3 && memcmp(мәгълүмат, "tru", 3) == 0);
    раслау(recvfrom(종단점, мәгълүмат, sizeof мәгълүмат, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    раслау(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&тиңдәш_VALUE, sizeof тиңдәш_VALUE) == 0);
    раслау(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    раслау(recvfrom(종단점, мәгълүмат, sizeof мәгълүмат, 0, NULL, NULL) == -1 && errno == EAGAIN);
    раслау(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
