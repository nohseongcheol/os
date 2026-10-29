#include "string.h"
size_t strlen(const char *ሕብረ_ቁምፊ_ሓበሬታ) { const char *자료위치 = ሕብረ_ቁምፊ_ሓበሬታ; while (*자료위치) 자료위치++; return 자료위치 - ሕብረ_ቁምፊ_ሓበሬታ; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *가로좌표 = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*가로좌표 != *세로좌표) return (int)*가로좌표 - *세로좌표; 가로좌표++; 세로좌표++; } return 0; }
void *memmove(void *መዓልቦ_ሓበሬታ, const void *ሕብረ_ቁምፊ_ሓበሬታ, size_t 개수) { unsigned char *가로좌표 = መዓልቦ_ሓበሬታ; const unsigned char *세로좌표 = ሕብረ_ቁምፊ_ሓበሬታ; if (가로좌표 < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) 가로좌표[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; 가로좌표[개수] = 세로좌표[개수]; } } return መዓልቦ_ሓበሬታ; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char 가로좌표 = *첫째값++, 세로좌표 = *둘째값++; if (가로좌표 != 세로좌표) return (int)가로좌표-세로좌표; if (!가로좌표) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *ሕብረ_ቁምፊ_ሓበሬታ, char **ኣቑም_ሽፋን, int ድሕረባይታ_ዋጋ) {
    const char *ጀምር_ሽፋን = ሕብረ_ቁምፊ_ሓበሬታ; unsigned long ዋጋ = 0; int ምምስጣር_ዋጋ = 1, 하나라도 = 0;
    while (*ሕብረ_ቁምፊ_ሓበሬታ == ' ' || (*ሕብረ_ቁምፊ_ሓበሬታ >= 9 && *ሕብረ_ቁምፊ_ሓበሬታ <= 13)) ሕብረ_ቁምፊ_ሓበሬታ++;
    if (*ሕብረ_ቁምፊ_ሓበሬታ == '-' || *ሕብረ_ቁምፊ_ሓበሬታ == '+') { if (*ሕብረ_ቁምፊ_ሓበሬታ == '-') ምምስጣር_ዋጋ = -1; ሕብረ_ቁምፊ_ሓበሬታ++; }
    if (ድሕረባይታ_ዋጋ == 0) ድሕረባይታ_ዋጋ = 10;
    while (*ሕብረ_ቁምፊ_ሓበሬታ >= '0' && *ሕብረ_ቁምፊ_ሓበሬታ <= '9' && *ሕብረ_ቁምፊ_ሓበሬታ - '0' < ድሕረባይታ_ዋጋ) {
        unsigned ኣሃዝ_ዋጋ = *ሕብረ_ቁምፊ_ሓበሬታ++ - '0'; 하나라도 = 1;
        if (ዋጋ > (0x7ffffffffffffffful - ኣሃዝ_ዋጋ) / (unsigned)ድሕረባይታ_ዋጋ) ዋጋ = 0x7ffffffffffffffful;
        else ዋጋ = ዋጋ * ድሕረባይታ_ዋጋ + ኣሃዝ_ዋጋ;
    }
    if (ኣቑም_ሽፋን) *ኣቑም_ሽፋን = (char *)(하나라도 ? ሕብረ_ቁምፊ_ሓበሬታ : ጀምር_ሽፋን); return ምምስጣር_ዋጋ > 0 ? (long)ዋጋ : -(long)ዋጋ;
}
int atoi(const char *ሕብረ_ቁምፊ_ሓበሬታ) { return (int)strtol(ሕብረ_ቁምፊ_ሓበሬታ, 0, 10); }
