#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void lungisa_Inethiwekhi(void);
void 통신망살피기(void);
int 통신끝점만들기(int uhlobo_udidi);
int 망주소묶기(int ifayile_isibambi, uint32_t idilesi, unsigned 접속번호);
int 연결기다리기(int ifayile_isibambi);
void 통신주소재사용(int ifayile_isibambi);
int 망연결하기(int ifayile_isibambi, uint32_t idilesi, unsigned 접속번호);
int 망연결받기(int ifayile_isibambi);
int 통신읽기(int ifayile_isibambi, void *iingcombolo, unsigned 개수);
int 통신쓰기(int ifayile_isibambi, const void *iingcombolo, unsigned 개수);
int 전문보내기(int ifayile_isibambi, const void *iingcombolo, unsigned 개수, uint32_t idilesi, unsigned 접속번호);
int 전문받기(int ifayile_isibambi, void *iingcombolo, unsigned 개수);
unsigned 통신접속번호(int ifayile_isibambi);
unsigned 상대접속번호(int ifayile_isibambi);
uint32_t 상대통신주소(int ifayile_isibambi);
void vala_Inethiwekhi(int ifayile_isibambi);
int ifayile_gqithisela_isilawuli(int Intshukumo);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ufako_nkcukacha_ixabiso, unsigned indeksa);
int lungiselela_Inethiwekhi(unsigned Intshukumo, uint32_t idilesi, uint32_t imaskhi_ixabiso, uint32_t isango_lekhompyutha_ixabiso);
int 응답시험시작(uint32_t idilesi, unsigned ulandelelwano_ixabiso);
int 응답시험읽기(unsigned ufako_nkcukacha_ixabiso);
#endif
