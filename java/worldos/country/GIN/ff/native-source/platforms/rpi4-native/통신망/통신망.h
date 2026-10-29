#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Heblu_laylaytol(void);
void 통신망살피기(void);
int 통신끝점만들기(int 유형);
int 망주소묶기(int fiilde_jaggoode, uint32_t ñiiɓirde, unsigned 접속번호);
int 연결기다리기(int fiilde_jaggoode);
void 통신주소재사용(int fiilde_jaggoode);
int 망연결하기(int fiilde_jaggoode, uint32_t ñiiɓirde, unsigned 접속번호);
int 망연결받기(int fiilde_jaggoode);
int 통신읽기(int fiilde_jaggoode, void *keɓe, unsigned 개수);
int 통신쓰기(int fiilde_jaggoode, const void *keɓe, unsigned 개수);
int 전문보내기(int fiilde_jaggoode, const void *keɓe, unsigned 개수, uint32_t ñiiɓirde, unsigned 접속번호);
int 전문받기(int fiilde_jaggoode, void *keɓe, unsigned 개수);
unsigned 통신접속번호(int fiilde_jaggoode);
unsigned 상대접속번호(int fiilde_jaggoode);
uint32_t 상대통신주소(int fiilde_jaggoode);
void uddude_laylaytol(int fiilde_jaggoode);
int fiilde_egginde_yuurnitorde(int gollal);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned naatnugol_njaru, unsigned joopirdu);
int heblude_laylaytol(unsigned gollal, uint32_t ñiiɓirde, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t ñiiɓirde, unsigned deggondiral_njaru);
int 응답시험읽기(unsigned naatnugol_njaru);
#endif
