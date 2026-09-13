#ifndef _선언_입출력과실행
#define _선언_입출력과실행

#include <기본정의.h>
#include <체계/자료형.h>

#define 표준입력번호 0
#define 표준출력번호 1
#define 표준오류출력번호 2
#define 존재확인 0
#define 실행권한확인 1
#define 쓰기권한확인 2
#define 읽기권한확인 4
#define 처음기준위치 0
#define 현재기준위치 1
#define 끝기준위치 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **환경변수목록;
void 즉시끝내기(int 끝난상태) __attribute__((noreturn));
부호있는크기형 읽기(int 자료철서술번호, void *완충영역, 크기형 수량);
부호있는크기형 쓰기(int 자료철서술번호, const void *완충영역, 크기형 수량);
int 닫기(int 자료철서술번호);
자료위치형 자료위치옮기기(int 자료철서술번호, 자료위치형 위치차이, int 위치기준);
실행과정번호형 실행과정갈라내기(void);
int 실행내용바꾸기(const char *경로, char *const 인수목록[], char *const 환경목록[]);
실행과정번호형 실행과정번호얻기(void);
실행과정번호형 부모실행과정번호얻기(void);
사용자번호형 사용자번호얻기(void);
사용자번호형 유효사용자번호얻기(void);
무리번호형 무리번호얻기(void);
무리번호형 유효무리번호얻기(void);
int 접근권한확인하기(const char *경로, int 접근방식);
int 작업목록바꾸기(const char *경로);
char *작업목록경로얻기(char *완충영역, 크기형 크기);
int 열린자료참조복제하기(int 자료철서술번호);
int 지정번호로열린자료참조복제하기(int 기존서술번호, int 새서술번호);
int 자료철기록맞추기(int 자료철서술번호);
void 모든기록맞추기(void);
int 단말인지확인하기(int 자료철서술번호);
int 동적기억끝정하기(void *주소);
void *동적기억끝옮기기(int 증가량);
#ifdef __cplusplus
}
#endif

#endif
