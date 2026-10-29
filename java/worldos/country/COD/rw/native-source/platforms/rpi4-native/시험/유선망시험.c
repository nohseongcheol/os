/* 가짜 MMIO/MDIO 장치로 gukora_mu_matsinda_agaciro umusago_agaciro·uburebure_agaciro·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(aderesi) 저장기[(aderesi)/4]
#define JKOROS_GENET_TEST 1
#include "../Urusobemiyoboro_Ikirundo/y_umugozi_Urusobemiyoboro.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Ijambo_SMS=유선저장기(0xe14);
    if(물리작동&&(Ijambo_SMS&(1u<<29))){unsigned aderesi=(Ijambo_SMS>>21)&31,umugerekashakiro=(Ijambo_SMS>>16)&31;
        if(aderesi!=1)유선저장기(0xe14)=1<<28;
        else{if(((Ijambo_SMS>>26)&3)==1)물리값[umugerekashakiro]=Ijambo_SMS&65535;유선저장기(0xe14)=물리값[umugerekashakiro];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *aderesi){const unsigned char agaciro[]={2,1,2,3,4,5};memcpy(aderesi,agaciro,6);return 1;}
void netif_set_link_up(struct netif *igendanwa_agaciro){igendanwa_agaciro->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *igendanwa_agaciro){igendanwa_agaciro->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *igendanwa_agaciro,struct pbuf *전문,const ip4_addr_t *aderesi){(void)igendanwa_agaciro;(void)전문;(void)aderesi;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer akugara_umugerekashakiro,u16_t 수,pbuf_type 종류){
    (void)akugara_umugerekashakiro;(void)종류;struct pbuf *amakurushingiro=calloc(1,sizeof(*amakurushingiro)+수);assert(amakurushingiro);amakurushingiro->payload=amakurushingiro+1;amakurushingiro->len=amakurushingiro->tot_len=수;return amakurushingiro;
}
u8_t pbuf_free(struct pbuf *amakurushingiro){free(amakurushingiro);return 1;}
err_t pbuf_take(struct pbuf *amakurushingiro,const void *원본,u16_t 수){assert(수<=amakurushingiro->len);memcpy(amakurushingiro->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *amakurushingiro,void *aho_ijya_agaciro,u16_t 수,u16_t ihuriro){assert(ihuriro+수<=amakurushingiro->len);memcpy(aho_ijya_agaciro,(char*)amakurushingiro->payload+ihuriro,수);return 수;}
static err_t kwemera_kwihuza(struct pbuf *amakurushingiro,struct netif *igendanwa_agaciro){(void)igendanwa_agaciro;assert(amakurushingiro->len==60);assert(((unsigned char*)amakurushingiro->payload)[0]==0x42);들어온수++;pbuf_free(amakurushingiro);return ERR_OK;}
int main(void){
    struct netif igendanwa_agaciro;memset(&igendanwa_agaciro,0,sizeof(igendanwa_agaciro));igendanwa_agaciro.input=kwemera_kwihuza;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Gutegura_y_umugozi_Urusobemiyoboro(&igendanwa_agaciro)==ERR_OK);assert(y_umugozi_agaciro.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&igendanwa_agaciro);assert(netif_is_link_up(&igendanwa_agaciro));assert(y_umugozi_agaciro.속도==1000);
    y_umugozi_agaciro.생산=y_umugozi_agaciro.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&igendanwa_agaciro,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=y_umugozi_agaciro.생산;}
    assert(y_umugozi_agaciro.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(y_umugozi_agaciro.kohereza[0][0]==0x42&&y_umugozi_agaciro.kohereza[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(y_umugozi_agaciro.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&igendanwa_agaciro,전문)==ERR_MEM);pbuf_free(전문);
    memset(y_umugozi_agaciro.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&igendanwa_agaciro);assert(들어온수==1&&y_umugozi_agaciro.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&igendanwa_agaciro);
    assert(y_umugozi_agaciro.소비==0&&들어온수==1&&y_umugozi_agaciro.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&igendanwa_agaciro);assert(!netif_is_link_up(&igendanwa_agaciro));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
