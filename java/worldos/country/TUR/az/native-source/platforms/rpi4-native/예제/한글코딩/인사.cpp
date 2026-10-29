#include "파일규약.h"
class sənəd_menecer {
    int INDEX;
public:
    sənəd_menecer(const char *Ad) : INDEX(açmaq_fayl(Ad, oxunan_yazılan | 없으면만들기 | 내용비우기, 0600)) {}
    ~sənəd_menecer() { if (INDEX >= 0) bağlamaq_fayl(INDEX); }
    입출력결과형 Yazma(const char *verilənlər, bayt_COUNT_TYPE Böyüklük) { return yazmaq_fayl_verilənlər(INDEX, verilənlər, Böyüklük); }
};
extern "C" int Başla_istifadəçi_proqram(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    sənəd_menecer 문서("C++인사.txt");
    yazmaq_fayl_verilənlər(1, 인사말, sizeof(인사말) - 1);
    return 문서.Yazma(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
