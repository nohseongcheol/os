#include <File_ABI.h>
#if defined(__linux__) || !defined(__JKOROS__) || __STDC_HOSTED__
#error This sample must be compiled with the native guest cc command.
#endif

int main(int 인수개수, char **argomento_elenco) {
    if (인수개수 < 1 || !argomento_elenco[0]) return 2;
    const char messaggio_di_saluto[] = "nativo 커널의 C와 Italiano POSIX\n";
    int Guides = aperto_File("messaggio_di_saluto_ae353e94.txt", in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600);
    if (Guides < 0) return 1;
    입출력결과형 durata_VALORE = scrivere_File_dati(Guides, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1);
    Chiudi_File(Guides);
    scrivere_File_dati(1, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1);
    return durata_VALORE == sizeof(messaggio_di_saluto) - 1 ? 0 : 3;
}
