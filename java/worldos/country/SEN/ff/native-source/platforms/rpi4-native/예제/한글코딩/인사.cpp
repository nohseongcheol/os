#include "파일규약.h"
class fiilannde_kisnoowo {
    int joopirdu;
public:
    fiilannde_kisnoowo(const char *innde) : joopirdu(udditde_fiilde(innde, tar_winndu | 없으면만들기 | 내용비우기, 0600)) {}
    ~fiilannde_kisnoowo() { if (joopirdu >= 0) uddude_fiilde(joopirdu); }
    입출력결과형 winndude(const char *keɓe, 바이트수형 waylude_etannde) { return winndude_fiilde_keɓe(joopirdu, keɓe, waylude_etannde); }
};
extern "C" int huɓɓude_kuutoro_tafirde(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    fiilannde_kisnoowo 문서("C++인사.txt");
    winndude_fiilde_keɓe(1, 인사말, sizeof(인사말) - 1);
    return 문서.winndude(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
