#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ƴeewtaade(ngonka) do { if (!(ngonka)) { puts("POSIX UDP CHECK FAILED: " #ngonka); return 1; } } while (0)
int main(int 인수개수, char **hujja_Doggol) {
    ƴeewtaade(인수개수 == 2);
    int 접속번호 = 0;
    for (int 칸 = 0; hujja_Doggol[1][칸]; 칸++) {
        ƴeewtaade(hujja_Doggol[1][칸] >= '0' && hujja_Doggol[1][칸] <= '9');
        접속번호 = 접속번호 * 10 + hujja_Doggol[1][칸] - '0';
        ƴeewtaade(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    ƴeewtaade(종단점 == 3);
    struct sockaddr_in nokkuwal_njaajeendi = {0}, giƴiraaɗo_njaru = {0}, 받은주소 = {0};
    nokkuwal_njaajeendi.sin_family = AF_INET;
    socklen_t njuuteendi_njaru = sizeof nokkuwal_njaajeendi;
    ƴeewtaade(통신주소읽기(종단점, (struct sockaddr *)&nokkuwal_njaajeendi, &njuuteendi_njaru) == 0 && nokkuwal_njaajeendi.sin_port == 0);
    ƴeewtaade(seŋondir_ñiiɓirde(종단점, (struct sockaddr *)&nokkuwal_njaajeendi, sizeof nokkuwal_njaajeendi) == 0);
    ƴeewtaade(통신주소읽기(종단점, (struct sockaddr *)&nokkuwal_njaajeendi, &njuuteendi_njaru) == 0 && ntohs(nokkuwal_njaajeendi.sin_port) >= 49152);
    ƴeewtaade(seŋondir_ñiiɓirde(종단점, (struct sockaddr *)&nokkuwal_njaajeendi, sizeof nokkuwal_njaajeendi) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ƴeewtaade(bind(둘째, (struct sockaddr *)&nokkuwal_njaajeendi, sizeof nokkuwal_njaajeendi) == -1 && errno == EADDRINUSE);
    ƴeewtaade(close(둘째) == 0);
    둘째 = dup(종단점);
    ƴeewtaade(close(종단점) == 0); 종단점 = 둘째;
    giƴiraaɗo_njaru.sin_family = AF_INET; giƴiraaɗo_njaru.sin_port = 망차례짧은수(접속번호);
    ƴeewtaade(망주소해석하기(AF_INET, "10.0.2.2", &giƴiraaɗo_njaru.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    ƴeewtaade(통신설정바꾸기(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char keɓe[32];
    ƴeewtaade(자료전문받기(종단점, keɓe, sizeof keɓe, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ƴeewtaade(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&giƴiraaɗo_njaru, sizeof giƴiraaɗo_njaru) == 9);
    njuuteendi_njaru = sizeof 받은주소;
    ƴeewtaade(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ƴeewtaade(자료전문받기(종단점, keɓe, sizeof keɓe, 0, (struct sockaddr *)&받은주소, &njuuteendi_njaru) == 9);
    ƴeewtaade(memcmp(keɓe, "posix-udp", 9) == 0 && njuuteendi_njaru == 16);
    ƴeewtaade(받은주소.sin_port == giƴiraaɗo_njaru.sin_port && 받은주소.sin_addr.s_addr == giƴiraaɗo_njaru.sin_addr.s_addr);
    ƴeewtaade(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&giƴiraaɗo_njaru, sizeof giƴiraaɗo_njaru) == 8);
    ƴeewtaade(recvfrom(종단점, keɓe, 3, 0, NULL, NULL) == 3 && memcmp(keɓe, "tru", 3) == 0);
    ƴeewtaade(recvfrom(종단점, keɓe, sizeof keɓe, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ƴeewtaade(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&giƴiraaɗo_njaru, sizeof giƴiraaɗo_njaru) == 0);
    ƴeewtaade(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    ƴeewtaade(recvfrom(종단점, keɓe, sizeof keɓe, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ƴeewtaade(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
