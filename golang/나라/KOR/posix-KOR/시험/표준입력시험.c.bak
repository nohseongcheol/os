#include <입출력과실행.h>

static void 전문쓰기(const char *문자열, unsigned int 크기)
{
    (void)쓰기(표준출력번호, 문자열, 크기);
}

int main(void)
{
    char 입력위치[4];
    부호있는크기형 수량;

    전문쓰기("\nPOSIX-STDIN:READY\n", 19);
    수량 = 읽기(표준입력번호, 입력위치, sizeof(입력위치));
    if (수량 == 2 && 입력위치[0] == 'a' && 입력위치[1] == '\n') {
        전문쓰기("POSIX-STDIN:PASS\n", 17);
        즉시끝내기(0);
    }
    전문쓰기("POSIX-STDIN:FAIL\n", 17);
    즉시끝내기(1);
}
