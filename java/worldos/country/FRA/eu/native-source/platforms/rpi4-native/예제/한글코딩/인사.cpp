#include "파일규약.h"
class dok_kudeatzaile {
    int INDIZE;
public:
    dok_kudeatzaile(const char *Izena) : INDIZE(ireki_fitxategi(Izena, irakurri_idatzi | 없으면만들기 | 내용비우기, 0600)) {}
    ~dok_kudeatzaile() { if (INDIZE >= 0) itxi_fitxategi(INDIZE); }
    입출력결과형 Idatzi(const char *datuak, byte_ZENBATU_MOTA Tamaina) { return idatzi_fitxategi_datuak(INDIZE, datuak, Tamaina); }
};
extern "C" int HASI_erabiltzaile_aplik(int Argumentuak) {
    (void)Argumentuak;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dok_kudeatzaile 문서("C++인사.txt");
    idatzi_fitxategi_datuak(1, 인사말, sizeof(인사말) - 1);
    return 문서.Idatzi(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
