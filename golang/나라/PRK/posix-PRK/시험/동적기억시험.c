/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <체계/자식대기.h>
#include <입출력과실행.h>

static void 전문쓰기(const char *문자열, unsigned int 크기)
{
    (void)쓰기(표준출력번호, 문자열, 크기);
}

int main(void)
{
    volatile unsigned char *시작위치 = (volatile unsigned char *)동적기억끝옮기기(0);
    volatile unsigned char *기억영역;
    실행과정번호형 자식자리;
    int 끝난상태;

    전문쓰기("\nPOSIX-HEAP:START\n", 18);
    기억영역 = (volatile unsigned char *)동적기억끝옮기기(32);
    if (시작위치 == (void *)-1 || 기억영역 != 시작위치 || 동적기억끝옮기기(0) != (void *)(시작위치 + 32)) {
        전문쓰기("PTEST:FAIL:sbrk-grow\n", 22);
        즉시끝내기(1);
    }
    전문쓰기("PTEST:PASS:sbrk-grow\n", 22);
    기억영역[0] = 0x5a;
    기억영역[31] = 0xa5;
    if (기억영역[0] != 0x5a || 기억영역[31] != 0xa5) {
        전문쓰기("PTEST:FAIL:sbrk-memory\n", 24);
        즉시끝내기(1);
    }
    전문쓰기("PTEST:PASS:sbrk-memory\n", 24);
    if (동적기억끝정하기((void *)시작위치) != 0 || 동적기억끝옮기기(0) != (void *)시작위치) {
        전문쓰기("PTEST:FAIL:brk-restore\n", 24);
        즉시끝내기(1);
    }
    전문쓰기("PTEST:PASS:brk-restore\n", 24);

    자식자리 = 실행과정갈라내기();
    if (자식자리 == 0) {
        if (동적기억끝옮기기(64) != (void *)시작위치)
            즉시끝내기(2);
        즉시끝내기(0);
    }
    if (자식자리 < 0 || 지정자식기다리기(자식자리, &끝난상태, 0) != 자식자리 ||
        !정상종료인지확인(끝난상태) || 종료값꺼내기(끝난상태) != 0 ||
        동적기억끝옮기기(0) != (void *)시작위치) {
        전문쓰기("PTEST:FAIL:brk-process-isolation\n", 33);
        즉시끝내기(1);
    }
    전문쓰기("PTEST:PASS:brk-process-isolation\n", 33);
    전문쓰기("POSIX-HEAP:PASS\n", 16);
    즉시끝내기(0);
}
