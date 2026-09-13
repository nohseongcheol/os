#include <입출력과실행.h>
#include <자료철제어.h>
#include <오류번호.h>
#include <체계/자료철상태.h>
int 함수모음동작시험하기(void);

int main(void)
{
    char 자료완충영역[16];
    /* USER2 is the ELF fixture installed by the boot harness, not user data. */
    int 자료철서술번호 = 열기("/USER2", 읽기전용열기);
    struct 자료철상태 상태자료;
    if (자료철서술번호 < 0 || 열린자료철상태얻기(자료철서술번호, &상태자료) < 0 || 읽기(자료철서술번호, 자료완충영역, 4) != 4 ||
        (unsigned char)자료완충영역[0] != 0x7f || 자료완충영역[1] != 'E' || 자료완충영역[2] != 'L' || 자료완충영역[3] != 'F' ||
        자료위치옮기기(자료철서술번호, 0, 처음기준위치) != 0 || 닫기(자료철서술번호) < 0 || 실행과정번호얻기() <= 0)
        goto 실패여부;
    오류번호 = 0;
    if (읽기(-1, 자료완충영역, 1) != -1 || 오류번호 != 오류서술번호잘못됨)
        goto 실패여부;
    if (함수모음동작시험하기() != 0)
        goto 실패여부;
    if (쓰기(표준출력번호, "POSIX-NATIVE:PASS\n", 18) != 18)
        goto 실패여부;
    return 0;
실패여부:
    쓰기(표준출력번호, "POSIX-NATIVE:FAIL\n", 18);
    return 1;
}
