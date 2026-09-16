/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _선언_일반함수
#define _선언_일반함수
#include <기본정의.h>
typedef struct { int 몫; int 나머지; } 정수나눗셈결과형;
typedef struct { long 몫; long 나머지; } 긴정수나눗셈결과형;
#define 성공종료 0
#define 실패종료 1
void *기억공간확보하기(크기형 크기);
void *영으로채운배열공간확보하기(크기형 수량, 크기형 원소크기);
void *기억공간크기바꾸기(void *주소, 크기형 크기);
void 기억공간반납하기(void *주소);
long 문자열을긴정수로읽기(const char *문자열, char **변환끝주소, int 진법밑수);
unsigned long 문자열을부호없는긴정수로읽기(const char *문자열, char **변환끝주소, int 진법밑수);
int 십진문자열을정수로읽기(const char *문자열);
long 십진문자열을긴정수로읽기(const char *문자열);
int 정수절댓값얻기(int 값);
long 긴정수절댓값얻기(long 값);
정수나눗셈결과형 정수몫과나머지얻기(int 왼쪽값, int 오른쪽값);
긴정수나눗셈결과형 긴정수몫과나머지얻기(long 왼쪽값, long 오른쪽값);
void 비교기준으로정렬하기(void *원소배열, 크기형 수량, 크기형 원소크기,
           int (*비교함수)(const void *, const void *));
void *정렬된배열이분탐색하기(const void *원본, const void *원소배열, 크기형 수량,
              크기형 원소크기, int (*비교함수)(const void *, const void *));
char *환경변수값얻기(const char *이름);
#endif
