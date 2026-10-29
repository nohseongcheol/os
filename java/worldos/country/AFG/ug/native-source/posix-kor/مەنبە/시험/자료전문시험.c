#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define دەلىللىمەك(شەرت) do { if (!(شەرت)) { puts("POSIX UDP CHECK FAILED: " #شەرت); return 1; } } while (0)
int main(int 인수개수, char **دەلىل_تىزىم) {
    دەلىللىمەك(인수개수 == 2);
    int 접속번호 = 0;
    for (int ئوقۇر_كىرگۈزۈش = 0; دەلىل_تىزىم[1][ئوقۇر_كىرگۈزۈش]; ئوقۇر_كىرگۈزۈش++) {
        دەلىللىمەك(دەلىل_تىزىم[1][ئوقۇر_كىرگۈزۈش] >= '0' && دەلىل_تىزىم[1][ئوقۇر_كىرگۈزۈش] <= '9');
        접속번호 = 접속번호 * 10 + دەلىل_تىزىم[1][ئوقۇر_كىرگۈزۈش] - '0';
        دەلىللىمەك(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    دەلىللىمەك(종단점 == 3);
    struct sockaddr_in يەرلىك_بوشلۇق = {0}, باراۋەرلىك_قىممىتى = {0}, 받은주소 = {0};
    يەرلىك_بوشلۇق.sin_family = AF_INET;
    socklen_t ئۇزۇنلۇق_قىممىتى = sizeof يەرلىك_بوشلۇق;
    دەلىللىمەك(통신주소읽기(종단점, (struct sockaddr *)&يەرلىك_بوشلۇق, &ئۇزۇنلۇق_قىممىتى) == 0 && يەرلىك_بوشلۇق.sin_port == 0);
    دەلىللىمەك(باغلاش_ئادرېس(종단점, (struct sockaddr *)&يەرلىك_بوشلۇق, sizeof يەرلىك_بوشلۇق) == 0);
    دەلىللىمەك(통신주소읽기(종단점, (struct sockaddr *)&يەرلىك_بوشلۇق, &ئۇزۇنلۇق_قىممىتى) == 0 && ntohs(يەرلىك_بوشلۇق.sin_port) >= 49152);
    دەلىللىمەك(باغلاش_ئادرېس(종단점, (struct sockaddr *)&يەرلىك_بوشلۇق, sizeof يەرلىك_بوشلۇق) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    دەلىللىمەك(bind(둘째, (struct sockaddr *)&يەرلىك_بوشلۇق, sizeof يەرلىك_بوشلۇق) == -1 && errno == EADDRINUSE);
    دەلىللىمەك(close(둘째) == 0);
    둘째 = dup(종단점);
    دەلىللىمەك(close(종단점) == 0); 종단점 = 둘째;
    باراۋەرلىك_قىممىتى.sin_family = AF_INET; باراۋەرلىك_قىممىتى.sin_port = 망차례짧은수(접속번호);
    دەلىللىمەك(망주소해석하기(AF_INET, "10.0.2.2", &باراۋەرلىك_قىممىتى.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    دەلىللىمەك(ئۆزگەرتمەك_تور_تەڭشەك(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char مەلۇمات[32];
    دەلىللىمەك(자료전문받기(종단점, مەلۇمات, sizeof مەلۇمات, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    دەلىللىمەك(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&باراۋەرلىك_قىممىتى, sizeof باراۋەرلىك_قىممىتى) == 9);
    ئۇزۇنلۇق_قىممىتى = sizeof 받은주소;
    دەلىللىمەك(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    دەلىللىمەك(자료전문받기(종단점, مەلۇمات, sizeof مەلۇمات, 0, (struct sockaddr *)&받은주소, &ئۇزۇنلۇق_قىممىتى) == 9);
    دەلىللىمەك(memcmp(مەلۇمات, "posix-udp", 9) == 0 && ئۇزۇنلۇق_قىممىتى == 16);
    دەلىللىمەك(받은주소.sin_port == باراۋەرلىك_قىممىتى.sin_port && 받은주소.sin_addr.s_addr == باراۋەرلىك_قىممىتى.sin_addr.s_addr);
    دەلىللىمەك(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&باراۋەرلىك_قىممىتى, sizeof باراۋەرلىك_قىممىتى) == 8);
    دەلىللىمەك(recvfrom(종단점, مەلۇمات, 3, 0, NULL, NULL) == 3 && memcmp(مەلۇمات, "tru", 3) == 0);
    دەلىللىمەك(recvfrom(종단점, مەلۇمات, sizeof مەلۇمات, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    دەلىللىمەك(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&باراۋەرلىك_قىممىتى, sizeof باراۋەرلىك_قىممىتى) == 0);
    دەلىللىمەك(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    دەلىللىمەك(recvfrom(종단점, مەلۇمات, sizeof مەلۇمات, 0, NULL, NULL) == -1 && errno == EAGAIN);
    دەلىللىمەك(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
