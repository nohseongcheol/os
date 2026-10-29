#include "파일규약.h"
class inyand_Umugenzuzi {
    int umugerekashakiro;
public:
    inyand_Umugenzuzi(const char *Izina) : umugerekashakiro(kurema_dosiye(Izina, gusoma_kwandika | 없으면만들기 | 내용비우기, 0600)) {}
    ~inyand_Umugenzuzi() { if (umugerekashakiro >= 0) gufunga_dosiye(umugerekashakiro); }
    입출력결과형 kwandika(const char *amakurushingiro, 바이트수형 Ingano) { return kwandika_dosiye_amakurushingiro(umugerekashakiro, amakurushingiro, Ingano); }
};
extern "C" int Itangira_ukoresha_porogaramu(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    inyand_Umugenzuzi 문서("C++인사.txt");
    kwandika_dosiye_amakurushingiro(1, 인사말, sizeof(인사말) - 1);
    return 문서.kwandika(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
