/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _선언_자료철제어
#define _선언_자료철제어

#include <체계/자료형.h>

#define 읽기전용열기 0x0000
#define 쓰기전용열기 0x0001
#define 읽고쓰기열기 0x0002
#define 접근방식가림값 0x0003
#define 없으면만들기 0x0040
#define 새자료철만허용 0x0080
#define 기존내용비우기 0x0200
#define 끝에덧붙이기 0x0400
#define 목록만허용 0x10000

#define 서술번호복제 0
#define 서술번호표시얻기 1
#define 서술번호표시설정 2
#define 자료철상태표시얻기 3
#define 자료철상태표시설정 4
#define 실행내용교체때닫기 1

#ifdef __cplusplus
extern "C" {
#endif
int 열기(const char *경로, int 열기선택, ...);
int 자료철만들기(const char *경로, 자료철방식형 접근방식);
int 자료철제어하기(int 자료철서술번호, int 제어명령, ...);
#ifdef __cplusplus
}
#endif

#endif
