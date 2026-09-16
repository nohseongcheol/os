/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <통신주소/여덟자리묶음순서.h>
#include <체계/체계호출.h>
#include <체계/통신끝점.h>

enum { 통신끝점체계호출번호 = 102 };
enum {
    통신끝점_통신끝점만들기 = 1, 통신끝점_지역주소맺기 = 2, 통신끝점_상대끝점잇기 = 3, 통신끝점_연결요청받을준비하기 = 4,
    통신끝점_연결요청받기 = 5, 통신끝점_지역끝점주소얻기 = 6, 통신끝점_상대끝점주소얻기 = 7,
    통신끝점_보내기 = 9, 통신끝점_받기 = 10, 통신끝점_목적지로보내기 = 11, 통신끝점_보낸곳과함께받기 = 12,
    통신끝점_통신방향닫기 = 13, 통신끝점_통신끝점설정하기 = 14
};

static long 통신끝점호출하기(long 통신호출번호, unsigned long *전달인수목록)
{
    return __syscall_result(
        __syscall6(통신끝점체계호출번호, 통신호출번호, (long)전달인수목록, 0, 0, 0, 0));
}

부호없는16이진자리정수 통신망순서로16자리바꾸기(부호없는16이진자리정수 값) { return (부호없는16이진자리정수)((값 << 8) | (값 >> 8)); }
부호없는16이진자리정수 기계순서로16자리바꾸기(부호없는16이진자리정수 값) { return 통신망순서로16자리바꾸기(값); }
부호없는32이진자리정수 통신망순서로32자리바꾸기(부호없는32이진자리정수 값)
{
    return ((값 & 0x000000ffU) << 24) | ((값 & 0x0000ff00U) << 8) |
           ((값 & 0x00ff0000U) >> 8) | ((값 & 0xff000000U) >> 24);
}
부호없는32이진자리정수 기계순서로32자리바꾸기(부호없는32이진자리정수 값) { return 통신망순서로32자리바꾸기(값); }

int 통신끝점만들기(int 주소계열, int 끝점종류, int 통신규약)
{
    unsigned long 전달값[3] = {(unsigned long)주소계열, (unsigned long)끝점종류, (unsigned long)통신규약};
    return (int)통신끝점호출하기(통신끝점_통신끝점만들기, 전달값);
}

int 지역주소맺기(int 자료철서술번호, const struct 통신끝점주소 *주소, 주소길이형 길이)
{
    unsigned long 전달값[3] = {(unsigned long)자료철서술번호, (unsigned long)주소, 길이};
    return (int)통신끝점호출하기(통신끝점_지역주소맺기, 전달값);
}

int 상대끝점잇기(int 자료철서술번호, const struct 통신끝점주소 *주소, 주소길이형 길이)
{
    unsigned long 전달값[3] = {(unsigned long)자료철서술번호, (unsigned long)주소, 길이};
    return (int)통신끝점호출하기(통신끝점_상대끝점잇기, 전달값);
}

int 연결요청받을준비하기(int 자료철서술번호, int 대기한도)
{
    unsigned long 전달값[2] = {(unsigned long)자료철서술번호, (unsigned long)대기한도};
    return (int)통신끝점호출하기(통신끝점_연결요청받을준비하기, 전달값);
}

int 연결요청받기(int 자료철서술번호, struct 통신끝점주소 *주소, 주소길이형 *길이)
{
    unsigned long 전달값[3] = {(unsigned long)자료철서술번호, (unsigned long)주소, (unsigned long)길이};
    return (int)통신끝점호출하기(통신끝점_연결요청받기, 전달값);
}

int 지역끝점주소얻기(int 자료철서술번호, struct 통신끝점주소 *주소, 주소길이형 *길이)
{
    unsigned long 전달값[3] = {(unsigned long)자료철서술번호, (unsigned long)주소, (unsigned long)길이};
    return (int)통신끝점호출하기(통신끝점_지역끝점주소얻기, 전달값);
}

int 상대끝점주소얻기(int 자료철서술번호, struct 통신끝점주소 *주소, 주소길이형 *길이)
{
    unsigned long 전달값[3] = {(unsigned long)자료철서술번호, (unsigned long)주소, (unsigned long)길이};
    return (int)통신끝점호출하기(통신끝점_상대끝점주소얻기, 전달값);
}

부호있는크기형 보내기(int 자료철서술번호, const void *자료완충영역, 크기형 길이, int 처리표시)
{
    unsigned long 전달값[4] = {(unsigned long)자료철서술번호, (unsigned long)자료완충영역, 길이, (unsigned long)처리표시};
    return (부호있는크기형)통신끝점호출하기(통신끝점_보내기, 전달값);
}

부호있는크기형 받기(int 자료철서술번호, void *자료완충영역, 크기형 길이, int 처리표시)
{
    unsigned long 전달값[4] = {(unsigned long)자료철서술번호, (unsigned long)자료완충영역, 길이, (unsigned long)처리표시};
    return (부호있는크기형)통신끝점호출하기(통신끝점_받기, 전달값);
}

부호있는크기형 목적지로보내기(int 자료철서술번호, const void *자료완충영역, 크기형 길이, int 처리표시,
               const struct 통신끝점주소 *주소, 주소길이형 주소길이)
{
    unsigned long 전달값[6] = {(unsigned long)자료철서술번호, (unsigned long)자료완충영역, 길이,
                          (unsigned long)처리표시, (unsigned long)주소, 주소길이};
    return (부호있는크기형)통신끝점호출하기(통신끝점_목적지로보내기, 전달값);
}

부호있는크기형 보낸곳과함께받기(int 자료철서술번호, void *자료완충영역, 크기형 길이, int 처리표시,
                 struct 통신끝점주소 *주소, 주소길이형 *주소길이)
{
    unsigned long 전달값[6] = {(unsigned long)자료철서술번호, (unsigned long)자료완충영역, 길이,
                          (unsigned long)처리표시, (unsigned long)주소,
                          (unsigned long)주소길이};
    return (부호있는크기형)통신끝점호출하기(통신끝점_보낸곳과함께받기, 전달값);
}

int 통신방향닫기(int 자료철서술번호, int 닫을방향)
{
    unsigned long 전달값[2] = {(unsigned long)자료철서술번호, (unsigned long)닫을방향};
    return (int)통신끝점호출하기(통신끝점_통신방향닫기, 전달값);
}

int 통신끝점설정하기(int 자료철서술번호, int 설정수준, int 설정이름,
               const void *설정값, 주소길이형 설정크기)
{
    unsigned long 전달값[5] = {(unsigned long)자료철서술번호, (unsigned long)설정수준,
                          (unsigned long)설정이름, (unsigned long)설정값,
                          설정크기};
    return (int)통신끝점호출하기(통신끝점_통신끝점설정하기, 전달값);
}
