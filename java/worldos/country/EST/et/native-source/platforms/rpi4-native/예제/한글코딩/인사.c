#include "파일규약.h"
int START_kasutaja_programm(int Argumendid) {
    (void)Argumendid;
    const char 인사말[] = "C에서 한글 이름과 posix-kor 호출\n";
    int 문서 = avama_Fail("C인사.txt", 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600);
    if (문서 < 0) return 1;
    입출력결과형 기록한수 = kirjutamine_Fail_andmed(문서, 인사말, sizeof(인사말) - 1);
    Sule_Fail(문서);
    kirjutamine_Fail_andmed(1, 인사말, sizeof(인사말) - 1);
    return 기록한수 == sizeof(인사말) - 1 ? 0 : 2;
}
