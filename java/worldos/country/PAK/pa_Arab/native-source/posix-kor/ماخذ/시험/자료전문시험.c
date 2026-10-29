#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define تصدیق_کرو(حالت) do { if (!(حالت)) { puts("POSIX UDP CHECK FAILED: " #حالت); return 1; } } while (0)
int main(int 인수개수, char **دلیل_فرست) {
    تصدیق_کرو(인수개수 == 2);
    int 접속번호 = 0;
    for (int سلاٹ_داخلہ = 0; دلیل_فرست[1][سلاٹ_داخلہ]; سلاٹ_داخلہ++) {
        تصدیق_کرو(دلیل_فرست[1][سلاٹ_داخلہ] >= '0' && دلیل_فرست[1][سلاٹ_داخلہ] <= '9');
        접속번호 = 접속번호 * 10 + دلیل_فرست[1][سلاٹ_داخلہ] - '0';
        تصدیق_کرو(접속번호 <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    تصدیق_کرو(종단점 == 3);
    struct sockaddr_in مقامی_سکوپ = {0}, ہم_سر_قدر = {0}, 받은주소 = {0};
    مقامی_سکوپ.sin_family = AF_INET;
    socklen_t لمبائی_قدر = sizeof مقامی_سکوپ;
    تصدیق_کرو(통신주소읽기(종단점, (struct sockaddr *)&مقامی_سکوپ, &لمبائی_قدر) == 0 && مقامی_سکوپ.sin_port == 0);
    تصدیق_کرو(بنھنا_پتا(종단점, (struct sockaddr *)&مقامی_سکوپ, sizeof مقامی_سکوپ) == 0);
    تصدیق_کرو(통신주소읽기(종단점, (struct sockaddr *)&مقامی_سکوپ, &لمبائی_قدر) == 0 && ntohs(مقامی_سکوپ.sin_port) >= 49152);
    تصدیق_کرو(بنھنا_پتا(종단점, (struct sockaddr *)&مقامی_سکوپ, sizeof مقامی_سکوپ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    تصدیق_کرو(bind(둘째, (struct sockaddr *)&مقامی_سکوپ, sizeof مقامی_سکوپ) == -1 && errno == EADDRINUSE);
    تصدیق_کرو(close(둘째) == 0);
    둘째 = dup(종단점);
    تصدیق_کرو(close(종단점) == 0); 종단점 = 둘째;
    ہم_سر_قدر.sin_family = AF_INET; ہم_سر_قدر.sin_port = 망차례짧은수(접속번호);
    تصدیق_کرو(망주소해석하기(AF_INET, "10.0.2.2", &ہم_سر_قدر.sin_addr) == 1);
    struct timeval 대기 = {0, 200000};
    تصدیق_کرو(تبدیل_کرو_نیٹ_ورک_سیٹنگاں(종단점, SOL_SOCKET, SO_RCVTIMEO, &대기, sizeof 대기) == 0);
    char کوائف[32];
    تصدیق_کرو(자료전문받기(종단점, کوائف, sizeof کوائف, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تصدیق_کرو(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ہم_سر_قدر, sizeof ہم_سر_قدر) == 9);
    لمبائی_قدر = sizeof 받은주소;
    تصدیق_کرو(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    تصدیق_کرو(자료전문받기(종단점, کوائف, sizeof کوائف, 0, (struct sockaddr *)&받은주소, &لمبائی_قدر) == 9);
    تصدیق_کرو(memcmp(کوائف, "posix-udp", 9) == 0 && لمبائی_قدر == 16);
    تصدیق_کرو(받은주소.sin_port == ہم_سر_قدر.sin_port && 받은주소.sin_addr.s_addr == ہم_سر_قدر.sin_addr.s_addr);
    تصدیق_کرو(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ہم_سر_قدر, sizeof ہم_سر_قدر) == 8);
    تصدیق_کرو(recvfrom(종단점, کوائف, 3, 0, NULL, NULL) == 3 && memcmp(کوائف, "tru", 3) == 0);
    تصدیق_کرو(recvfrom(종단점, کوائف, sizeof کوائف, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تصدیق_کرو(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ہم_سر_قدر, sizeof ہم_سر_قدر) == 0);
    تصدیق_کرو(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    تصدیق_کرو(recvfrom(종단점, کوائف, sizeof کوائف, 0, NULL, NULL) == -1 && errno == EAGAIN);
    تصدیق_کرو(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
