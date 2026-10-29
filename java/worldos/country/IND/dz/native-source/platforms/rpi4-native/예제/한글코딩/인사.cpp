#include "파일규약.h"
class 문서관리 {
    int 번호;
public:
    문서관리(const char *མིང) : 번호(파일열기(མིང, 읽고쓰기 | 없으면만들기 | 내용비우기, 0600)) {}
    ~문서관리() { if (번호 >= 0) 파일닫기(번호); }
    입출력결과형 བྲིས(const char *자료, 바이트수형 ཚད) { return 파일자료쓰기(번호, 자료, ཚད); }
};
extern "C" int 사용자시작(int 인수) {
    (void)인수;
    const char 인사말[] = "C++에서 한글 클래스와 posix-kor 호출\n";
    문서관리 문서("C++인사.txt");
    파일자료쓰기(1, 인사말, sizeof(인사말) - 1);
    return 문서.བྲིས(인사말, sizeof(인사말) - 1) == sizeof(인사말) - 1 ? 0 : 1;
}
