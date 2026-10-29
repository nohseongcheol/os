#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define يتحقق(شرط) do { if (!(شرط)) { puts("POSIX UDP CHECK FAILED: " #شرط); return 1; } } while (0)
int main(int 인수개수, char **وسيطة_قائمة) {
    يتحقق(인수개수 == 2);
    int رقم_المنفذ = 0;
    for (int فتحة_إدخال = 0; وسيطة_قائمة[1][فتحة_إدخال]; فتحة_إدخال++) {
        يتحقق(وسيطة_قائمة[1][فتحة_إدخال] >= '0' && وسيطة_قائمة[1][فتحة_إدخال] <= '9');
        رقم_المنفذ = رقم_المنفذ * 10 + وسيطة_قائمة[1][فتحة_إدخال] - '0';
        يتحقق(رقم_المنفذ <= 65535);
    }
    int المشارك_قيمة = فتح_المشارك(AF_INET, SOCK_DGRAM, 0);
    يتحقق(المشارك_قيمة == 3);
    struct sockaddr_in محلي_نطاق = {0}, نظير_قيمة = {0}, 받은주소 = {0};
    محلي_نطاق.sin_family = AF_INET;
    socklen_t 길이 = sizeof محلي_نطاق;
    يتحقق(يقرأ_مأخذ_التوصيل_عنوان(المشارك_قيمة, (struct sockaddr *)&محلي_نطاق, &길이) == 0 && محلي_نطاق.sin_port == 0);
    يتحقق(يربط_عنوان(المشارك_قيمة, (struct sockaddr *)&محلي_نطاق, sizeof محلي_نطاق) == 0);
    يتحقق(يقرأ_مأخذ_التوصيل_عنوان(المشارك_قيمة, (struct sockaddr *)&محلي_نطاق, &길이) == 0 && ntohs(محلي_نطاق.sin_port) >= 49152);
    يتحقق(يربط_عنوان(المشارك_قيمة, (struct sockaddr *)&محلي_نطاق, sizeof محلي_نطاق) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    يتحقق(bind(둘째, (struct sockaddr *)&محلي_نطاق, sizeof محلي_نطاق) == -1 && errno == EADDRINUSE);
    يتحقق(close(둘째) == 0);
    둘째 = dup(المشارك_قيمة);
    يتحقق(close(المشارك_قيمة) == 0); المشارك_قيمة = 둘째;
    نظير_قيمة.sin_family = AF_INET; نظير_قيمة.sin_port = 망차례짧은수(رقم_المنفذ);
    يتحقق(يوزّع_معرف_الشبكة(AF_INET, "10.0.2.2", &نظير_قيمة.sin_addr) == 1);
    struct timeval انتظر_قيمة = {0, 200000};
    يتحقق(يغيّر_شبكة_إعدادات(المشارك_قيمة, SOL_SOCKET, SO_RCVTIMEO, &انتظر_قيمة, sizeof انتظر_قيمة) == 0);
    char بيانات[32];
    يتحقق(يستلم_مخطط_بيانات_بيانات(المشارك_قيمة, بيانات, sizeof بيانات, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    يتحقق(يرسل_مخطط_بيانات_بيانات(المشارك_قيمة, "posix-udp", 9, 0, (struct sockaddr *)&نظير_قيمة, sizeof نظير_قيمة) == 9);
    길이 = sizeof 받은주소;
    يتحقق(recvfrom(المشارك_قيمة, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    يتحقق(يستلم_مخطط_بيانات_بيانات(المشارك_قيمة, بيانات, sizeof بيانات, 0, (struct sockaddr *)&받은주소, &길이) == 9);
    يتحقق(memcmp(بيانات, "posix-udp", 9) == 0 && 길이 == 16);
    يتحقق(받은주소.sin_port == نظير_قيمة.sin_port && 받은주소.sin_addr.s_addr == نظير_قيمة.sin_addr.s_addr);
    يتحقق(sendto(المشارك_قيمة, "truncate", 8, 0, (struct sockaddr *)&نظير_قيمة, sizeof نظير_قيمة) == 8);
    يتحقق(recvfrom(المشارك_قيمة, بيانات, 3, 0, NULL, NULL) == 3 && memcmp(بيانات, "tru", 3) == 0);
    يتحقق(recvfrom(المشارك_قيمة, بيانات, sizeof بيانات, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    يتحقق(sendto(المشارك_قيمة, NULL, 0, 0, (struct sockaddr *)&نظير_قيمة, sizeof نظير_قيمة) == 0);
    يتحقق(recvfrom(المشارك_قيمة, NULL, 0, 0, NULL, NULL) == 0);
    يتحقق(recvfrom(المشارك_قيمة, بيانات, sizeof بيانات, 0, NULL, NULL) == -1 && errno == EAGAIN);
    يتحقق(close(المشارك_قيمة) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
