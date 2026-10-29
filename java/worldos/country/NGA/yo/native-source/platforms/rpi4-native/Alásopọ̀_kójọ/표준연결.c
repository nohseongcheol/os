#include "string.h"
size_t strlen(const char *fọ́nrán_détà) { const char *자료위치 = fọ́nrán_détà; while (*자료위치) 자료위치++; return 자료위치 - fọ́nrán_détà; }
int memcmp(const void *첫째값, const void *둘째값, size_t 개수) { const unsigned char *ibi_ìtọ́kasí_x = 첫째값, *세로좌표 = 둘째값; while (개수--) { if (*ibi_ìtọ́kasí_x != *세로좌표) return (int)*ibi_ìtọ́kasí_x - *세로좌표; ibi_ìtọ́kasí_x++; 세로좌표++; } return 0; }
void *memmove(void *èbúté_détà, const void *fọ́nrán_détà, size_t 개수) { unsigned char *ibi_ìtọ́kasí_x = èbúté_détà; const unsigned char *세로좌표 = fọ́nrán_détà; if (ibi_ìtọ́kasí_x < 세로좌표) { for (size_t 순번 = 0; 순번 < 개수; 순번++) ibi_ìtọ́kasí_x[순번] = 세로좌표[순번]; } else { while (개수) { 개수--; ibi_ìtọ́kasí_x[개수] = 세로좌표[개수]; } } return èbúté_détà; }
int strncmp(const char *첫째값, const char *둘째값, size_t 개수) { while (개수--) { unsigned char ibi_ìtọ́kasí_x = *첫째값++, 세로좌표 = *둘째값++; if (ibi_ìtọ́kasí_x != 세로좌표) return (int)ibi_ìtọ́kasí_x-세로좌표; if (!ibi_ìtọ́kasí_x) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *fọ́nrán_détà, char **parí_Ìtayọ, int Àgbétẹ́lẹ̀_iye) {
    const char *bẹ̀rẹ̀_Ìtayọ = fọ́nrán_détà; unsigned long iye = 0; int pípàrokò_iye = 1, 하나라도 = 0;
    while (*fọ́nrán_détà == ' ' || (*fọ́nrán_détà >= 9 && *fọ́nrán_détà <= 13)) fọ́nrán_détà++;
    if (*fọ́nrán_détà == '-' || *fọ́nrán_détà == '+') { if (*fọ́nrán_détà == '-') pípàrokò_iye = -1; fọ́nrán_détà++; }
    if (Àgbétẹ́lẹ̀_iye == 0) Àgbétẹ́lẹ̀_iye = 10;
    while (*fọ́nrán_détà >= '0' && *fọ́nrán_détà <= '9' && *fọ́nrán_détà - '0' < Àgbétẹ́lẹ̀_iye) {
        unsigned díjììtì_iye = *fọ́nrán_détà++ - '0'; 하나라도 = 1;
        if (iye > (0x7ffffffffffffffful - díjììtì_iye) / (unsigned)Àgbétẹ́lẹ̀_iye) iye = 0x7ffffffffffffffful;
        else iye = iye * Àgbétẹ́lẹ̀_iye + díjììtì_iye;
    }
    if (parí_Ìtayọ) *parí_Ìtayọ = (char *)(하나라도 ? fọ́nrán_détà : bẹ̀rẹ̀_Ìtayọ); return pípàrokò_iye > 0 ? (long)iye : -(long)iye;
}
int atoi(const char *fọ́nrán_détà) { return (int)strtol(fọ́nrán_détà, 0, 10); }
