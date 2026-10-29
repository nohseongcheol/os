#ifndef _선언_체계_통신끝점
#define _선언_체계_통신끝점

#include <기본정의.h>
#include <체계/자료형.h>

typedef unsigned short 주소계열형;

struct 통신끝점주소 {
    주소계열형 끝점주소계열;
    char 주소자료[14];
};

#define 주소계열미지정 0
#define 상호연결망주소계열 2
#define 상호연결망규약계열 상호연결망주소계열

#define 자료흐름끝점 1
#define 자료전문끝점 2

#define 수신중단 0
#define 송신중단 1
#define 양방향중단 2

#ifdef __cplusplus
extern "C" {
#endif
int 통신끝점만들기(int 주소계열, int 끝점종류, int 통신규약);
int 지역주소맺기(int 자료철서술번호, const struct 통신끝점주소 *주소, 주소길이형 주소크기);
int 상대끝점잇기(int 자료철서술번호, const struct 통신끝점주소 *주소, 주소길이형 주소크기);
int 연결요청받을준비하기(int 자료철서술번호, int 대기한도);
int 연결요청받기(int 자료철서술번호, struct 통신끝점주소 *주소, 주소길이형 *주소크기);
int 지역끝점주소얻기(int 자료철서술번호, struct 통신끝점주소 *주소, 주소길이형 *주소크기);
int 상대끝점주소얻기(int 자료철서술번호, struct 통신끝점주소 *주소, 주소길이형 *주소크기);
부호있는크기형 보내기(int 자료철서술번호, const void *자료완충영역, 크기형 길이, int 처리표시);
부호있는크기형 받기(int 자료철서술번호, void *자료완충영역, 크기형 길이, int 처리표시);
부호있는크기형 목적지로보내기(int 자료철서술번호, const void *전문, 크기형 길이, int 처리표시,
               const struct 통신끝점주소 *목적지주소, 주소길이형 목적지주소길이);
부호있는크기형 보낸곳과함께받기(int 자료철서술번호, void *자료완충영역, 크기형 길이, int 처리표시,
                 struct 통신끝점주소 *주소, 주소길이형 *주소크기);
int 통신방향닫기(int 자료철서술번호, int 닫을방향);
int 통신끝점설정하기(int 자료철서술번호, int 설정수준, int 설정이름,
               const void *설정값, 주소길이형 설정크기);
#ifdef __cplusplus
}
#endif

#endif
