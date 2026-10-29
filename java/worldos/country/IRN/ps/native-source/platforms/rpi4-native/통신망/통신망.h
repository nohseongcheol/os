#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void 통신망준비(void);
void 통신망살피기(void);
int 통신끝점만들기(int 유형);
int 망주소묶기(int دوتنه_لاستى, uint32_t پته, unsigned 접속번호);
int 연결기다리기(int دوتنه_لاستى);
void 통신주소재사용(int دوتنه_لاستى);
int 망연결하기(int دوتنه_لاستى, uint32_t پته, unsigned 접속번호);
int 망연결받기(int دوتنه_لاستى);
int 통신읽기(int دوتنه_لاستى, void *اومتوک, unsigned 개수);
int 통신쓰기(int دوتنه_لاستى, const void *اومتوک, unsigned 개수);
int 전문보내기(int دوتنه_لاستى, const void *اومتوک, unsigned 개수, uint32_t پته, unsigned 접속번호);
int 전문받기(int دوتنه_لاستى, void *اومتوک, unsigned 개수);
unsigned 통신접속번호(int دوتنه_لاستى);
unsigned 상대접속번호(int دوتنه_لاستى);
uint32_t 상대통신주소(int دوتنه_لاستى);
void بندول_جال(int دوتنه_لاستى);
int دوتنه_لېږدول_مهار(int چار);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ننوت_ارزښت, unsigned لړیال);
int سازول_جال(unsigned چار, uint32_t پته, uint32_t وربوزۍ_ارزښت, uint32_t ورلار_ارزښت);
int 응답시험시작(uint32_t پته, unsigned اڼن_اوډون_ارزښت);
int 응답시험읽기(unsigned ننوت_ارزښت);
#endif
