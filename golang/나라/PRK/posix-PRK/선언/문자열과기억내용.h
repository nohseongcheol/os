/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _선언_문자열과기억내용
#define _선언_문자열과기억내용
#include <기본정의.h>
void *기억내용복사하기(void *옮길곳, const void *원본, 크기형 길이);
void *겹침허용기억내용옮기기(void *옮길곳, const void *원본, 크기형 길이);
void *기억영역값채우기(void *옮길곳, int 문자값, 크기형 길이);
int 기억내용비교하기(const void *왼쪽값, const void *오른쪽값, 크기형 길이);
void *기억영역에서값찾기(const void *원본, int 문자값, 크기형 길이);
크기형 문자열여덟자리묶음길이얻기(const char *문자열);
크기형 한도내문자열여덟자리묶음길이얻기(const char *문자열, 크기형 한도);
char *문자열복사하기(char *옮길곳, const char *원본);
char *한도만큼문자열채워복사하기(char *옮길곳, const char *원본, 크기형 한도);
char *문자열복사뒤끝얻기(char *옮길곳, const char *원본);
char *한도만큼채워복사뒤끝얻기(char *옮길곳, const char *원본, 크기형 한도);
char *문자열덧붙이기(char *옮길곳, const char *원본);
char *한도내문자열덧붙이기(char *옮길곳, const char *원본, 크기형 한도);
int 문자열비교하기(const char *왼쪽값, const char *오른쪽값);
int 한도내문자열비교하기(const char *왼쪽값, const char *오른쪽값, 크기형 한도);
int 정렬규칙으로문자열비교하기(const char *왼쪽값, const char *오른쪽값);
크기형 문자열정렬키만들기(char *옮길곳, const char *원본, 크기형 한도);
char *문자열에서첫값찾기(const char *문자열, int 문자값);
char *문자열에서끝값찾기(const char *문자열, int 문자값);
char *문자열에서부분문자열찾기(const char *문자열, const char *원본);
크기형 허용값으로된앞부분길이얻기(const char *문자열, const char *구분값집합);
크기형 제외값없는앞부분길이얻기(const char *문자열, const char *구분값집합);
char *문자열에서집합값찾기(const char *문자열, const char *구분값집합);
char *문자열낱말나누기(char *문자열, const char *구분값집합);
char *진행상태지정문자열낱말나누기(char *문자열, const char *구분값집합, char **저장된진행상태);
char *문자열새공간에복제하기(const char *문자열);
char *한도내문자열새공간에복제하기(const char *문자열, 크기형 한도);
#endif
