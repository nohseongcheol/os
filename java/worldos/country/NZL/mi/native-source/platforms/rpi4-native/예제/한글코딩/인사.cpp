#include "파일규약.h"
class tuhinga_pouwhakahaere {
    int INDEX;
public:
    tuhinga_pouwhakahaere(const char *Ingoa) : INDEX(tiwhikete_kōnae(Ingoa, 읽고쓰기 | 없으면만들기 | 내용비우기, 0600)) {}
    ~tuhinga_pouwhakahaere() { if (INDEX >= 0) kati_kōnae(INDEX); }
    입출력결과형 Tuhia(const char *raraunga, paita_COUNT_TYPE rahi) { return tuhi_kōnae_raraunga(INDEX, raraunga, rahi); }
};
extern "C" int Start_kaiwhakamahi_kaupapa(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    tuhinga_pouwhakahaere 문서("C++인사.txt");
    tuhi_kōnae_raraunga(1, 인사말, sizeof(인사말) - 1);
    return 문서.Tuhia(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
