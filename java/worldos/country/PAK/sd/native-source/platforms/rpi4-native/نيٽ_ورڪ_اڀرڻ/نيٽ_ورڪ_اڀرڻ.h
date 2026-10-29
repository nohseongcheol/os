#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void تياري_ڪريو_نيٽ_ورڪ(void);
void 통신망살피기(void);
int 통신끝점만들기(int قسم_قسم);
int 망주소묶기(int فائل_منهن_ڏيڻ, uint32_t پتو, unsigned 접속번호);
int 연결기다리기(int فائل_منهن_ڏيڻ);
void 통신주소재사용(int فائل_منهن_ڏيڻ);
int 망연결하기(int فائل_منهن_ڏيڻ, uint32_t پتو, unsigned 접속번호);
int 망연결받기(int فائل_منهن_ڏيڻ);
int 통신읽기(int فائل_منهن_ڏيڻ, void *ڪوائف, unsigned 개수);
int 통신쓰기(int فائل_منهن_ڏيڻ, const void *ڪوائف, unsigned 개수);
int 전문보내기(int فائل_منهن_ڏيڻ, const void *ڪوائف, unsigned 개수, uint32_t پتو, unsigned 접속번호);
int 전문받기(int فائل_منهن_ڏيڻ, void *ڪوائف, unsigned 개수);
unsigned 통신접속번호(int فائل_منهن_ڏيڻ);
unsigned 상대접속번호(int فائل_منهن_ڏيڻ);
uint32_t 상대통신주소(int فائل_منهن_ڏيڻ);
void بند_ڪرڻ_نيٽ_ورڪ(int فائل_منهن_ڏيڻ);
int فائل_منتقلي_ڪنٽرول(int عمل);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned داخلا_قدر, unsigned ابتدائي);
int جوڙيو_نيٽ_ورڪ(unsigned عمل, uint32_t پتو, uint32_t 가림, uint32_t 관문);
int 응답시험시작(uint32_t پتو, unsigned ترتيب_قدر);
int 응답시험읽기(unsigned داخلا_قدر);
#endif
