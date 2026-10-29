#include "호출경계.h"
extern int main(int 인수개수, char **ágúmẹ́ntì_Àtòkọ);
static char ágúmẹ́ntì_ibi_ìpamọ́[2048];
static char *ágúmẹ́ntì_Àtòkọ[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 ṣiṣẹ́_àṣẹ 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    ágúmẹ́ntì_Àtòkọ[0] = "jkoros-app";
    int 위치 = 0;
    for (int wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 개수; wá_atọ̀ka_àkóónú++) {
        const int *원본 = (const int *)jkoros_syscall(3, wá_atọ̀ka_àkóónú, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        ágúmẹ́ntì_Àtòkọ[wá_atọ̀ka_àkóónú + 1] = ágúmẹ́ntì_ibi_ìpamọ́ + 위치;
        for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < 원본[0]; ààyè_ìfàyọkàsí_ìgbéwọlé++) {
            if (위치 >= 2047) return 126;
            ágúmẹ́ntì_ibi_ìpamọ́[위치++] = 원본[ààyè_ìfàyọkàsí_ìgbéwọlé + 1];
        }
        ágúmẹ́ntì_ibi_ìpamọ́[위치++] = 0;
    }
    ágúmẹ́ntì_Àtòkọ[개수 + 1] = 0;
    return main(개수 + 1, ágúmẹ́ntì_Àtòkọ);
}
