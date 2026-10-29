#include "파일규약.h"
class 문서관리 {
    int INDEX;
public:
    문서관리(const char *Nosaukums) : INDEX(atvērt_Fails(Nosaukums, 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600)) {}
    ~문서관리() { if (INDEX >= 0) Aizvērt_Fails(INDEX); }
    입출력결과형 Rakstīt(const char *dati, byte_COUNT_TYPE Izmērs) { return rakstīšana_Fails_dati(INDEX, dati, Izmērs); }
};
extern "C" int Sākt_lietotājs_programma(int Parametri) {
    (void)Parametri;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    문서관리 문서("C++인사.txt");
    rakstīšana_Fails_dati(1, 인사말, sizeof(인사말) - 1);
    return 문서.Rakstīt(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
