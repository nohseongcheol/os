#include <자료철제어.h>
#include <체계/체계호출.h>

enum { 체계호출_열기 = 5, 체계호출_자료철만들기 = 8, 체계호출_자료철제어하기 = 55 };

int 열기(const char *경로, int 열기선택, ...)
{
    자료철방식형 접근방식 = 0;
    if ((열기선택 & 없으면만들기) != 0) {
        __builtin_va_list 가변인수;
        __builtin_va_start(가변인수, 열기선택);
        접근방식 = __builtin_va_arg(가변인수, 자료철방식형);
        __builtin_va_end(가변인수);
    }
    return (int)__syscall_result(
        __syscall6(체계호출_열기, (long)경로, 열기선택, 접근방식, 0, 0, 0));
}

int 자료철만들기(const char *경로, 자료철방식형 접근방식)
{
    return (int)__syscall_result(
        __syscall6(체계호출_자료철만들기, (long)경로, 접근방식, 0, 0, 0, 0));
}

int 자료철제어하기(int 자료철서술번호, int 제어명령, ...)
{
    long 인수값 = 0;
    if (제어명령 == 서술번호복제 || 제어명령 == 서술번호표시설정 || 제어명령 == 자료철상태표시설정) {
        __builtin_va_list 가변인수;
        __builtin_va_start(가변인수, 제어명령);
        인수값 = __builtin_va_arg(가변인수, long);
        __builtin_va_end(가변인수);
    }
    return (int)__syscall_result(
        __syscall6(체계호출_자료철제어하기, 자료철서술번호, 제어명령, 인수값, 0, 0, 0));
}
