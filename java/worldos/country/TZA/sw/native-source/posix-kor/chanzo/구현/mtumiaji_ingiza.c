#include "호출경계.h"
extern int main(int 인수개수, char **hoja_Orodha);
static char hoja_kumbukumbu[2048];
static char *hoja_Orodha[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 tekeleza_amri 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    hoja_Orodha[0] = "jkoros-app";
    int 위치 = 0;
    for (int kielezo = 0; kielezo < 개수; kielezo++) {
        const int *원본 = (const int *)jkoros_syscall(3, kielezo, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        hoja_Orodha[kielezo + 1] = hoja_kumbukumbu + 위치;
        for (int Sloti_ingizo = 0; Sloti_ingizo < 원본[0]; Sloti_ingizo++) {
            if (위치 >= 2047) return 126;
            hoja_kumbukumbu[위치++] = 원본[Sloti_ingizo + 1];
        }
        hoja_kumbukumbu[위치++] = 0;
    }
    hoja_Orodha[개수 + 1] = 0;
    return main(개수 + 1, hoja_Orodha);
}
