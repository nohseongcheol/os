#include <파일규약.h>
#include <통신규약.h>
#include <string.h>
#include <stdio.h>

#define ודא_אמת(תנאי) do { if (!(תנאי)) { puts("POSIX UDP CHECK FAILED: " #תנאי); return 1; } } while (0)
int main(int 인수개수, char **ארגומנט_רשימה) {
    ודא_אמת(인수개수 == 2);
    int מספר_יציאה = 0;
    for (int חריץ_ערך = 0; ארגומנט_רשימה[1][חריץ_ערך]; חריץ_ערך++) {
        ודא_אמת(ארגומנט_רשימה[1][חריץ_ערך] >= '0' && ארגומנט_רשימה[1][חריץ_ערך] <= '9');
        מספר_יציאה = מספר_יציאה * 10 + ארגומנט_רשימה[1][חריץ_ערך] - '0';
        ודא_אמת(מספר_יציאה <= 65535);
    }
    int משתתף_ערך = ליצור_משתתף(AF_INET, SOCK_DGRAM, 0);
    ודא_אמת(משתתף_ערך == 3);
    struct sockaddr_in מקומי_היקף = {0}, עמית_ערך = {0}, 받은주소 = {0};
    מקומי_היקף.sin_family = AF_INET;
    socklen_t 길이 = sizeof מקומי_היקף;
    ודא_אמת(통신주소읽기(משתתף_ערך, (struct sockaddr *)&מקומי_היקף, &길이) == 0 && מקומי_היקף.sin_port == 0);
    ודא_אמת(לאגד_למען(משתתף_ערך, (struct sockaddr *)&מקומי_היקף, sizeof מקומי_היקף) == 0);
    ודא_אמת(통신주소읽기(משתתף_ערך, (struct sockaddr *)&מקומי_היקף, &길이) == 0 && ntohs(מקומי_היקף.sin_port) >= 49152);
    ודא_אמת(לאגד_למען(משתתף_ערך, (struct sockaddr *)&מקומי_היקף, sizeof מקומי_היקף) == -1 && errno == EINVAL);
    int 둘째 = socket(AF_INET, SOCK_DGRAM, 0);
    ודא_אמת(bind(둘째, (struct sockaddr *)&מקומי_היקף, sizeof מקומי_היקף) == -1 && errno == EADDRINUSE);
    ודא_אמת(close(둘째) == 0);
    둘째 = dup(משתתף_ערך);
    ודא_אמת(close(משתתף_ערך) == 0); משתתף_ערך = 둘째;
    עמית_ערך.sin_family = AF_INET; עמית_ערך.sin_port = 망차례짧은수(מספר_יציאה);
    ודא_אמת(ניתוח_מבנה_טקסט_מזהה_רשת(AF_INET, "10.0.2.2", &עמית_ערך.sin_addr) == 1);
    struct timeval רק_רגע_ערך = {0, 200000};
    ודא_אמת(שנה_רשת_הגדרות(משתתף_ערך, SOL_SOCKET, SO_RCVTIMEO, &רק_רגע_ערך, sizeof רק_רגע_ערך) == 0);
    char נתונים[32];
    ודא_אמת(לקבל_יחידת_נתונים_נתונים(משתתף_ערך, נתונים, sizeof נתונים, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ודא_אמת(שלח_יחידת_נתונים_נתונים(משתתף_ערך, "posix-udp", 9, 0, (struct sockaddr *)&עמית_ערך, sizeof עמית_ערך) == 9);
    길이 = sizeof 받은주소;
    ודא_אמת(recvfrom(משתתף_ערך, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    ודא_אמת(לקבל_יחידת_נתונים_נתונים(משתתף_ערך, נתונים, sizeof נתונים, 0, (struct sockaddr *)&받은주소, &길이) == 9);
    ודא_אמת(memcmp(נתונים, "posix-udp", 9) == 0 && 길이 == 16);
    ודא_אמת(받은주소.sin_port == עמית_ערך.sin_port && 받은주소.sin_addr.s_addr == עמית_ערך.sin_addr.s_addr);
    ודא_אמת(sendto(משתתף_ערך, "truncate", 8, 0, (struct sockaddr *)&עמית_ערך, sizeof עמית_ערך) == 8);
    ודא_אמת(recvfrom(משתתף_ערך, נתונים, 3, 0, NULL, NULL) == 3 && memcmp(נתונים, "tru", 3) == 0);
    ודא_אמת(recvfrom(משתתף_ערך, נתונים, sizeof נתונים, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    ודא_אמת(sendto(משתתף_ערך, NULL, 0, 0, (struct sockaddr *)&עמית_ערך, sizeof עמית_ערך) == 0);
    ודא_אמת(recvfrom(משתתף_ערך, NULL, 0, 0, NULL, NULL) == 0);
    ודא_אמת(recvfrom(משתתף_ערך, נתונים, sizeof נתונים, 0, NULL, NULL) == -1 && errno == EAGAIN);
    ודא_אמת(close(משתתף_ערך) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
