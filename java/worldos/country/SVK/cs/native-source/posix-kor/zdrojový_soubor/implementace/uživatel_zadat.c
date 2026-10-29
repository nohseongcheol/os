#include "VOLAT_mez.h"
extern int main(int 인수개수, char **argument_Seznam);
static char argument_Paměť[2048];
static char *argument_Seznam[18];
int jkoros_main(void) {
    int zboží_POČET = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (zboží_POČET < 0 || zboží_POČET > 16) return 126;
    /* dobrá_zboží 커널의 argv는 Provést_příkaz 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Seznam[0] = "jkoros-app";
    int pozice = 0;
    for (int INDEX = 0; INDEX < zboží_POČET; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Seznam[INDEX + 1] = argument_Paměť + pozice;
        for (int přihrádka_položka = 0; přihrádka_položka < 원본[0]; přihrádka_položka++) {
            if (pozice >= 2047) return 126;
            argument_Paměť[pozice++] = 원본[přihrádka_položka + 1];
        }
        argument_Paměť[pozice++] = 0;
    }
    argument_Seznam[zboží_POČET + 1] = 0;
    return main(zboží_POČET + 1, argument_Seznam);
}
