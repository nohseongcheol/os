#include "Połącz_granica.h"
extern int main(int 인수개수, char **argument_Lista);
static char argument_Pamięć[2048];
static char *argument_Lista[18];
int jkoros_main(void) {
    int towar_ILE_LICZB = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (towar_ILE_LICZB < 0 || towar_ILE_LICZB > 16) return 126;
    /* bieżący_towar 커널의 argv는 Wykonaj_polecenie 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Lista[0] = "jkoros-app";
    int pozycja = 0;
    for (int INDEKS = 0; INDEKS < towar_ILE_LICZB; INDEKS++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEKS, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Lista[INDEKS + 1] = argument_Pamięć + pozycja;
        for (int gniazdo_wpis = 0; gniazdo_wpis < 원본[0]; gniazdo_wpis++) {
            if (pozycja >= 2047) return 126;
            argument_Pamięć[pozycja++] = 원본[gniazdo_wpis + 1];
        }
        argument_Pamięć[pozycja++] = 0;
    }
    argument_Lista[towar_ILE_LICZB + 1] = 0;
    return main(towar_ILE_LICZB + 1, argument_Lista);
}
