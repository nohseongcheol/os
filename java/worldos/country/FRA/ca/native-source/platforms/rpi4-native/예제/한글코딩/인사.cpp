#include "파일규약.h"
class document_administrador {
    int INDEX;
public:
    document_administrador(const char *Nom) : INDEX(crear_arxiu(Nom, lectura_escriptura | 없으면만들기 | 내용비우기, 0600)) {}
    ~document_administrador() { if (INDEX >= 0) Tanca_arxiu(INDEX); }
    입출력결과형 Escriptura(const char *dades, byte_COMPT_TIPUS Mida) { return escriure_arxiu_dades(INDEX, dades, Mida); }
};
extern "C" int Inici_usuari_programa(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    document_administrador 문서("C++인사.txt");
    escriure_arxiu_dades(1, 인사말, sizeof(인사말) - 1);
    return 문서.Escriptura(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
