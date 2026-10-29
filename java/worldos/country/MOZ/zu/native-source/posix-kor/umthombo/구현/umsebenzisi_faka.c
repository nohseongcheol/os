#include "호출경계.h"
extern int main(int 인수개수, char **i_agumenti_Uhlu);
static char i_agumenti_inkumbulo[2048];
static char *i_agumenti_Uhlu[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 yenza_umyalo 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    i_agumenti_Uhlu[0] = "jkoros-app";
    int 위치 = 0;
    for (int thola_inkomba = 0; thola_inkomba < 개수; thola_inkomba++) {
        const int *원본 = (const int *)jkoros_syscall(3, thola_inkomba, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        i_agumenti_Uhlu[thola_inkomba + 1] = i_agumenti_inkumbulo + 위치;
        for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < 원본[0]; isikhala_okufakwayo++) {
            if (위치 >= 2047) return 126;
            i_agumenti_inkumbulo[위치++] = 원본[isikhala_okufakwayo + 1];
        }
        i_agumenti_inkumbulo[위치++] = 0;
    }
    i_agumenti_Uhlu[개수 + 1] = 0;
    return main(개수 + 1, i_agumenti_Uhlu);
}
