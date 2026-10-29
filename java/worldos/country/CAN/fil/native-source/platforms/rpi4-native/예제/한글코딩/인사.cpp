#include "파일규약.h"
class doc_tagapamahala {
    int INDEX;
public:
    doc_tagapamahala(const char *pangalan) : INDEX(buksan_file(pangalan, nababasa_nasusulatan | 없으면만들기 | 내용비우기, 0600)) {}
    ~doc_tagapamahala() { if (INDEX >= 0) isara_file(INDEX); }
    입출력결과형 sumulat(const char *data, byte_COUNT_TYPE sukat_82232621) { return sumulat_file_data(INDEX, data, sukat_82232621); }
};
extern "C" int Start_gumagamit_app(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    doc_tagapamahala 문서("C++인사.txt");
    sumulat_file_data(1, 인사말, sizeof(인사말) - 1);
    return 문서.sumulat(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
