#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Hlela_iNethiwekhi(void);
void 통신망살피기(void);
int 통신끝점만들기(int thayipha_umunxa);
int 망주소묶기(int ifayela_isibambo, uint32_t ikheli, unsigned 접속번호);
int 연결기다리기(int ifayela_isibambo);
void 통신주소재사용(int ifayela_isibambo);
int 망연결하기(int ifayela_isibambo, uint32_t ikheli, unsigned 접속번호);
int 망연결받기(int ifayela_isibambo);
int 통신읽기(int ifayela_isibambo, void *imininingwane, unsigned 개수);
int 통신쓰기(int ifayela_isibambo, const void *imininingwane, unsigned 개수);
int 전문보내기(int ifayela_isibambo, const void *imininingwane, unsigned 개수, uint32_t ikheli, unsigned 접속번호);
int 전문받기(int ifayela_isibambo, void *imininingwane, unsigned 개수);
unsigned 통신접속번호(int ifayela_isibambo);
unsigned 상대접속번호(int ifayela_isibambo);
uint32_t 상대통신주소(int ifayela_isibambo);
void vala_iNethiwekhi(int ifayela_isibambo);
int ifayela_dlulisa_isilawuli(int Isenzo);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned okufakwayo_inani, unsigned thola_inkomba);
int misa_iNethiwekhi(unsigned Isenzo, uint32_t ikheli, uint32_t insitha_inani, uint32_t isango_inani);
int 응답시험시작(uint32_t ikheli, unsigned ukuhleleka_inani);
int 응답시험읽기(unsigned okufakwayo_inani);
#endif
