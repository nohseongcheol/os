#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Andaa_Mtandao(void);
void 통신망살피기(void);
int 통신끝점만들기(int aina_kategoria);
int 망주소묶기(int faili_kishiko, uint32_t anwani, unsigned namba_ya_kituo);
int 연결기다리기(int faili_kishiko);
void 통신주소재사용(int faili_kishiko);
int 망연결하기(int faili_kishiko, uint32_t anwani, unsigned namba_ya_kituo);
int 망연결받기(int faili_kishiko);
int 통신읽기(int faili_kishiko, void *data, unsigned 개수);
int 통신쓰기(int faili_kishiko, const void *data, unsigned 개수);
int 전문보내기(int faili_kishiko, const void *data, unsigned 개수, uint32_t anwani, unsigned namba_ya_kituo);
int 전문받기(int faili_kishiko, void *data, unsigned 개수);
unsigned Mtandao_namba_ya_kituo(int faili_kishiko);
unsigned kompyuta_rika_namba_ya_kituo(int faili_kishiko);
uint32_t 상대통신주소(int faili_kishiko);
void funga_Mtandao(int faili_kishiko);
int faili_hamisha_udhibiti(int Kitendo);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned ingizo_thamani, unsigned kielezo);
int sanidi_Mtandao(unsigned Kitendo, uint32_t anwani, uint32_t barakoa_thamani, uint32_t kichanganishi_mtandao_thamani);
int 응답시험시작(uint32_t anwani, unsigned mpangilio_thamani);
int 응답시험읽기(unsigned ingizo_thamani);
#endif
