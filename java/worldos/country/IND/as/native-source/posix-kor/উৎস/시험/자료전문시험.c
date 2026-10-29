#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define প্ৰমাণিত_কৰক(চৰ্ত) do { if (!(চৰ্ত)) { puts("POSIX UDP CHECK FAILED: " #চৰ্ত); return 1; } } while (0)
int main(int 인수개수, char **যুক্তি_সূচী) {
    প্ৰমাণিত_কৰক(인수개수 == 2);
    int 접속번호 = 0;
    for (int শ্লট_প্রবিষ্ট = 0; যুক্তি_সূচী[1][শ্লট_প্রবিষ্ট]; শ্লট_প্রবিষ্ট++) {
        প্ৰমাণিত_কৰক(যুক্তি_সূচী[1][শ্লট_প্রবিষ্ট] >= '0' && যুক্তি_সূচী[1][শ্লট_প্রবিষ্ট] <= '9');
        접속번호 = 접속번호 * 10 + যুক্তি_সূচী[1][শ্লট_প্রবিষ্ট] - '0';
        প্ৰমাণিত_কৰক(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    প্ৰমাণিত_কৰক(종단점 == 3);
    struct sockaddr_in স্থানীয়_সুযোগ = {0}, পীয়েৰ_মান = {0}, 받은주소 = {0};
    স্থানীয়_সুযোগ.sin_family = AF_INET;
    socklen_t দৈর্ঘ্য_মান = sizeof স্থানীয়_সুযোগ;
    প্ৰমাণিত_কৰক(통신주소읽기(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, &দৈর্ঘ্য_মান) == 0 && স্থানীয়_সুযোগ.sin_port == 0);
    প্ৰমাণিত_কৰক(বান্ধক_ঠিকনা(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, sizeof স্থানীয়_সুযোগ) == 0);
    প্ৰমাণিত_কৰক(통신주소읽기(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, &দৈর্ঘ্য_মান) == 0 && ntohs(স্থানীয়_সুযোগ.sin_port) >= 49152);
    প্ৰমাণিত_কৰক(বান্ধক_ঠিকনা(종단점, (struct sockaddr *)&স্থানীয়_সুযোগ, sizeof স্থানীয়_সুযোগ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    প্ৰমাণিত_কৰক(bind(둘째, (struct sockaddr *)&স্থানীয়_সুযোগ, sizeof স্থানীয়_সুযোগ) == -1 && errno == EADDRINUSE);
    প্ৰমাণিত_কৰক(close(둘째) == 0);
    둘째 = dup(종단점);
    প্ৰমাণিত_কৰক(close(종단점) == 0); 종단점 = 둘째;
    পীয়েৰ_মান.sin_family = AF_INET; পীয়েৰ_মান.sin_port = 망차례짧은수(접속번호);
    প্ৰমাণিত_কৰক(পাৰ্ছ_কৰক_নেটৱৰ্ক_ঠিকনা(AF_INET, "10.0.2.2", &পীয়েৰ_মান.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    প্ৰমাণিত_কৰক(পৰিবৰ্তন_কৰক_নেটৱৰ্ক_ছেটিংছ(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char ডাটা[32];
    প্ৰমাণিত_কৰক(자료전문받기(종단점, ডাটা, sizeof ডাটা, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    প্ৰমাণিত_কৰক(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&পীয়েৰ_মান, sizeof পীয়েৰ_মান) == 9);
    দৈর্ঘ্য_মান = sizeof 받은주소;
    প্ৰমাণিত_কৰক(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    প্ৰমাণিত_কৰক(자료전문받기(종단점, ডাটা, sizeof ডাটা, 0, (struct sockaddr *)&받은주소, &দৈর্ঘ্য_মান) == 9);
    প্ৰমাণিত_কৰক(memcmp(ডাটা, "posix-udp", 9) == 0 && দৈর্ঘ্য_মান == 16);
    প্ৰমাণিত_কৰক(받은주소.sin_port == পীয়েৰ_মান.sin_port && 받은주소.sin_addr.s_addr == পীয়েৰ_মান.sin_addr.s_addr);
    প্ৰমাণিত_কৰক(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&পীয়েৰ_মান, sizeof পীয়েৰ_মান) == 8);
    প্ৰমাণিত_কৰক(recvfrom(종단점, ডাটা, 3, 0, NULL, NULL) == 3 && memcmp(ডাটা, "tru", 3) == 0);
    প্ৰমাণিত_কৰক(recvfrom(종단점, ডাটা, sizeof ডাটা, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    প্ৰমাণিত_কৰক(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&পীয়েৰ_মান, sizeof পীয়েৰ_মান) == 0);
    প্ৰমাণিত_কৰক(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    প্ৰমাণিত_কৰক(recvfrom(종단점, ডাটা, sizeof ডাটা, 0, NULL, NULL) == -1 && errno == EAGAIN);
    প্ৰমাণিত_কৰক(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
