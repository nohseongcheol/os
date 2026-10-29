#include "파일규약.h"
class dọkụment_njikwa {
    int indèks;
public:
    dọkụment_njikwa(const char *Aha) : indèks(mepee_ọbọakwụkwọ(Aha, gụọ_dèe | 없으면만들기 | 내용비우기, 0600)) {}
    ~dọkụment_njikwa() { if (indèks >= 0) mmechi_ọbọakwụkwọ(indèks); }
    입출력결과형 Chekwaa_ozi(const char *datà, 바이트수형 Ụhara) { return dee_ọbọakwụkwọ_datà(indèks, datà, Ụhara); }
};
extern "C" int Mbido_òjìàrụ_app(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    dọkụment_njikwa 문서("C++인사.txt");
    dee_ọbọakwụkwọ_datà(1, 인사말, sizeof(인사말) - 1);
    return 문서.Chekwaa_ozi(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
