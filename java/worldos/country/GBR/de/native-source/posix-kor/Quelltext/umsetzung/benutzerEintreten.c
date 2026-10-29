#include "AufrufVorgangGrenzstelle.h"
extern int main(int argumenteAnzahl, char **argumentListe);
static char argumentSpeicher[2048];
static char *argumentListe[18];
int jkoros_main(void) {
    int elementeintragAnzahl = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (elementeintragAnzahl < 0 || elementeintragAnzahl > 16) return 126;
    /* aktuellElementeintrag 커널의 argv는 befehlAusführen 이름을 제외한다. C argv[0]은 고정 wertIdentifizieren 이름이다. */
    argumentListe[0] = "jkoros-app";
    int position = 0;
    for (int Nummer = 0; Nummer < elementeintragAnzahl; Nummer++) {
        const int *ursprünglich = (const int *)jkoros_syscall(3, Nummer, 0, 0, 0, 0);
        if (!ursprünglich || ursprünglich[0] < 0 || ursprünglich[0] > 127) return 126;
        argumentListe[Nummer + 1] = argumentSpeicher + position;
        for (int platzEintrag = 0; platzEintrag < ursprünglich[0]; platzEintrag++) {
            if (position >= 2047) return 126;
            argumentSpeicher[position++] = ursprünglich[platzEintrag + 1];
        }
        argumentSpeicher[position++] = 0;
    }
    argumentListe[elementeintragAnzahl + 1] = 0;
    return main(elementeintragAnzahl + 1, argumentListe);
}
