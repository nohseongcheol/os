/* 가짜 MMIO/MDIO 장치로 memmenwè_valuu njubigaoke_valuu·ogologo_valuu·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t 저장기[0x10000/4];
#define 유선저장기(àdreèsì) 저장기[(àdreèsì)/4]
#define JKOROS_GENET_TEST 1
#include "../Netwọọkụ_ikpo/èjìrìwayàrụ_Netwọọkụ.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Mkpụrụokwu_SMS=유선저장기(0xe14);
    if(물리작동&&(Mkpụrụokwu_SMS&(1u<<29))){unsigned àdreèsì=(Mkpụrụokwu_SMS>>21)&31,indèks=(Mkpụrụokwu_SMS>>16)&31;
        if(àdreèsì!=1)유선저장기(0xe14)=1<<28;
        else{if(((Mkpụrụokwu_SMS>>26)&3)==1)물리값[indèks]=Mkpụrụokwu_SMS&65535;유선저장기(0xe14)=물리값[indèks];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *àdreèsì){const unsigned char valuu[]={2,1,2,3,4,5};memcpy(àdreèsì,valuu,6);return 1;}
void netif_set_link_up(struct netif *njìarụ_valuu){njìarụ_valuu->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *njìarụ_valuu){njìarụ_valuu->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *njìarụ_valuu,struct pbuf *전문,const ip4_addr_t *àdreèsì){(void)njìarụ_valuu;(void)전문;(void)àdreèsì;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer òkpùkpù_indèks,u16_t 수,pbuf_type 종류){
    (void)òkpùkpù_indèks;(void)종류;struct pbuf *datà=calloc(1,sizeof(*datà)+수);assert(datà);datà->payload=datà+1;datà->len=datà->tot_len=수;return datà;
}
u8_t pbuf_free(struct pbuf *datà){free(datà);return 1;}
err_t pbuf_take(struct pbuf *datà,const void *원본,u16_t 수){assert(수<=datà->len);memcpy(datà->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *datà,void *ebemwèga_valuu,u16_t 수,u16_t Bido){assert(Bido+수<=datà->len);memcpy(ebemwèga_valuu,(char*)datà->payload+Bido,수);return 수;}
static err_t nabata_njikọ(struct pbuf *datà,struct netif *njìarụ_valuu){(void)njìarụ_valuu;assert(datà->len==60);assert(((unsigned char*)datà->payload)[0]==0x42);들어온수++;pbuf_free(datà);return ERR_OK;}
int main(void){
    struct netif njìarụ_valuu;memset(&njìarụ_valuu,0,sizeof(njìarụ_valuu));njìarụ_valuu.input=nabata_njikọ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Kwado_èjìrìwayàrụ_Netwọọkụ(&njìarụ_valuu)==ERR_OK);assert(èjìrìwayàrụ_valuu.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&njìarụ_valuu);assert(netif_is_link_up(&njìarụ_valuu));assert(èjìrìwayàrụ_valuu.속도==1000);
    èjìrìwayàrụ_valuu.생산=èjìrìwayàrụ_valuu.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&njìarụ_valuu,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=èjìrìwayàrụ_valuu.생산;}
    assert(èjìrìwayàrụ_valuu.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(èjìrìwayàrụ_valuu.zìga[0][0]==0x42&&èjìrìwayàrụ_valuu.zìga[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(èjìrìwayàrụ_valuu.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&njìarụ_valuu,전문)==ERR_MEM);pbuf_free(전문);
    memset(èjìrìwayàrụ_valuu.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&njìarụ_valuu);assert(들어온수==1&&èjìrìwayàrụ_valuu.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&njìarụ_valuu);
    assert(èjìrìwayàrụ_valuu.소비==0&&들어온수==1&&èjìrìwayàrụ_valuu.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&njìarụ_valuu);assert(!netif_is_link_up(&njìarụ_valuu));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
