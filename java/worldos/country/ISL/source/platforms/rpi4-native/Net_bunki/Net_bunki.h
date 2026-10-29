#ifndef 자체통신망머리
#define 자체통신망머리
#include <stdint.h>
#include <stddef.h>
void Undirbúa_Net(void);
void 통신망살피기(void);
int 통신끝점만들기(int TYPE_tegund);
int nettó_BIND(int skrá_hald, uint32_t slóð, unsigned tengisnúmer);
int nettó_hlusta(int skrá_hald);
void 통신주소재사용(int skrá_hald);
int nettó_TENGJA(int skrá_hald, uint32_t slóð, unsigned tengisnúmer);
int nettó_samþykkja(int skrá_hald);
int 통신읽기(int skrá_hald, void *gögn, unsigned vara_COUNT);
int nettó_skrifa(int skrá_hald, const void *gögn, unsigned vara_COUNT);
int 전문보내기(int skrá_hald, const void *gögn, unsigned vara_COUNT, uint32_t slóð, unsigned tengisnúmer);
int 전문받기(int skrá_hald, void *gögn, unsigned vara_COUNT);
unsigned Net_tengisnúmer(int skrá_hald);
unsigned jafningi_tengisnúmer(int skrá_hald);
uint32_t nettó_jafningi_slóð(int skrá_hald);
void loka_Net(int skrá_hald);
int skrá_flytja_stýring(int Aðgerð);
void 파일전송살피기(void);
uint32_t 망상태읽기(unsigned færsla_VALUE, unsigned INDEX);
int grunnstilla_Net(unsigned Aðgerð, uint32_t slóð, uint32_t sía_VALUE_3fef50ae, uint32_t gátt_VALUE_cfee51e8);
int 응답시험시작(uint32_t slóð, unsigned röð_VALUE);
int 응답시험읽기(unsigned færsla_VALUE);
#endif
