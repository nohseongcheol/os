#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *අනුලකුණු_වැල_අගය) { size_t දිග_අගය = 0; while (අනුලකුණු_වැල_අගය[දිග_අගය]) දිග_අගය++; return දිග_අගය; }
int strcmp(const char *앞, const char *ආපසු_අගය) {
    while (*앞 && *앞 == *ආපසු_අගය) { 앞++; ආපසු_අගය++; }
    return (unsigned char)*앞 - (unsigned char)*ආපසු_අගය;
}
int memcmp(const void *앞, const void *ආපසු_අගය, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = ආපසු_අගය;
    for (size_t විවරය_පිවිසුම = 0; විවරය_පිවිසුම < 바이트수; විවරය_පිවිසුම++) if (가[විවරය_පිවිසුම] != 나[විවරය_පිවිසුම]) return 가[විවරය_පිවිසුම] - 나[විවරය_පිවිසුම];
    return 0;
}
void *memcpy(void *ගමනාන්තය_අගය, const void *원본, size_t 바이트수) {
    unsigned char *가 = ගමනාන්තය_අගය; const unsigned char *나 = 원본;
    for (size_t විවරය_පිවිසුම = 0; විවරය_පිවිසුම < 바이트수; විවරය_පිවිසුම++) 가[විවරය_පිවිසුම] = 나[විවරය_පිවිසුම];
    return ගමනාන්තය_අගය;
}
void *memset(void *ගමනාන්තය_අගය, int අගය, size_t 바이트수) {
    unsigned char *දත්ත = ගමනාන්තය_අගය;
    for (size_t විවරය_පිවිසුම = 0; විවරය_පිවිසුම < 바이트수; විවරය_පිවිසුම++) දත්ත[විවරය_පිවිසුම] = අගය;
    return ගමනාන්තය_අගය;
}
int putchar(int 문자) { unsigned char අගය = 문자; return write(1, &අගය, 1) == 1 ? අගය : EOF; }
int puts(const char *අනුලකුණු_වැල_අගය) {
    size_t දිග_අගය = strlen(අනුලකුණු_වැල_අගය), පිහිටීම = 0;
    while (පිහිටීම < දිග_අගය) { ssize_t 결과 = write(1, අනුලකුණු_වැල_අගය + පිහිටීම, දිග_අගය - පිහිටීම); if (결과 <= 0) return EOF; පිහිටීම += 결과; }
    return putchar('\n') == EOF ? EOF : 0;
}
