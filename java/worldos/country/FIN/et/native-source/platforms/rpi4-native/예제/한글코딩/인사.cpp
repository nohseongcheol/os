#include "파일규약.h"
class 문서관리 {
    int INDEX;
public:
    문서관리(const char *Nimi_2) : INDEX(avama_Fail(Nimi_2, 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600)) {}
    ~문서관리() { if (INDEX >= 0) Sule_Fail(INDEX); }
    입출력결과형 Kirjutamine(const char *andmed, bait_COUNT_TYPE Suurus) { return kirjutamine_Fail_andmed(INDEX, andmed, Suurus); }
};
extern "C" int START_kasutaja_programm(int Argumendid) {
    (void)Argumendid;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    문서관리 문서("C++인사.txt");
    kirjutamine_Fail_andmed(1, 인사말, sizeof(인사말) - 1);
    return 문서.Kirjutamine(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
