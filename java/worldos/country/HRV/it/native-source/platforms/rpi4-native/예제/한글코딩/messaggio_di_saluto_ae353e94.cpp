#include "File_ABI.h"
class Gestione_documenti {
    int INDICE;
public:
    Gestione_documenti(const char *Nome) : INDICE(aperto_File(Nome, in_lettura_scrittura | 없으면만들기 | tagliare_Sommario, 0600)) {}
    ~Gestione_documenti() { if (INDICE >= 0) Chiudi_File(INDICE); }
    입출력결과형 Scrittura(const char *dati, byte_CONTA_NUMERI_TIPO Dimensione) { return scrivere_File_dati(INDICE, dati, Dimensione); }
};
extern "C" int START_USER_app(int argomenti) {
    (void)argomenti;
    const char messaggio_di_saluto[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    Gestione_documenti Guides("C++messaggio_di_saluto_ae353e94.txt");
    scrivere_File_dati(1, messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1);
    return Guides.Scrittura(messaggio_di_saluto, sizeof(messaggio_di_saluto) - 1) == sizeof(messaggio_di_saluto) - 1 ? 0 : 1;
}
