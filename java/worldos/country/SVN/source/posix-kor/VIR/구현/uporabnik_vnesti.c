#include "호출경계.h"
extern int main(int 인수개수, char **argument_Seznam);
static char argument_pomnilnik[2048];
static char *argument_Seznam[18];
int jkoros_main(void) {
    int element_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (element_COUNT < 0 || element_COUNT > 16) return 126;
    /* sprotno_element 커널의 argv는 Izvedi_ukaz 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Seznam[0] = "jkoros-app";
    int Položaj = 0;
    for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Seznam[INDEX + 1] = argument_pomnilnik + Položaj;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Položaj >= 2047) return 126;
            argument_pomnilnik[Položaj++] = 원본[칸 + 1];
        }
        argument_pomnilnik[Položaj++] = 0;
    }
    argument_Seznam[element_COUNT + 1] = 0;
    return main(element_COUNT + 1, argument_Seznam);
}
