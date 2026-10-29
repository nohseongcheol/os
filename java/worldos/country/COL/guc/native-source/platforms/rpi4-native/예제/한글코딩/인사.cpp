#include "파일규약.h"
class 문서관리 {
    int ee_iyatialujuna;
public:
    문서관리(const char *이름) : ee_iyatialujuna(파일열기(이름, 읽고쓰기 | 없으면만들기 | 내용비우기, 0600)) {}
    ~문서관리() { if (ee_iyatialujuna >= 0) asürülaa_anaajaalaa(ee_iyatialujuna); }
    입출력결과형 ashajaa(const char *atijaaya, 바이트수형 크기) { return ashajaa_anaajaalaa_atijaaya(ee_iyatialujuna, atijaaya, 크기); }
};
extern "C" int achuwalaa_ka_yataayakalü_akumajiaa(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    문서관리 문서("C++인사.txt");
    ashajaa_anaajaalaa_atijaaya(1, 인사말, sizeof(인사말) - 1);
    return 문서.ashajaa(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
