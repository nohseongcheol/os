/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <일반함수.h>
#include <문자열과기억내용.h>
#include <문자분류.h>
#include <오류번호.h>
#include <정수한계.h>
#include <입출력과실행.h>

static int 숫자값구하기(unsigned char 문자값)
{
    if (십진숫자인지확인하기(문자값)) return 문자값 - '0';
    if (영문자인지확인하기(문자값)) return 소문자로바꾸기(문자값) - 'a' + 10;
    return 36;
}

static unsigned long 부호없는수해석하기(const char *문자열, char **변환끝주소,
                                    int 진법밑수, int 부호없음여부, int *음수여부, int *범위초과여부)
{
    const char *진행위치 = 문자열, *첫일치위치;
    unsigned long 크기값 = 0, 최댓값;
    int 숫자값;
    if (변환끝주소) *변환끝주소 = (char *)문자열;
    *음수여부 = 0;
    *범위초과여부 = 0;
    if (진법밑수 && (진법밑수 < 2 || 진법밑수 > 36)) { 오류번호 = 오류전달값잘못됨; return 0; }
    while (공백문자인지확인하기((unsigned char)*진행위치)) ++진행위치;
    if (*진행위치 == '+' || *진행위치 == '-') { *음수여부 = *진행위치 == '-'; ++진행위치; }
    if ((진법밑수 == 0 || 진법밑수 == 16) && 진행위치[0] == '0' &&
        (진행위치[1] == 'x' || 진행위치[1] == 'X') && 숫자값구하기((unsigned char)진행위치[2]) < 16) {
        진행위치 += 2; 진법밑수 = 16;
    }
    if (!진법밑수) 진법밑수 = *진행위치 == '0' ? 8 : 10;
    최댓값 = 부호없음여부 ? 부호없는긴정수최댓값 : (unsigned long)긴정수최댓값 + (unsigned long)*음수여부;
    첫일치위치 = 진행위치;
    while ((숫자값 = 숫자값구하기((unsigned char)*진행위치)) < 진법밑수) {
        if (크기값 > (최댓값 - (unsigned long)숫자값) / (unsigned long)진법밑수)
            *범위초과여부 = 1;
        else if (!*범위초과여부)
            크기값 = 크기값 * (unsigned long)진법밑수 + (unsigned long)숫자값;
        ++진행위치;
    }
    if (진행위치 == 첫일치위치) return 0;
    if (변환끝주소) *변환끝주소 = (char *)진행위치;
    if (*범위초과여부) { 오류번호 = 오류값범위벗어남; return 최댓값; }
    return 크기값;
}

long 문자열을긴정수로읽기(const char *문자열, char **변환끝주소, int 진법밑수)
{
    int 음수여부, 범위초과여부;
    unsigned long 크기값 = 부호없는수해석하기(문자열, 변환끝주소, 진법밑수, 0, &음수여부, &범위초과여부);
    if (!음수여부) return (long)크기값;
    return 크기값 == (unsigned long)긴정수최댓값 + 1UL ? 긴정수최솟값 : -(long)크기값;
}

unsigned long 문자열을부호없는긴정수로읽기(const char *문자열, char **변환끝주소, int 진법밑수)
{
    int 음수여부, 범위초과여부;
    unsigned long 크기값 = 부호없는수해석하기(문자열, 변환끝주소, 진법밑수, 1, &음수여부, &범위초과여부);
    if (범위초과여부) return 부호없는긴정수최댓값;
    return 음수여부 ? 0UL - 크기값 : 크기값;
}

int 십진문자열을정수로읽기(const char *문자열) { return (int)문자열을긴정수로읽기(문자열, 빈주소, 10); }
long 십진문자열을긴정수로읽기(const char *문자열) { return 문자열을긴정수로읽기(문자열, 빈주소, 10); }
int 정수절댓값얻기(int 값) { return 값 < 0 ? -값 : 값; }
long 긴정수절댓값얻기(long 값) { return 값 < 0 ? -값 : 값; }
정수나눗셈결과형 정수몫과나머지얻기(int 왼쪽값, int 오른쪽값) { 정수나눗셈결과형 결과 = {왼쪽값 / 오른쪽값, 왼쪽값 % 오른쪽값}; return 결과; }
긴정수나눗셈결과형 긴정수몫과나머지얻기(long 왼쪽값, long 오른쪽값) { 긴정수나눗셈결과형 결과 = {왼쪽값 / 오른쪽값, 왼쪽값 % 오른쪽값}; return 결과; }

static void 원소맞바꾸기(unsigned char *왼쪽값, unsigned char *오른쪽값, 크기형 원소크기)
{
    while (원소크기--) { unsigned char 임시값 = *왼쪽값; *왼쪽값++ = *오른쪽값; *오른쪽값++ = 임시값; }
}

static void 아래로정렬맞추기(unsigned char *원소배열, 크기형 내려갈자리, 크기형 수량,
                      크기형 원소크기, int (*비교함수)(const void *, const void *))
{
    while (내려갈자리 < 수량 / 2) {
        크기형 자식자리 = 내려갈자리 * 2 + 1;
        if (자식자리 + 1 < 수량 && 비교함수(원소배열 + 자식자리 * 원소크기, 원소배열 + (자식자리 + 1) * 원소크기) < 0)
            ++자식자리;
        if (비교함수(원소배열 + 내려갈자리 * 원소크기, 원소배열 + 자식자리 * 원소크기) >= 0) return;
        원소맞바꾸기(원소배열 + 내려갈자리 * 원소크기, 원소배열 + 자식자리 * 원소크기, 원소크기);
        내려갈자리 = 자식자리;
    }
}

void 비교기준으로정렬하기(void *원소배열, 크기형 수량, 크기형 원소크기,
           int (*비교함수)(const void *, const void *))
{
    unsigned char *진행위치 = 원소배열;
    크기형 순번;
    if (수량 < 2 || !원소크기 || 수량 > (크기형)-1 / 원소크기) return;
    /* Heap sort: bounded stack, O(n log n), comparator receives array elements. */
    for (순번 = 수량 / 2; 순번; ) 아래로정렬맞추기(진행위치, --순번, 수량, 원소크기, 비교함수);
    for (순번 = 수량 - 1; 순번; --순번) {
        원소맞바꾸기(진행위치, 진행위치 + 순번 * 원소크기, 원소크기);
        아래로정렬맞추기(진행위치, 0, 순번, 원소크기, 비교함수);
    }
}

void *정렬된배열이분탐색하기(const void *원본, const void *원소배열, 크기형 수량,
              크기형 원소크기, int (*비교함수)(const void *, const void *))
{
    크기형 아래경계 = 0, 위경계 = 수량;
    const unsigned char *진행위치 = 원소배열;
    if (!원소크기 || 수량 > (크기형)-1 / 원소크기) return 빈주소;
    while (아래경계 < 위경계) {
        크기형 가운데위치 = 아래경계 + (위경계 - 아래경계) / 2;
        int 결과 = 비교함수(원본, 진행위치 + 가운데위치 * 원소크기);
        if (!결과) return (void *)(진행위치 + 가운데위치 * 원소크기);
        if (결과 < 0) 위경계 = 가운데위치;
        else 아래경계 = 가운데위치 + 1;
    }
    return 빈주소;
}

char *환경변수값얻기(const char *이름)
{
    크기형 길이 = 문자열여덟자리묶음길이얻기(이름);
    char **진행위치 = 환경변수목록;
    if (!길이 || 문자열에서첫값찾기(이름, '=') || !진행위치) return 빈주소;
    while (*진행위치) {
        if (!한도내문자열비교하기(*진행위치, 이름, 길이) && (*진행위치)[길이] == '=') return *진행위치 + 길이 + 1;
        ++진행위치;
    }
    return 빈주소;
}
