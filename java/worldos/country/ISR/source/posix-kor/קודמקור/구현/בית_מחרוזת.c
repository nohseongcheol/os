#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *מחרוזת_ערך) { size_t 길이 = 0; while (מחרוזת_ערך[길이]) 길이++; return 길이; }
int strcmp(const char *מצלמה_קדמית_ערך_ec1a6b96, const char *הקודם_ערך) {
    while (*מצלמה_קדמית_ערך_ec1a6b96 && *מצלמה_קדמית_ערך_ec1a6b96 == *הקודם_ערך) { מצלמה_קדמית_ערך_ec1a6b96++; הקודם_ערך++; }
    return (unsigned char)*מצלמה_קדמית_ערך_ec1a6b96 - (unsigned char)*הקודם_ערך;
}
int memcmp(const void *מצלמה_קדמית_ערך_ec1a6b96, const void *הקודם_ערך, size_t 바이트수) {
    const unsigned char *가 = מצלמה_קדמית_ערך_ec1a6b96, *나 = הקודם_ערך;
    for (size_t חריץ_ערך = 0; חריץ_ערך < 바이트수; חריץ_ערך++) if (가[חריץ_ערך] != 나[חריץ_ערך]) return 가[חריץ_ערך] - 나[חריץ_ערך];
    return 0;
}
void *memcpy(void *יעד_ערך, const void *원본, size_t 바이트수) {
    unsigned char *가 = יעד_ערך; const unsigned char *나 = 원본;
    for (size_t חריץ_ערך = 0; חריץ_ערך < 바이트수; חריץ_ערך++) 가[חריץ_ערך] = 나[חריץ_ערך];
    return יעד_ערך;
}
void *memset(void *יעד_ערך, int ערך, size_t 바이트수) {
    unsigned char *נתונים = יעד_ערך;
    for (size_t חריץ_ערך = 0; חריץ_ערך < 바이트수; חריץ_ערך++) נתונים[חריץ_ערך] = ערך;
    return יעד_ערך;
}
int putchar(int 문자) { unsigned char ערך = 문자; return write(1, &ערך, 1) == 1 ? ערך : EOF; }
int puts(const char *מחרוזת_ערך) {
    size_t 길이 = strlen(מחרוזת_ערך), מיקום = 0;
    while (מיקום < 길이) { ssize_t תוצאה = write(1, מחרוזת_ערך + מיקום, 길이 - מיקום); if (תוצאה <= 0) return EOF; מיקום += תוצאה; }
    return putchar('\n') == EOF ? EOF : 0;
}
