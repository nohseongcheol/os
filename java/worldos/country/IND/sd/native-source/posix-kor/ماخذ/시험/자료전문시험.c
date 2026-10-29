#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define تصديق_ڪريو(حالت) do { if (!(حالت)) { puts("POSIX UDP CHECK FAILED: " #حالت); return 1; } } while (0)
int main(int 인수개수, char **دليل_فهرست) {
    تصديق_ڪريو(인수개수 == 2);
    int 접속번호 = 0;
    for (int سوراخ_داخلا = 0; دليل_فهرست[1][سوراخ_داخلا]; سوراخ_داخلا++) {
        تصديق_ڪريو(دليل_فهرست[1][سوراخ_داخلا] >= '0' && دليل_فهرست[1][سوراخ_داخلا] <= '9');
        접속번호 = 접속번호 * 10 + دليل_فهرست[1][سوراخ_داخلا] - '0';
        تصديق_ڪريو(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    تصديق_ڪريو(종단점 == 3);
    struct sockaddr_in مقامي_اسڪوپ = {0}, همعصر_قدر = {0}, 받은주소 = {0};
    مقامي_اسڪوپ.sin_family = AF_INET;
    socklen_t لمبائي_قدر = sizeof مقامي_اسڪوپ;
    تصديق_ڪريو(통신주소읽기(종단점, (struct sockaddr *)&مقامي_اسڪوپ, &لمبائي_قدر) == 0 && مقامي_اسڪوپ.sin_port == 0);
    تصديق_ڪريو(ٻڌو_پتو(종단점, (struct sockaddr *)&مقامي_اسڪوپ, sizeof مقامي_اسڪوپ) == 0);
    تصديق_ڪريو(통신주소읽기(종단점, (struct sockaddr *)&مقامي_اسڪوپ, &لمبائي_قدر) == 0 && ntohs(مقامي_اسڪوپ.sin_port) >= 49152);
    تصديق_ڪريو(ٻڌو_پتو(종단점, (struct sockaddr *)&مقامي_اسڪوپ, sizeof مقامي_اسڪوپ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    تصديق_ڪريو(bind(둘째, (struct sockaddr *)&مقامي_اسڪوپ, sizeof مقامي_اسڪوپ) == -1 && errno == EADDRINUSE);
    تصديق_ڪريو(close(둘째) == 0);
    둘째 = dup(종단점);
    تصديق_ڪريو(close(종단점) == 0); 종단점 = 둘째;
    همعصر_قدر.sin_family = AF_INET; همعصر_قدر.sin_port = 망차례짧은수(접속번호);
    تصديق_ڪريو(망주소해석하기(AF_INET, "10.0.2.2", &همعصر_قدر.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    تصديق_ڪريو(تبديل_ڪريو_نيٽ_ورڪ_سيٽنگون(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char ڪوائف[32];
    تصديق_ڪريو(자료전문받기(종단점, ڪوائف, sizeof ڪوائف, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تصديق_ڪريو(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&همعصر_قدر, sizeof همعصر_قدر) == 9);
    لمبائي_قدر = sizeof 받은주소;
    تصديق_ڪريو(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    تصديق_ڪريو(자료전문받기(종단점, ڪوائف, sizeof ڪوائف, 0, (struct sockaddr *)&받은주소, &لمبائي_قدر) == 9);
    تصديق_ڪريو(memcmp(ڪوائف, "posix-udp", 9) == 0 && لمبائي_قدر == 16);
    تصديق_ڪريو(받은주소.sin_port == همعصر_قدر.sin_port && 받은주소.sin_addr.s_addr == همعصر_قدر.sin_addr.s_addr);
    تصديق_ڪريو(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&همعصر_قدر, sizeof همعصر_قدر) == 8);
    تصديق_ڪريو(recvfrom(종단점, ڪوائف, 3, 0, NULL, NULL) == 3 && memcmp(ڪوائف, "tru", 3) == 0);
    تصديق_ڪريو(recvfrom(종단점, ڪوائف, sizeof ڪوائف, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تصديق_ڪريو(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&همعصر_قدر, sizeof همعصر_قدر) == 0);
    تصديق_ڪريو(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    تصديق_ڪريو(recvfrom(종단점, ڪوائف, sizeof ڪوائف, 0, NULL, NULL) == -1 && errno == EAGAIN);
    تصديق_ڪريو(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
