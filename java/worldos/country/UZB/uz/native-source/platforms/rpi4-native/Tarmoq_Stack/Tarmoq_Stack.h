#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Tayyorlamoq_Tarmoq(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_toifa);
int 망주소묶기(int fayl_deskriptor, uint32_t manzil, unsigned 접속번호);
int 연결기다리기(int fayl_deskriptor);
void 통신주소재사용(int fayl_deskriptor);
int 망연결하기(int fayl_deskriptor, uint32_t manzil, unsigned 접속번호);
int 망연결받기(int fayl_deskriptor);
int 통신읽기(int fayl_deskriptor, void *ma_lumotlar, unsigned element_COUNT);
int 통신쓰기(int fayl_deskriptor, const void *ma_lumotlar, unsigned element_COUNT);
int 전문보내기(int fayl_deskriptor, const void *ma_lumotlar, unsigned element_COUNT, uint32_t manzil, unsigned 접속번호);
int 전문받기(int fayl_deskriptor, void *ma_lumotlar, unsigned element_COUNT);
unsigned 통신접속번호(int fayl_deskriptor);
unsigned 상대접속번호(int fayl_deskriptor);
uint32_t 상대통신주소(int fayl_deskriptor);
void yopmoq_Tarmoq(int fayl_deskriptor);
int fayl_uzatish_boshqaruv(int Amal);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned kiritish_VALUE, unsigned INDEX);
int sozlamoq_Tarmoq(unsigned Amal, uint32_t manzil, uint32_t niqob_VALUE, uint32_t shluz_VALUE);
int 응답시험시작(uint32_t manzil, unsigned tartib_VALUE);
int 응답시험읽기(unsigned kiritish_VALUE);
#endif
