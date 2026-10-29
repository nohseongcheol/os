#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void तयार_करचें_नॅटवर्क(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_वर्ग);
int 망주소묶기(int फायल_हँडल, uint32_t नामो, unsigned 접속번호);
int 연결기다리기(int फायल_हँडल);
void 통신주소재사용(int फायल_हँडल);
int 망연결하기(int फायल_हँडल, uint32_t नामो, unsigned 접속번호);
int 망연결받기(int फायल_हँडल);
int 통신읽기(int फायल_हँडल, void *डेटा, unsigned आयटम_COUNT);
int 통신쓰기(int फायल_हँडल, const void *डेटा, unsigned आयटम_COUNT);
int 전문보내기(int फायल_हँडल, const void *डेटा, unsigned आयटम_COUNT, uint32_t नामो, unsigned 접속번호);
int 전문받기(int फायल_हँडल, void *डेटा, unsigned आयटम_COUNT);
unsigned 통신접속번호(int फायल_हँडल);
unsigned 상대접속번호(int फायल_हँडल);
uint32_t 상대통신주소(int फायल_हँडल);
void शेवट_नॅटवर्क(int फायल_हँडल);
int फायल_ट्रान्सफर_नियंत्रण(int कृती);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned प्रवेश_मोल, unsigned INDEX);
int कॉन्फिगर_नॅटवर्क(unsigned कृती, uint32_t नामो, uint32_t मास्क_मोल, uint32_t गेटवे_मोल);
int 응답시험시작(uint32_t नामो, unsigned क्रम_मोल);
int 응답시험읽기(unsigned प्रवेश_मोल);
#endif
