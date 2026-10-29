#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define تصدیق_کریں(شرط) do { if (!(شرط)) { puts("POSIX UDP CHECK FAILED: " #شرط); return 1; } } while (0)
int main(int 인수개수, char **دلائل_فہرست) {
    تصدیق_کریں(인수개수 == 2);
    int دہانہ_نمبر = 0;
    for (int سلاٹ_اندراج = 0; دلائل_فہرست[1][سلاٹ_اندراج]; سلاٹ_اندراج++) {
        تصدیق_کریں(دلائل_فہرست[1][سلاٹ_اندراج] >= '0' && دلائل_فہرست[1][سلاٹ_اندراج] <= '9');
        دہانہ_نمبر = دہانہ_نمبر * 10 + دلائل_فہرست[1][سلاٹ_اندراج] - '0';
        تصدیق_کریں(دہانہ_نمبر <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    تصدیق_کریں(종단점 == 3);
    struct sockaddr_in مقامی_اسکوپ = {0}, ساتھی_قدر = {0}, 받은주소 = {0};
    مقامی_اسکوپ.sin_family = AF_INET;
    socklen_t لمبا_ئی_قدر = sizeof مقامی_اسکوپ;
    تصدیق_کریں(통신주소읽기(종단점, (struct sockaddr *)&مقامی_اسکوپ, &لمبا_ئی_قدر) == 0 && مقامی_اسکوپ.sin_port == 0);
    تصدیق_کریں(باندھیں_پتہ(종단점, (struct sockaddr *)&مقامی_اسکوپ, sizeof مقامی_اسکوپ) == 0);
    تصدیق_کریں(통신주소읽기(종단점, (struct sockaddr *)&مقامی_اسکوپ, &لمبا_ئی_قدر) == 0 && ntohs(مقامی_اسکوپ.sin_port) >= 49152);
    تصدیق_کریں(باندھیں_پتہ(종단점, (struct sockaddr *)&مقامی_اسکوپ, sizeof مقامی_اسکوپ) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    تصدیق_کریں(bind(둘째, (struct sockaddr *)&مقامی_اسکوپ, sizeof مقامی_اسکوپ) == -1 && errno == EADDRINUSE);
    تصدیق_کریں(close(둘째) == 0);
    둘째 = dup(종단점);
    تصدیق_کریں(close(종단점) == 0); 종단점 = 둘째;
    ساتھی_قدر.sin_family = AF_INET; ساتھی_قدر.sin_port = 망차례짧은수(دہانہ_نمبر);
    تصدیق_کریں(پارس_نیٹ_ورک_پتہ(AF_INET, "10.0.2.2", &ساتھی_قدر.sin_addr) == 1);
    struct timeval انتظار_قدر = {0, 200000};
    تصدیق_کریں(تبدیل_کریں_نیٹ_ورک_سیٹنگز(종단점, SOL_SOCKET, SO_RCVTIMEO, &انتظار_قدر, sizeof انتظار_قدر) == 0);
    char کوائف[32];
    تصدیق_کریں(자료전문받기(종단점, کوائف, sizeof کوائف, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تصدیق_کریں(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&ساتھی_قدر, sizeof ساتھی_قدر) == 9);
    لمبا_ئی_قدر = sizeof 받은주소;
    تصدیق_کریں(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    تصدیق_کریں(자료전문받기(종단점, کوائف, sizeof کوائف, 0, (struct sockaddr *)&받은주소, &لمبا_ئی_قدر) == 9);
    تصدیق_کریں(memcmp(کوائف, "posix-udp", 9) == 0 && لمبا_ئی_قدر == 16);
    تصدیق_کریں(받은주소.sin_port == ساتھی_قدر.sin_port && 받은주소.sin_addr.s_addr == ساتھی_قدر.sin_addr.s_addr);
    تصدیق_کریں(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&ساتھی_قدر, sizeof ساتھی_قدر) == 8);
    تصدیق_کریں(recvfrom(종단점, کوائف, 3, 0, NULL, NULL) == 3 && memcmp(کوائف, "tru", 3) == 0);
    تصدیق_کریں(recvfrom(종단점, کوائف, sizeof کوائف, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تصدیق_کریں(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&ساتھی_قدر, sizeof ساتھی_قدر) == 0);
    تصدیق_کریں(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    تصدیق_کریں(recvfrom(종단점, کوائف, sizeof کوائف, 0, NULL, NULL) == -1 && errno == EAGAIN);
    تصدیق_کریں(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
