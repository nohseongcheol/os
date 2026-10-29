#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Kwado_Netwọọkụ(void);
void 통신망살피기(void);
int 통신끝점만들기(int pinye_otu);
int 망주소묶기(int ọbọakwụkwọ_ebenjìaka, uint32_t àdreèsì, unsigned 접속번호);
int 연결기다리기(int ọbọakwụkwọ_ebenjìaka);
void 통신주소재사용(int ọbọakwụkwọ_ebenjìaka);
int 망연결하기(int ọbọakwụkwọ_ebenjìaka, uint32_t àdreèsì, unsigned 접속번호);
int 망연결받기(int ọbọakwụkwọ_ebenjìaka);
int 통신읽기(int ọbọakwụkwọ_ebenjìaka, void *datà, unsigned 개수);
int 통신쓰기(int ọbọakwụkwọ_ebenjìaka, const void *datà, unsigned 개수);
int 전문보내기(int ọbọakwụkwọ_ebenjìaka, const void *datà, unsigned 개수, uint32_t àdreèsì, unsigned 접속번호);
int 전문받기(int ọbọakwụkwọ_ebenjìaka, void *datà, unsigned 개수);
unsigned 통신접속번호(int ọbọakwụkwọ_ebenjìaka);
unsigned 상대접속번호(int ọbọakwụkwọ_ebenjìaka);
uint32_t 상대통신주소(int ọbọakwụkwọ_ebenjìaka);
void mmechi_Netwọọkụ(int ọbọakwụkwọ_ebenjìaka);
int ọbọakwụkwọ_dògharịa_njizi(int mmèm);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ndebà_valuu, unsigned indèks);
int hàkọọ_ngwaāhụ_kọmputa_Netwọọkụ(unsigned mmèm, uint32_t àdreèsì, uint32_t mkpù_valuu, uint32_t ụzọmbànye_valuu);
int 응답시험시작(uint32_t àdreèsì, unsigned ùsòrò_valuu);
int 응답시험읽기(unsigned ndebà_valuu);
#endif
