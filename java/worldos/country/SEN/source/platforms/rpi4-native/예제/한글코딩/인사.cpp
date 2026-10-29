#include "파일규약.h"
class téere_doxalkat {
    int àlluwa_tur;
public:
    téere_doxalkat(const char *tur_253d1510) : àlluwa_tur(sos_bara_denc(tur_253d1510, jàng_bind | 없으면만들기 | 내용비우기, 0600)) {}
    ~téere_doxalkat() { if (àlluwa_tur >= 0) Tej_bara_denc(àlluwa_tur); }
    입출력결과형 biir(const char *mbir, 바이트수형 tolluwaay) { return biir_bara_denc_mbir(àlluwa_tur, mbir, tolluwaay); }
};
extern "C" int Door_kiy_jariñoo_internet_jëfekaay(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    téere_doxalkat 문서("C++인사.txt");
    biir_bara_denc_mbir(1, 인사말, sizeof(인사말) - 1);
    return 문서.biir(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
