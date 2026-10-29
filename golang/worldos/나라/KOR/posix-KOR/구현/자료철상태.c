#include <체계/자료철상태.h>
#include <체계/체제정보.h>
#include <체계/체계호출.h>

enum { 체계호출_자료철상태 = 106, 체계호출_연결자체상태얻기 = 107, 체계호출_열린자료철상태얻기 = 108, 체계호출_체제정보얻기 = 122 };

int 자료철상태(const char *경로, struct 자료철상태 *완충영역)
{
    return (int)__syscall_result(
        __syscall6(체계호출_자료철상태, (long)경로, (long)완충영역, 0, 0, 0, 0));
}

int 연결자체상태얻기(const char *경로, struct 자료철상태 *완충영역)
{
    return (int)__syscall_result(
        __syscall6(체계호출_연결자체상태얻기, (long)경로, (long)완충영역, 0, 0, 0, 0));
}

int 열린자료철상태얻기(int 자료철서술번호, struct 자료철상태 *완충영역)
{
    return (int)__syscall_result(
        __syscall6(체계호출_열린자료철상태얻기, 자료철서술번호, (long)완충영역, 0, 0, 0, 0));
}

int 체제정보얻기(struct 체제정보 *이름)
{
    return (int)__syscall_result(
        __syscall6(체계호출_체제정보얻기, (long)이름, 0, 0, 0, 0, 0));
}
