#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ھەرپ_تىزمىسى_قىممىتى) { size_t ئۇزۇنلۇق_قىممىتى = 0; while (ھەرپ_تىزمىسى_قىممىتى[ئۇزۇنلۇق_قىممىتى]) ئۇزۇنلۇق_قىممىتى++; return ئۇزۇنلۇق_قىممىتى; }
int strcmp(const char *앞, const char *ئارقىغا_قىممىتى) {
    while (*앞 && *앞 == *ئارقىغا_قىممىتى) { 앞++; ئارقىغا_قىممىتى++; }
    return (unsigned char)*앞 - (unsigned char)*ئارقىغا_قىممىتى;
}
int memcmp(const void *앞, const void *ئارقىغا_قىممىتى, size_t 바이트수) {
    const unsigned char *가 = 앞, *나 = ئارقىغا_قىممىتى;
    for (size_t ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < 바이트수; ئوقۇر_كىرگۈزۈش++) if (가[ئوقۇر_كىرگۈزۈش] != 나[ئوقۇر_كىرگۈزۈش]) return 가[ئوقۇر_كىرگۈزۈش] - 나[ئوقۇر_كىرگۈزۈش];
    return 0;
}
void *memcpy(void *نىشان_قىممىتى, const void *원본, size_t 바이트수) {
    unsigned char *가 = نىشان_قىممىتى; const unsigned char *나 = 원본;
    for (size_t ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < 바이트수; ئوقۇر_كىرگۈزۈش++) 가[ئوقۇر_كىرگۈزۈش] = 나[ئوقۇر_كىرگۈزۈش];
    return نىشان_قىممىتى;
}
void *memset(void *نىشان_قىممىتى, int قىممىتى, size_t 바이트수) {
    unsigned char *مەلۇمات = نىشان_قىممىتى;
    for (size_t ئوقۇر_كىرگۈزۈش = 0; ئوقۇر_كىرگۈزۈش < 바이트수; ئوقۇر_كىرگۈزۈش++) مەلۇمات[ئوقۇر_كىرگۈزۈش] = قىممىتى;
    return نىشان_قىممىتى;
}
int putchar(int 문자) { unsigned char قىممىتى = 문자; return write(1, &قىممىتى, 1) == 1 ? قىممىتى : EOF; }
int puts(const char *ھەرپ_تىزمىسى_قىممىتى) {
    size_t ئۇزۇنلۇق_قىممىتى = strlen(ھەرپ_تىزمىسى_قىممىتى), ئورۇن = 0;
    while (ئورۇن < ئۇزۇنلۇق_قىممىتى) { ssize_t ئۆلچەم = write(1, ھەرپ_تىزمىسى_قىممىتى + ئورۇن, ئۇزۇنلۇق_قىممىتى - ئورۇن); if (ئۆلچەم <= 0) return EOF; ئورۇن += ئۆلچەم; }
    return putchar('\n') == EOF ? EOF : 0;
}
