#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Gutegura_Urusobemiyoboro(void);
void 통신망살피기(void);
int 통신끝점만들기(int 유형);
int 망주소묶기(int dosiye_umukondo, uint32_t aderesi, unsigned 접속번호);
int 연결기다리기(int dosiye_umukondo);
void 통신주소재사용(int dosiye_umukondo);
int 망연결하기(int dosiye_umukondo, uint32_t aderesi, unsigned 접속번호);
int 망연결받기(int dosiye_umukondo);
int 통신읽기(int dosiye_umukondo, void *amakurushingiro, unsigned 개수);
int 통신쓰기(int dosiye_umukondo, const void *amakurushingiro, unsigned 개수);
int 전문보내기(int dosiye_umukondo, const void *amakurushingiro, unsigned 개수, uint32_t aderesi, unsigned 접속번호);
int 전문받기(int dosiye_umukondo, void *amakurushingiro, unsigned 개수);
unsigned 통신접속번호(int dosiye_umukondo);
unsigned 상대접속번호(int dosiye_umukondo);
uint32_t 상대통신주소(int dosiye_umukondo);
void gufunga_Urusobemiyoboro(int dosiye_umukondo);
int dosiye_iyimura_icunga(int Igikorwa);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned icyinjizwa_agaciro, unsigned umugerekashakiro);
int kuboneza_Urusobemiyoboro(unsigned Igikorwa, uint32_t aderesi, uint32_t masiki_agaciro, uint32_t muhuzaporotokore_agaciro);
int 응답시험시작(uint32_t aderesi, unsigned umujyo_agaciro);
int 응답시험읽기(unsigned icyinjizwa_agaciro);
#endif
