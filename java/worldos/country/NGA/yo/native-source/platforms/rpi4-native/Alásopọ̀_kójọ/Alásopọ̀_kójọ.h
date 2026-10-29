#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void gbaradì_Alásopọ̀(void);
void 통신망살피기(void);
int 통신끝점만들기(int irú_ìsọ̀rí);
int 망주소묶기(int fáìlì_èkù, uint32_t àdírẹ́ẹ̀sì, unsigned 접속번호);
int 연결기다리기(int fáìlì_èkù);
void 통신주소재사용(int fáìlì_èkù);
int 망연결하기(int fáìlì_èkù, uint32_t àdírẹ́ẹ̀sì, unsigned 접속번호);
int 망연결받기(int fáìlì_èkù);
int 통신읽기(int fáìlì_èkù, void *détà, unsigned 개수);
int 통신쓰기(int fáìlì_èkù, const void *détà, unsigned 개수);
int 전문보내기(int fáìlì_èkù, const void *détà, unsigned 개수, uint32_t àdírẹ́ẹ̀sì, unsigned 접속번호);
int 전문받기(int fáìlì_èkù, void *détà, unsigned 개수);
unsigned 통신접속번호(int fáìlì_èkù);
unsigned 상대접속번호(int fáìlì_èkù);
uint32_t 상대통신주소(int fáìlì_èkù);
void pa_dé_Alásopọ̀(int fáìlì_èkù);
int fáìlì_ṣàgbélọ_ìdarí(int ìṣe);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ìgbéwọlé_iye, unsigned wá_atọ̀ka_àkóónú);
int ṣàtòpọ̀_Alásopọ̀(unsigned ìṣe, uint32_t àdírẹ́ẹ̀sì, uint32_t asẹ́_iye_iye, uint32_t ẹnu_odi_iye);
int 응답시험시작(uint32_t àdírẹ́ẹ̀sì, unsigned ìtodátà_iye);
int 응답시험읽기(unsigned ìgbéwọlé_iye);
#endif
