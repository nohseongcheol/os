#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Parnalli_Kasuqatigiitsimajut(void);
void 통신망살피기(void);
int 통신끝점만들기(int qanuittuuninga_Ataqatigiivvik);
int 망주소묶기(int ini_nuuttarut, uint32_t turaarut, unsigned 접속번호);
int 연결기다리기(int ini_nuuttarut);
void 통신주소재사용(int ini_nuuttarut);
int 망연결하기(int ini_nuuttarut, uint32_t turaarut, unsigned 접속번호);
int 망연결받기(int ini_nuuttarut);
int 통신읽기(int ini_nuuttarut, void *titiqqat, unsigned 개수);
int 통신쓰기(int ini_nuuttarut, const void *titiqqat, unsigned 개수);
int 전문보내기(int ini_nuuttarut, const void *titiqqat, unsigned 개수, uint32_t turaarut, unsigned 접속번호);
int 전문받기(int ini_nuuttarut, void *titiqqat, unsigned 개수);
unsigned 통신접속번호(int ini_nuuttarut);
unsigned 상대접속번호(int ini_nuuttarut);
uint32_t 상대통신주소(int ini_nuuttarut);
void matuli_Kasuqatigiitsimajut(int ini_nuuttarut);
int ini_aullaaqtilli_aulattivik(int sugiarut);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned Iliniku_atuutilik, unsigned nalunaiqsimavik);
int qarasaujarmut_aaqqissurli_Kasuqatigiitsimajut(unsigned sugiarut, uint32_t turaarut, uint32_t kiinappak_atuutilik, uint32_t aqqusiurut_atuutilik);
int 응답시험시작(uint32_t turaarut, unsigned agguijjut_atuutilik);
int 응답시험읽기(unsigned Iliniku_atuutilik);
#endif
