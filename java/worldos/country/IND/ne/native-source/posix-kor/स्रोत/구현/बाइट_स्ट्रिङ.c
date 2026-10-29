#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *स्ट्रिङ_मान) { size_t लम्बाइ_मान = 0; while (स्ट्रिङ_मान[लम्बाइ_मान]) लम्बाइ_मान++; return लम्बाइ_मान; }
int strcmp(const char *앞, const char *पछाडि_मान) {
    while (*앞 && *앞 == *पछाडि_मान) { 앞++; पछाडि_मान++; }
    return (unsigned char)*앞 - (unsigned char)*पछाडि_मान;
}
int memcmp(const void *앞, const void *पछाडि_मान, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = पछाडि_मान;
    for (size_t स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < 바이트수; स्लट_प्रविष्टि++) if (가[स्लट_प्रविष्टि] != 나[स्लट_प्रविष्टि]) return 가[स्लट_प्रविष्टि] - 나[स्लट_प्रविष्टि];
    return 0;
}
void *memcpy(void *गन्तव्य_मान, const void *원본, size_t 바이트수) {
    unsigned char *가 = गन्तव्य_मान; const unsigned char *나 = 원본;
    for (size_t स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < 바이트수; स्लट_प्रविष्टि++) 가[स्लट_प्रविष्टि] = 나[स्लट_प्रविष्टि];
    return गन्तव्य_मान;
}
void *memset(void *गन्तव्य_मान, int मान, size_t 바이트수) {
    unsigned char *लगत = गन्तव्य_मान;
    for (size_t स्लट_प्रविष्टि = 0; स्लट_प्रविष्टि < 바이트수; स्लट_प्रविष्टि++) लगत[स्लट_प्रविष्टि] = मान;
    return गन्तव्य_मान;
}
int putchar(int 문자) { unsigned char मान = 문자; return write(1, &मान, 1) == 1 ? मान : EOF; }
int puts(const char *स्ट्रिङ_मान) {
    size_t लम्बाइ_मान = strlen(स्ट्रिङ_मान), स्थिति = 0;
    while (स्थिति < लम्बाइ_मान) { ssize_t मापन = write(1, स्ट्रिङ_मान + स्थिति, लम्बाइ_मान - स्थिति); if (मापन <= 0) return EOF; स्थिति += मापन; }
    return putchar('\n') == EOF ? EOF : 0;
}
