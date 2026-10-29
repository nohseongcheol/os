#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define যাচাই_করা(শর্ত) do { if (!(শর্ত)) { puts("POSIX UDP CHECK FAILED: " #শর্ত); return 1; } } while (0)
int main(int 인수개수, char **যুক্তি_তালিকা) {
    যাচাই_করা(인수개수 == 2);
    int পোর্ট_নম্বর = 0;
    for (int স্লট_ভুক্তি = 0; যুক্তি_তালিকা[1][স্লট_ভুক্তি]; স্লট_ভুক্তি++) {
        যাচাই_করা(যুক্তি_তালিকা[1][স্লট_ভুক্তি] >= '0' && যুক্তি_তালিকা[1][স্লট_ভুক্তি] <= '9');
        পোর্ট_নম্বর = পোর্ট_নম্বর * 10 + যুক্তি_তালিকা[1][স্লট_ভুক্তি] - '0';
        যাচাই_করা(পোর্ট_নম্বর <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    যাচাই_করা(종단점 == 3);
    struct sockaddr_in স্থানীয়_সুযোগ = {0}, পিয়ার_মান = {0}, 받은주소 = {0};
    স্থানীয়_সুযোগ.sin_family = AF_INET;
    socklen_t দৈর্ঘ্য_মান = sizeof স্থানীয়_সুযোগ;
    যাচাই_করা(통신주소읽기(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, &দৈর্ঘ্য_মান) == 0 && স্থানীয়_সুযোগ.sin_port == 0);
    যাচাই_করা(বন্ধন_করা_ইমেইল(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, sizeof স্থানীয়_সুযোগ) == 0);
    যাচাই_করা(통신주소읽기(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, &দৈর্ঘ্য_মান) == 0 && ntohs(স্থানীয়_সুযোগ.sin_port) >= 49152);
    যাচাই_করা(বন্ধন_করা_ইমেইল(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, sizeof স্থানীয়_সুযোগ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    যাচাই_করা(bind(둘째, (struct sockaddr *)&স্থানীয়_সুযোগ, sizeof স্থানীয়_সুযোগ) == -1 && errno == EADDRINUSE);
    যাচাই_করা(close(둘째) == 0);
    둘째 = dup(종단점);
    যাচাই_করা(close(종단점) == 0); 종단점 = 둘째;
    পিয়ার_মান.sin_family = AF_INET; পিয়ার_মান.sin_port = 망차례짧은수(পোর্ট_নম্বর);
    যাচাই_করা(বিভাজন_করা_নেটওয়ার্ক_ইমেইল(AF_INET, "10.0.2.2", &পিয়ার_মান.sin_addr) == 1);
    struct timeval অপেক্ষা_মান = {0, 200000};
    যাচাই_করা(পরিবর্তন_করা_নেটওয়ার্ক_সেটিংস(종단점, SOL_SOCKET, SO_RCVTIMEO, &অপেক্ষা_মান, sizeof অপেক্ষা_মান) == 0);
    char ডাটা[32];
    যাচাই_করা(자료전문받기(종단점, ডাটা, sizeof ডাটা, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    যাচাই_করা(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&পিয়ার_মান, sizeof পিয়ার_মান) == 9);
    দৈর্ঘ্য_মান = sizeof 받은주소;
    যাচাই_করা(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    যাচাই_করা(자료전문받기(종단점, ডাটা, sizeof ডাটা, 0, (struct sockaddr *)&받은주소, &দৈর্ঘ্য_মান) == 9);
    যাচাই_করা(memcmp(ডাটা, "posix-udp", 9) == 0 && দৈর্ঘ্য_মান == 16);
    যাচাই_করা(받은주소.sin_port == পিয়ার_মান.sin_port && 받은주소.sin_addr.s_addr == পিয়ার_মান.sin_addr.s_addr);
    যাচাই_করা(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&পিয়ার_মান, sizeof পিয়ার_মান) == 8);
    যাচাই_করা(recvfrom(종단점, ডাটা, 3, 0, NULL, NULL) == 3 && memcmp(ডাটা, "tru", 3) == 0);
    যাচাই_করা(recvfrom(종단점, ডাটা, sizeof ডাটা, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    যাচাই_করা(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&পিয়ার_মান, sizeof পিয়ার_মান) == 0);
    যাচাই_করা(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    যাচাই_করা(recvfrom(종단점, ডাটা, sizeof ডাটা, 0, NULL, NULL) == -1 && errno == EAGAIN);
    যাচাই_করা(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
