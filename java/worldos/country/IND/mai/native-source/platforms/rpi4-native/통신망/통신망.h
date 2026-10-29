#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void 통신망준비(void);
void 통신망살피기(void);
int 통신끝점만들기(int 유형);
int 망주소묶기(int 파일기술자, uint32_t 주소, unsigned 접속번호);
int 연결기다리기(int 파일기술자);
void 통신주소재사용(int 파일기술자);
int 망연결하기(int 파일기술자, uint32_t 주소, unsigned 접속번호);
int 망연결받기(int 파일기술자);
int 통신읽기(int 파일기술자, void *자료, unsigned 개수);
int 통신쓰기(int 파일기술자, const void *자료, unsigned 개수);
int 전문보내기(int 파일기술자, const void *자료, unsigned 개수, uint32_t 주소, unsigned 접속번호);
int 전문받기(int 파일기술자, void *자료, unsigned 개수);
unsigned 통신접속번호(int 파일기술자);
unsigned 상대접속번호(int 파일기술자);
uint32_t 상대통신주소(int 파일기술자);
void 통신닫기(int 파일기술자);
int 파일전송제어(int क्रिया);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned 항목, unsigned 번호);
int 망설정하기(unsigned क्रिया, uint32_t 주소, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t 주소, unsigned 순서);
int 응답시험읽기(unsigned 항목);
#endif
