/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <입출력과실행.h>
int 함수모음동작시험하기(void);
int main(void)
{
    int 실패줄번호 = 함수모음동작시험하기();
    if (실패줄번호) {
        char 자료완충영역[16];
        int 길이 = 0;
        쓰기(1, "POSIX-LIBRARY:FAIL line=", 24);
        do { 자료완충영역[길이++] = (char)('0' + 실패줄번호 % 10); 실패줄번호 /= 10; } while (실패줄번호);
        while (길이) 쓰기(1, &자료완충영역[--길이], 1);
        쓰기(1, "\n", 1);
        return 1;
    }
    return 쓰기(1, "POSIX-LIBRARY:PASS\n", 19) == 19 ? 0 : 1;
}
