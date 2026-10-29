#include "파일규약.h"
int 사용자시작(int Argumentu) {
    (void)Argumentu;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = 파일열기("C인사.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = 파일자료쓰기(문서, 인사말, sizeof(인사말) - 1);
    파일닫기(문서);
    파일자료쓰기(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
