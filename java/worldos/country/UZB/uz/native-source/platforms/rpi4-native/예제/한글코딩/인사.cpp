#include "파일규약.h"
class hujjat_menejer {
    int INDEX;
public:
    hujjat_menejer(const char *Nomi) : INDEX(ochmoq_fayl(Nomi, o_qish_yozish_mumkin | 없으면만들기 | 내용비우기, 0600)) {}
    ~hujjat_menejer() { if (INDEX >= 0) yopmoq_fayl(INDEX); }
    입출력결과형 Yozish(const char *ma_lumotlar, bayt_COUNT_TYPE Hajmi) { return yozmoq_fayl_ma_lumotlar(INDEX, ma_lumotlar, Hajmi); }
};
extern "C" int Start_foydalanuvchi_ilova(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    hujjat_menejer 문서("C++인사.txt");
    yozmoq_fayl_ma_lumotlar(1, 인사말, sizeof(인사말) - 1);
    return 문서.Yozish(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
