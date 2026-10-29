#include "Dosya_ABI.h"
class belge_yönetici {
    int Dizin;
public:
    belge_yönetici(const char *İsim) : Dizin(açık_Dosya(İsim, R_W | 없으면만들기 | kesmek_içindekiler, 0600)) {}
    ~belge_yönetici() { if (Dizin >= 0) Kapat_Dosya(Dizin); }
    입출력결과형 Yazma(const char *veri, bayt_BAĞ_DEĞ_SAY_TÜR Boyut) { return yazma_Dosya_veri(Dizin, veri, Boyut); }
};
extern "C" int Start_kullanıcı_program(int bağımsız_değişkenler) {
    (void)bağımsız_değişkenler;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    belge_yönetici 문서("C++인사.txt");
    yazma_Dosya_veri(1, 인사말, sizeof(인사말) - 1);
    return 문서.Yazma(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
