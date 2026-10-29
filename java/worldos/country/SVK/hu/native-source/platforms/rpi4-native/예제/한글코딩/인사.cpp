#include "파일규약.h"
class üzenet_kezelő {
    int INDEX;
public:
    üzenet_kezelő(const char *Név) : INDEX(készít_Fájl(Név, 읽고쓰기 | 없으면만들기 | vág_Tartalom, 0600)) {}
    ~üzenet_kezelő() { if (INDEX >= 0) bezár_Fájl(INDEX); }
    입출력결과형 Írás(const char *adat, bájt_DARAB_beír Méret) { return ír_Fájl_adat(INDEX, adat, Méret); }
};
extern "C" int START_felhasználó_app(int Argumentumok) {
    (void)Argumentumok;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    üzenet_kezelő 문서("C++인사.txt");
    ír_Fájl_adat(1, 인사말, sizeof(인사말) - 1);
    return 문서.Írás(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
