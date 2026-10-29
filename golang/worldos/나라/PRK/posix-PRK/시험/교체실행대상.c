#include <오류번호.h>
#include <자료철제어.h>
#include <입출력과실행.h>

static int 문자열같은지(const char *왼쪽값, const char *오른쪽값)
{
    unsigned int 항목순번 = 0;
    while (왼쪽값[항목순번] != 0 && 오른쪽값[항목순번] != 0) {
        if (왼쪽값[항목순번] != 오른쪽값[항목순번])
            return 0;
        항목순번++;
    }
    return 왼쪽값[항목순번] == 오른쪽값[항목순번];
}

int main(int 인수수, char **인수목록, char **환경목록)
{
    static const char 불러온값[] = "PTEST:PASS:exec-image\n";
    static const char 인수검사성공[] = "PTEST:PASS:exec-argv-envp\n";
    static const char 인수검사실패[] = "PTEST:FAIL:exec-argv-envp\n";

    (void)쓰기(표준출력번호, 불러온값, sizeof(불러온값) - 1);
    if (인수수 == 2 && 인수목록 != (char **)0 && 환경목록 != (char **)0 &&
        인수목록[0] != (char *)0 && 인수목록[1] != (char *)0 && 인수목록[2] == (char *)0 &&
        환경목록[0] != (char *)0 && 환경목록[1] == (char *)0 &&
        환경변수목록 == 환경목록 && 문자열같은지(인수목록[0], "PXEXEC") &&
        문자열같은지(인수목록[1], "argument") && 문자열같은지(환경목록[0], "POSIX_TEST=1")) {
        (void)쓰기(표준출력번호, 인수검사성공, sizeof(인수검사성공) - 1);
    } else {
        (void)쓰기(표준출력번호, 인수검사실패, sizeof(인수검사실패) - 1);
        즉시끝내기(38);
    }
    오류번호 = 0;
    if (자료철제어하기(10, 서술번호표시얻기) == -1 && 오류번호 == 오류서술번호잘못됨) {
        static const char 실행교체때닫기성공[] = "PTEST:PASS:cloexec\n";
        (void)쓰기(표준출력번호, 실행교체때닫기성공, sizeof(실행교체때닫기성공) - 1);
        즉시끝내기(37);
    }
    {
        static const char 실행교체때닫기실패[] = "PTEST:FAIL:cloexec\n";
        (void)쓰기(표준출력번호, 실행교체때닫기실패, sizeof(실행교체때닫기실패) - 1);
    }
    즉시끝내기(39);
}
