#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define 확인(조건) do { if (!(조건)) { puts("POSIX UDP CHECK FAILED: " #조건); return 1; } } while (0)
int main(int 인수개수, char **인수목록) {
    확인(인수개수 == 2);
    int 접속번호 = 0;
    for (int 칸 = 0; 인수목록[1][칸]; 칸++) {
        확인(인수목록[1][칸] >= '0' && 인수목록[1][칸] <= '9');
        접속번호 = 접속번호 * 10 + 인수목록[1][칸] - '0';
        확인(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    확인(종단점 == 3);
    struct sockaddr_in 지역 = {0}, 상대 = {0}, 받은주소 = {0};
    지역.sin_family = AF_INET;
    socklen_t 길이 = sizeof 지역;
    확인(통신주소읽기(종단점, (struct sockaddr *)&지역, &길이) == 0 && 지역.sin_port == 0);
    확인(통신주소묶기(종단점, (struct sockaddr *)&지역, sizeof 지역) == 0);
    확인(통신주소읽기(종단점, (struct sockaddr *)&지역, &길이) == 0 && ntohs(지역.sin_port) >= 49152);
    확인(통신주소묶기(종단점, (struct sockaddr *)&지역, sizeof 지역) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    확인(bind(둘째, (struct sockaddr *)&지역, sizeof 지역) == -1 && errno == EADDRINUSE);
    확인(close(둘째) == 0);
    둘째 = dup(종단점);
    확인(close(종단점) == 0); 종단점 = 둘째;
    상대.sin_family = AF_INET; 상대.sin_port = 망차례짧은수(접속번호);
    확인(망주소해석하기(AF_INET, "10.0.2.2", &상대.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    확인(통신설정바꾸기(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char 자료[32];
    확인(자료전문받기(종단점, 자료, sizeof 자료, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&상대, sizeof 상대) == 9);
    길이 = sizeof 받은주소;
    확인(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    확인(자료전문받기(종단점, 자료, sizeof 자료, 0, (struct sockaddr *)&받은주소, &길이) == 9);
    확인(memcmp(자료, "posix-udp", 9) == 0 && 길이 == 16);
    확인(받은주소.sin_port == 상대.sin_port && 받은주소.sin_addr.s_addr == 상대.sin_addr.s_addr);
    확인(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&상대, sizeof 상대) == 8);
    확인(recvfrom(종단점, 자료, 3, 0, NULL, NULL) == 3 && memcmp(자료, "tru", 3) == 0);
    확인(recvfrom(종단점, 자료, sizeof 자료, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&상대, sizeof 상대) == 0);
    확인(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    확인(recvfrom(종단점, 자료, sizeof 자료, 0, NULL, NULL) == -1 && errno == EAGAIN);
    확인(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
