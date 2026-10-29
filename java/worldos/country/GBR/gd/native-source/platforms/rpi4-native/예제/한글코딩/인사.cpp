#include "파일규약.h"
class doc_manaidsear {
    int INDEX;
public:
    doc_manaidsear(const char *Ainm) : INDEX(fosgail_faidhle(Ainm, so_leughte_so_sgrìobhte | 없으면만들기 | 내용비우기, 0600)) {}
    ~doc_manaidsear() { if (INDEX >= 0) dùin_faidhle(INDEX); }
    입출력결과형 sgrìobh(const char *dàta, baidht_COUNT_TYPE atharraich_am_meud) { return sgrìobh_faidhle_dàta(INDEX, dàta, atharraich_am_meud); }
};
extern "C" int Start_cleachdaiche_ap(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    doc_manaidsear 문서("C++인사.txt");
    sgrìobh_faidhle_dàta(1, 인사말, sizeof(인사말) - 1);
    return 문서.sgrìobh(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
