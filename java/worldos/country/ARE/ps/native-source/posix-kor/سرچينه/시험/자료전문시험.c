#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define 확인(آړ) do { if (!(آړ)) { puts("POSIX UDP CHECK FAILED: " #آړ); return 1; } } while (0)
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
    struct sockaddr_in 지역 = {0}, جوړه_ارزښت = {0}, 받은주소 = {0};
    지역.sin_family = AF_INET;
    socklen_t اوږدوالى_ارزښت = sizeof 지역;
    확인(통신주소읽기(종단점, (struct sockaddr *)&지역, &اوږدوالى_ارزښت) == 0 && 지역.sin_port == 0);
    확인(اړه_لري_پته(종단점, (struct sockaddr *)&지역, sizeof 지역) == 0);
    확인(통신주소읽기(종단점, (struct sockaddr *)&지역, &اوږدوالى_ارزښت) == 0 && ntohs(지역.sin_port) >= 49152);
    확인(اړه_لري_پته(종단점, (struct sockaddr *)&지역, sizeof 지역) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    확인(bind(둘째, (struct sockaddr *)&지역, sizeof 지역) == -1 && errno == EADDRINUSE);
    확인(close(둘째) == 0);
    둘째 = dup(종단점);
    확인(close(종단점) == 0); 종단점 = 둘째;
    جوړه_ارزښت.sin_family = AF_INET; جوړه_ارزښت.sin_port = 망차례짧은수(접속번호);
    확인(تجزیه_جال_پته(AF_INET, "10.0.2.2", &جوړه_ارزښت.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    확인(통신설정바꾸기(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char اومتوک[32];
    확인(자료전문받기(종단점, اومتوک, sizeof اومتوک, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&جوړه_ارزښت, sizeof جوړه_ارزښت) == 9);
    اوږدوالى_ارزښت = sizeof 받은주소;
    확인(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    확인(자료전문받기(종단점, اومتوک, sizeof اومتوک, 0, (struct sockaddr *)&받은주소, &اوږدوالى_ارزښت) == 9);
    확인(memcmp(اومتوک, "posix-udp", 9) == 0 && اوږدوالى_ارزښت == 16);
    확인(받은주소.sin_port == جوړه_ارزښت.sin_port && 받은주소.sin_addr.s_addr == جوړه_ارزښت.sin_addr.s_addr);
    확인(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&جوړه_ارزښت, sizeof جوړه_ارزښت) == 8);
    확인(recvfrom(종단점, اومتوک, 3, 0, NULL, NULL) == 3 && memcmp(اومتوک, "tru", 3) == 0);
    확인(recvfrom(종단점, اومتوک, sizeof اومتوک, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    확인(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&جوړه_ارزښت, sizeof جوړه_ارزښت) == 0);
    확인(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    확인(recvfrom(종단점, اومتوک, sizeof اومتوک, 0, NULL, NULL) == -1 && errno == EAGAIN);
    확인(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
