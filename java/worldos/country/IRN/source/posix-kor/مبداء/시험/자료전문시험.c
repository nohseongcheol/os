#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define تأیید_صحت(شرط) do { if (!(شرط)) { puts("POSIX UDP CHECK FAILED: " #شرط); return 1; } } while (0)
int main(int 인수개수, char **آرگومان_لیست) {
    تأیید_صحت(인수개수 == 2);
    int شماره_درگاه = 0;
    for (int شکاف_ورودی = 0; آرگومان_لیست[1][شکاف_ورودی]; شکاف_ورودی++) {
        تأیید_صحت(آرگومان_لیست[1][شکاف_ورودی] >= '0' && آرگومان_لیست[1][شکاف_ورودی] <= '9');
        شماره_درگاه = شماره_درگاه * 10 + آرگومان_لیست[1][شکاف_ورودی] - '0';
        تأیید_صحت(شماره_درگاه <= 65535);
    }
    int 종단점 = 통신종단점만들기(AF_INET, SOCK_DGRAM, 0);
    تأیید_صحت(종단점 == 3);
    struct sockaddr_in محلی_محدوده = {0}, مشابه_مقدار = {0}, 받은주소 = {0};
    محلی_محدوده.sin_family = AF_INET;
    socklen_t طول_مقدار = sizeof محلی_محدوده;
    تأیید_صحت(통신주소읽기(종단점, (struct sockaddr *)&محلی_محدوده, &طول_مقدار) == 0 && محلی_محدوده.sin_port == 0);
    تأیید_صحت(مرتبط_سازی_آدرس(종단점, (struct sockaddr *)&محلی_محدوده, sizeof محلی_محدوده) == 0);
    تأیید_صحت(통신주소읽기(종단점, (struct sockaddr *)&محلی_محدوده, &طول_مقدار) == 0 && ntohs(محلی_محدوده.sin_port) >= 49152);
    تأیید_صحت(مرتبط_سازی_آدرس(종단점, (struct sockaddr *)&محلی_محدوده, sizeof محلی_محدوده) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    تأیید_صحت(bind(둘째, (struct sockaddr *)&محلی_محدوده, sizeof محلی_محدوده) == -1 && errno == EADDRINUSE);
    تأیید_صحت(close(둘째) == 0);
    둘째 = dup(종단점);
    تأیید_صحت(close(종단점) == 0); 종단점 = 둘째;
    مشابه_مقدار.sin_family = AF_INET; مشابه_مقدار.sin_port = 망차례짧은수(شماره_درگاه);
    تأیید_صحت(تفسیر_شبکه_آدرس(AF_INET, "10.0.2.2", &مشابه_مقدار.sin_addr) == 1);
    struct timeval منتظر_ماندن_مقدار = {0, 200000};
    تأیید_صحت(تغییر_شبکه_تنظیمات(종단점, SOL_SOCKET, SO_RCVTIMEO, &منتظر_ماندن_مقدار, sizeof منتظر_ماندن_مقدار) == 0);
    char داده_ها[32];
    تأیید_صحت(자료전문받기(종단점, داده_ها, sizeof داده_ها, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تأیید_صحت(자료전문보내기(종단점, "posix-udp", 9, 0, (struct sockaddr *)&مشابه_مقدار, sizeof مشابه_مقدار) == 9);
    طول_مقدار = sizeof 받은주소;
    تأیید_صحت(recvfrom(종단점, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    تأیید_صحت(자료전문받기(종단점, داده_ها, sizeof داده_ها, 0, (struct sockaddr *)&받은주소, &طول_مقدار) == 9);
    تأیید_صحت(memcmp(داده_ها, "posix-udp", 9) == 0 && طول_مقدار == 16);
    تأیید_صحت(받은주소.sin_port == مشابه_مقدار.sin_port && 받은주소.sin_addr.s_addr == مشابه_مقدار.sin_addr.s_addr);
    تأیید_صحت(sendto(종단점, "truncate", 8, 0, (struct sockaddr *)&مشابه_مقدار, sizeof مشابه_مقدار) == 8);
    تأیید_صحت(recvfrom(종단점, داده_ها, 3, 0, NULL, NULL) == 3 && memcmp(داده_ها, "tru", 3) == 0);
    تأیید_صحت(recvfrom(종단점, داده_ها, sizeof داده_ها, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    تأیید_صحت(sendto(종단점, NULL, 0, 0, (struct sockaddr *)&مشابه_مقدار, sizeof مشابه_مقدار) == 0);
    تأیید_صحت(recvfrom(종단점, NULL, 0, 0, NULL, NULL) == 0);
    تأیید_صحت(recvfrom(종단점, داده_ها, sizeof داده_ها, 0, NULL, NULL) == -1 && errno == EAGAIN);
    تأیید_صحت(close(종단점) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
