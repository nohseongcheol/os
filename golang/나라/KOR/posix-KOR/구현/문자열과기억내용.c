/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <문자열과기억내용.h>
#include <문자열대소비교.h>
#include <일반함수.h>
#include <정수형.h>
#include <문자분류.h>

void *기억내용복사하기(void *옮길곳, const void *원본, 크기형 길이)
{
    unsigned char *진행위치 = 옮길곳;
    const unsigned char *입력위치 = 원본;
    while (길이--) *진행위치++ = *입력위치++;
    return 옮길곳;
}

void *겹침허용기억내용옮기기(void *옮길곳, const void *원본, 크기형 길이)
{
    unsigned char *진행위치 = 옮길곳;
    const unsigned char *입력위치 = 원본;
    if ((주소크기부호없는정수)옮길곳 <= (주소크기부호없는정수)원본)
        return 기억내용복사하기(옮길곳, 원본, 길이);
    while (길이) { --길이; 진행위치[길이] = 입력위치[길이]; }
    return 옮길곳;
}

void *기억영역값채우기(void *옮길곳, int 문자값, 크기형 길이)
{
    unsigned char *진행위치 = 옮길곳;
    while (길이--) *진행위치++ = (unsigned char)문자값;
    return 옮길곳;
}

int 기억내용비교하기(const void *왼쪽값, const void *오른쪽값, 크기형 길이)
{
    const unsigned char *진행위치 = 왼쪽값, *입력위치 = 오른쪽값;
    while (길이--) {
        if (*진행위치 != *입력위치) return (int)*진행위치 - (int)*입력위치;
        ++진행위치; ++입력위치;
    }
    return 0;
}

void *기억영역에서값찾기(const void *원본, int 문자값, 크기형 길이)
{
    const unsigned char *진행위치 = 원본;
    while (길이--) {
        if (*진행위치 == (unsigned char)문자값) return (void *)진행위치;
        ++진행위치;
    }
    return 빈주소;
}

크기형 문자열여덟자리묶음길이얻기(const char *문자열)
{
    const char *진행위치 = 문자열;
    while (*진행위치) ++진행위치;
    return (크기형)(진행위치 - 문자열);
}

크기형 한도내문자열여덟자리묶음길이얻기(const char *문자열, 크기형 한도)
{
    크기형 길이 = 0;
    while (길이 < 한도 && 문자열[길이]) ++길이;
    return 길이;
}

char *문자열복사뒤끝얻기(char *옮길곳, const char *원본)
{
    while ((*옮길곳 = *원본) != 0) { ++옮길곳; ++원본; }
    return 옮길곳;
}

char *문자열복사하기(char *옮길곳, const char *원본)
{
    문자열복사뒤끝얻기(옮길곳, 원본);
    return 옮길곳;
}

char *한도만큼채워복사뒤끝얻기(char *옮길곳, const char *원본, 크기형 한도)
{
    크기형 길이 = 한도내문자열여덟자리묶음길이얻기(원본, 한도);
    기억내용복사하기(옮길곳, 원본, 길이);
    기억영역값채우기(옮길곳 + 길이, 0, 한도 - 길이);
    return 옮길곳 + 길이;
}

char *한도만큼문자열채워복사하기(char *옮길곳, const char *원본, 크기형 한도)
{
    한도만큼채워복사뒤끝얻기(옮길곳, 원본, 한도);
    return 옮길곳;
}

char *문자열덧붙이기(char *옮길곳, const char *원본)
{
    문자열복사뒤끝얻기(옮길곳 + 문자열여덟자리묶음길이얻기(옮길곳), 원본);
    return 옮길곳;
}

char *한도내문자열덧붙이기(char *옮길곳, const char *원본, 크기형 한도)
{
    char *진행위치 = 옮길곳 + 문자열여덟자리묶음길이얻기(옮길곳);
    크기형 길이 = 한도내문자열여덟자리묶음길이얻기(원본, 한도);
    기억내용복사하기(진행위치, 원본, 길이);
    진행위치[길이] = 0;
    return 옮길곳;
}

int 문자열비교하기(const char *왼쪽값, const char *오른쪽값)
{
    while (*왼쪽값 && *왼쪽값 == *오른쪽값) { ++왼쪽값; ++오른쪽값; }
    return (int)(unsigned char)*왼쪽값 - (int)(unsigned char)*오른쪽값;
}

int 한도내문자열비교하기(const char *왼쪽값, const char *오른쪽값, 크기형 한도)
{
    while (한도--) {
        int 결과 = (int)(unsigned char)*왼쪽값 - (int)(unsigned char)*오른쪽값;
        if (결과 || !*왼쪽값) return 결과;
        ++왼쪽값; ++오른쪽값;
    }
    return 0;
}

/* The only active locale in this runtime is the initial C/POSIX locale. */
int 정렬규칙으로문자열비교하기(const char *왼쪽값, const char *오른쪽값) { return 문자열비교하기(왼쪽값, 오른쪽값); }

크기형 문자열정렬키만들기(char *옮길곳, const char *원본, 크기형 한도)
{
    크기형 길이 = 문자열여덟자리묶음길이얻기(원본);
    if (한도) {
        크기형 복사길이 = 길이 < 한도 ? 길이 : 한도;
        기억내용복사하기(옮길곳, 원본, 복사길이);
        if (길이 < 한도) 옮길곳[길이] = 0;
    }
    return 길이;
}

char *문자열에서첫값찾기(const char *문자열, int 문자값)
{
    do {
        if (*문자열 == (char)문자값) return (char *)문자열;
    } while (*문자열++);
    return 빈주소;
}

char *문자열에서끝값찾기(const char *문자열, int 문자값)
{
    char *찾은위치 = 빈주소;
    do { if (*문자열 == (char)문자값) 찾은위치 = (char *)문자열; } while (*문자열++);
    return 찾은위치;
}

char *문자열에서부분문자열찾기(const char *문자열, const char *원본)
{
    크기형 길이 = 문자열여덟자리묶음길이얻기(원본);
    if (!길이) return (char *)문자열;
    while (*문자열) {
        if (한도내문자열비교하기(문자열, 원본, 길이) == 0) return (char *)문자열;
        ++문자열;
    }
    return 빈주소;
}

크기형 허용값으로된앞부분길이얻기(const char *문자열, const char *구분값집합)
{
    크기형 길이 = 0;
    while (문자열[길이] && 문자열에서첫값찾기(구분값집합, 문자열[길이])) ++길이;
    return 길이;
}

크기형 제외값없는앞부분길이얻기(const char *문자열, const char *구분값집합)
{
    크기형 길이 = 0;
    while (문자열[길이] && !문자열에서첫값찾기(구분값집합, 문자열[길이])) ++길이;
    return 길이;
}

char *문자열에서집합값찾기(const char *문자열, const char *구분값집합)
{
    const char *진행위치 = 문자열 + 제외값없는앞부분길이얻기(문자열, 구분값집합);
    return *진행위치 ? (char *)진행위치 : 빈주소;
}

char *진행상태지정문자열낱말나누기(char *문자열, const char *구분값집합, char **저장된진행상태)
{
    char *진행위치 = 문자열 ? 문자열 : *저장된진행상태;
    if (!진행위치) return 빈주소;
    진행위치 += 허용값으로된앞부분길이얻기(진행위치, 구분값집합);
    if (!*진행위치) { *저장된진행상태 = 진행위치; return 빈주소; }
    문자열 = 진행위치;
    진행위치 += 제외값없는앞부분길이얻기(진행위치, 구분값집합);
    if (*진행위치) *진행위치++ = 0;
    *저장된진행상태 = 진행위치;
    return 문자열;
}

char *문자열낱말나누기(char *문자열, const char *구분값집합)
{
    static char *저장된진행상태;
    return 진행상태지정문자열낱말나누기(문자열, 구분값집합, &저장된진행상태);
}

char *한도내문자열새공간에복제하기(const char *문자열, 크기형 한도)
{
    크기형 길이 = 한도내문자열여덟자리묶음길이얻기(문자열, 한도);
    char *옮길곳 = 기억공간확보하기(길이 + 1);
    if (옮길곳) { 기억내용복사하기(옮길곳, 문자열, 길이); 옮길곳[길이] = 0; }
    return 옮길곳;
}

char *문자열새공간에복제하기(const char *문자열) { return 한도내문자열새공간에복제하기(문자열, 문자열여덟자리묶음길이얻기(문자열)); }

int 한도내대소문자구별없이비교하기(const char *왼쪽값, const char *오른쪽값, 크기형 한도)
{
    while (한도--) {
        int 결과 = 소문자로바꾸기((unsigned char)*왼쪽값) - 소문자로바꾸기((unsigned char)*오른쪽값);
        if (결과 || !*왼쪽값) return 결과;
        ++왼쪽값; ++오른쪽값;
    }
    return 0;
}

int 대소문자구별없이비교하기(const char *왼쪽값, const char *오른쪽값)
{
    while (*왼쪽값 && 소문자로바꾸기((unsigned char)*왼쪽값) == 소문자로바꾸기((unsigned char)*오른쪽값)) { ++왼쪽값; ++오른쪽값; }
    return 소문자로바꾸기((unsigned char)*왼쪽값) - 소문자로바꾸기((unsigned char)*오른쪽값);
}
