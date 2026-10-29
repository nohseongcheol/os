#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ) { size_t ಉದ್ದ_ಮೌಲ್ಯ = 0; while (ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ[ಉದ್ದ_ಮೌಲ್ಯ]) ಉದ್ದ_ಮೌಲ್ಯ++; return ಉದ್ದ_ಮೌಲ್ಯ; }
int strcmp(const char *ಮುಂದೆ_ಮೌಲ್ಯ, const char *ಹಿಂದೆ_ಮೌಲ್ಯ) {
    while (*ಮುಂದೆ_ಮೌಲ್ಯ && *ಮುಂದೆ_ಮೌಲ್ಯ == *ಹಿಂದೆ_ಮೌಲ್ಯ) { ಮುಂದೆ_ಮೌಲ್ಯ++; ಹಿಂದೆ_ಮೌಲ್ಯ++; }
    return (unsigned char)*ಮುಂದೆ_ಮೌಲ್ಯ - (unsigned char)*ಹಿಂದೆ_ಮೌಲ್ಯ;
}
int memcmp(const void *ಮುಂದೆ_ಮೌಲ್ಯ, const void *ಹಿಂದೆ_ಮೌಲ್ಯ, size_t 바이트수) {
    const unsigned char *가 = ಮುಂದೆ_ಮೌಲ್ಯ, *나 = ಹಿಂದೆ_ಮೌಲ್ಯ;
    for (size_t ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < 바이트수; ಸ್ಲಾಟ್_ನಮೂದು++) if (가[ಸ್ಲಾಟ್_ನಮೂದು] != 나[ಸ್ಲಾಟ್_ನಮೂದು]) return 가[ಸ್ಲಾಟ್_ನಮೂದು] - 나[ಸ್ಲಾಟ್_ನಮೂದು];
    return 0;
}
void *memcpy(void *ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ, const void *원본, size_t 바이트수) {
    unsigned char *가 = ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ; const unsigned char *나 = 원본;
    for (size_t ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < 바이트수; ಸ್ಲಾಟ್_ನಮೂದು++) 가[ಸ್ಲಾಟ್_ನಮೂದು] = 나[ಸ್ಲಾಟ್_ನಮೂದು];
    return ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ;
}
void *memset(void *ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ, int ಮೌಲ್ಯ, size_t 바이트수) {
    unsigned char *ಡೇಟಾ = ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ;
    for (size_t ಸ್ಲಾಟ್_ನಮೂದು = 0; ಸ್ಲಾಟ್_ನಮೂದು < 바이트수; ಸ್ಲಾಟ್_ನಮೂದು++) ಡೇಟಾ[ಸ್ಲಾಟ್_ನಮೂದು] = ಮೌಲ್ಯ;
    return ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ;
}
int putchar(int 문자) { unsigned char ಮೌಲ್ಯ = 문자; return write(1, &ಮೌಲ್ಯ, 1) == 1 ? ಮೌಲ್ಯ : EOF; }
int puts(const char *ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ) {
    size_t ಉದ್ದ_ಮೌಲ್ಯ = strlen(ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ), ಸ್ಥಾನ = 0;
    while (ಸ್ಥಾನ < ಉದ್ದ_ಮೌಲ್ಯ) { ssize_t ಮಾಪನ = write(1, ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ + ಸ್ಥಾನ, ಉದ್ದ_ಮೌಲ್ಯ - ಸ್ಥಾನ); if (ಮಾಪನ <= 0) return EOF; ಸ್ಥಾನ += ಮಾಪನ; }
    return putchar('\n') == EOF ? EOF : 0;
}
