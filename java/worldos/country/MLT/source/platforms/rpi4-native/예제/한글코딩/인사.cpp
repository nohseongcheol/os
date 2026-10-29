#include "파일규약.h"
class dokument_maniġer {
    int INDEX;
public:
    dokument_maniġer(const char *isem) : INDEX(fetaħ_fajl(isem, qari_kitba | 없으면만들기 | 내용비우기, 0600)) {}
    ~dokument_maniġer() { if (INDEX >= 0) agħlaq_fajl(INDEX); }
    입출력결과형 kiteb(const char *data, byte_COUNT_TYPE daqqas) { return kiteb_fajl_data(INDEX, data, daqqas); }
};
extern "C" int Bidu_utent_programm(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dokument_maniġer 문서("C++인사.txt");
    kiteb_fajl_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.kiteb(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
