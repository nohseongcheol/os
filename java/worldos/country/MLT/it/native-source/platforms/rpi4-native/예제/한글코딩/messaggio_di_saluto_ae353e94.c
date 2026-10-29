#include "File_ABI.h"
int START_USER_app(int argomenti) {
    (void)argomenti;
    const char messaggio_di_saluto[] = "C에서 한글 이름과 posix-kor 호출\n";
    int Guides = aperto_File("C인사.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (Guides < 0) return 1;
    입출력결과형 기록한수 = scrivere_File_dati(Guides, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1);
    Chiudi_File(Guides);
    scrivere_File_dati(1, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1);
    return 기록한수 == sizeof(messaggio_di_saluto) - 1 ? 0 : 2;
}
