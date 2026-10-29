#include <오류번호.h>
#include <체계/체계호출.h>

int 오류번호;
char **환경변수목록;

long __syscall_result(long 결과)
{
    if ((unsigned long)결과 >= (unsigned long)-4095) {
        오류번호 = (int)-결과;
        return -1;
    }
    return 결과;
}
