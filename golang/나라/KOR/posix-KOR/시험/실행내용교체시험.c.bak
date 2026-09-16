#include <오류번호.h>
#include <자료철제어.h>
#include <체계/자식대기.h>
#include <입출력과실행.h>

static void 전문쓰기(const char *문자열, unsigned int 크기)
{
    (void)쓰기(표준출력번호, 문자열, 크기);
}

int main(void)
{
    int 끝난상태;
    int 자료철서술번호;
    char *인수목록[] = {(char *)"PXEXEC", (char *)"argument", (char *)0};
    char *환경목록[] = {(char *)"POSIX_TEST=1", (char *)0};

    전문쓰기("\nPOSIX-EXEC:START\n", 18);
    오류번호 = 0;
    if (지정자식기다리기(-1, &끝난상태, 준비안되면기다리지않기) == -1 && 오류번호 == 오류자식실행과정없음)
        전문쓰기("PTEST:PASS:waitpid-echild-empty\n", 32);
    else
        전문쓰기("PTEST:FAIL:waitpid-echild-empty\n", 32);
    오류번호 = 0;
    if (자식기다리기(&끝난상태) == -1 && 오류번호 == 오류자식실행과정없음)
        전문쓰기("PTEST:PASS:wait-echild-empty\n", 29);
    else
        전문쓰기("PTEST:FAIL:wait-echild-empty\n", 29);

    자료철서술번호 = 열기("/USER2", 읽기전용열기);
    if (자료철서술번호 < 0 || 지정번호로열린자료참조복제하기(자료철서술번호, 10) != 10 || 자료철제어하기(10, 서술번호표시설정, 실행내용교체때닫기) != 0) {
        전문쓰기("PTEST:FAIL:cloexec-setup\n", 25);
        즉시끝내기(98);
    }
    if (자료철서술번호 != 10)
        (void)닫기(자료철서술번호);

    (void)실행내용바꾸기("/PXEXEC", 인수목록, 환경목록);
    전문쓰기("PTEST:FAIL:exec-image\n", 22);
    즉시끝내기(99);
}
