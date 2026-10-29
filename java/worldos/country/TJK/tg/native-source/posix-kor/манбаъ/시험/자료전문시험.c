#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define тасдиқ_кардан(шарт) do { if (!(шарт)) { puts("POSIX UDP CHECK FAILED: " #шарт); return 1; } } while (0)
int main(int 인수개수, char **аргумент_Рӯйхат) {
    тасдиқ_кардан(인수개수 == 2);
    int 접속번호 = 0;
    for (int ковокӣ_ворида = 0; аргумент_Рӯйхат[1][ковокӣ_ворида]; ковокӣ_ворида++) {
        тасдиқ_кардан(аргумент_Рӯйхат[1][ковокӣ_ворида] >= '0' && аргумент_Рӯйхат[1][ковокӣ_ворида] <= '9');
        접속번호 = 접속번호 * 10 + аргумент_Рӯйхат[1][ковокӣ_ворида] - '0';
        тасдиқ_кардан(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    тасдиқ_кардан(종단점 == 3);
    struct sockaddr_in маҳаллӣ_ҳаҷм = {0}, ҳамсон_қимат = {0}, 받은주소 = {0};
    маҳаллӣ_ҳаҷм.sin_family = AF_INET;
    socklen_t дарозӣ_қимат = sizeof маҳаллӣ_ҳаҷм;
    тасдиқ_кардан(통신주소읽기(종단점, (struct sockaddr *)&маҳаллӣ_ҳаҷм, &дарозӣ_қимат) == 0 && маҳаллӣ_ҳаҷм.sin_port == 0);
    тасдиқ_кардан(иртибот_додан_суроға(종단점, (struct sockaddr *)&маҳаллӣ_ҳаҷм, sizeof маҳаллӣ_ҳаҷм) == 0);
    тасдиқ_кардан(통신주소읽기(종단점, (struct sockaddr *)&маҳаллӣ_ҳаҷм, &дарозӣ_қимат) == 0 && ntohs(маҳаллӣ_ҳаҷм.sin_port) >= 49152);
    тасдиқ_кардан(иртибот_додан_суроға(종단점, (struct sockaddr *)&маҳаллӣ_ҳаҷм, sizeof маҳаллӣ_ҳаҷм) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    тасдиқ_кардан(bind(둘째, (struct sockaddr *)&маҳаллӣ_ҳаҷм, sizeof маҳаллӣ_ҳаҷм) == -1 && errno == EADDRINUSE);
    тасдиқ_кардан(close(둘째) == 0);
    둘째 = dup(종단점);
    тасдиқ_кардан(close(종단점) == 0); 종단점 = 둘째;
    ҳамсон_қимат.sin_family = AF_INET; ҳамсон_қимат.sin_port = 망차례짧은수(접속번호);
    тасдиқ_кардан(망주소해석하기(AF_INET, "10.0.2.2", &ҳамсон_қимат.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    тасдиқ_кардан(тағйир_додан_Шабака_Танзимот(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char иттилоот[32];
    тасдиқ_кардан(자료전문받기(종단점, иттилоот, sizeof иттилоот, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    тасдиқ_кардан(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ҳамсон_қимат, sizeof ҳамсон_қимат) == 9);
    дарозӣ_қимат = sizeof 받은주소;
    тасдиқ_кардан(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    тасдиқ_кардан(자료전문받기(종단점, иттилоот, sizeof иттилоот, 0, (struct sockaddr *)&받은주소, &дарозӣ_қимат) == 9);
    тасдиқ_кардан(memcmp(иттилоот, "posix-udp", 9) == 0 && дарозӣ_қимат == 16);
    тасдиқ_кардан(받은주소.sin_port == ҳамсон_қимат.sin_port && 받은주소.sin_addr.s_addr == ҳамсон_қимат.sin_addr.s_addr);
    тасдиқ_кардан(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ҳамсон_қимат, sizeof ҳамсон_қимат) == 8);
    тасдиқ_кардан(recvfrom(종단점, иттилоот, 3, 0, NULL, NULL) == 3 && memcmp(иттилоот, "tru", 3) == 0);
    тасдиқ_кардан(recvfrom(종단점, иттилоот, sizeof иттилоот, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    тасдиқ_кардан(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ҳамсон_қимат, sizeof ҳамсон_қимат) == 0);
    тасдиқ_кардан(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    тасдиқ_кардан(recvfrom(종단점, иттилоот, sizeof иттилоот, 0, NULL, NULL) == -1 && errno == EAGAIN);
    тасдиқ_кардан(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
