/* 가짜 MMIO/MDIO 장치로 lùb_VALUE taomadh_VALUE·faid_VALUE·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t clàraich_VALUE[0x10000/4];
#define 유선저장기(ADDRESS) clàraich_VALUE[(ADDRESS)/4]
#define JKOROS_GENET_TEST 1
#include "../lìonra_stac/유선망.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t Word_SMS=유선저장기(0xe14);
    if(물리작동&&(Word_SMS&(1u<<29))){unsigned ADDRESS=(Word_SMS>>21)&31,INDEX=(Word_SMS>>16)&31;
        if(ADDRESS!=1)유선저장기(0xe14)=1<<28;
        else{if(((Word_SMS>>26)&3)==1)물리값[INDEX]=Word_SMS&65535;유선저장기(0xe14)=물리값[INDEX];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int bòrd_inneal_ADDRESS(unsigned char *ADDRESS){const unsigned char VALUE[]={2,1,2,3,4,5};memcpy(ADDRESS,VALUE,6);return 1;}
void netif_set_link_up(struct netif *uidheam_VALUE){uidheam_VALUE->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *uidheam_VALUE){uidheam_VALUE->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *uidheam_VALUE,struct pbuf *전문,const ip4_addr_t *ADDRESS){(void)uidheam_VALUE;(void)전문;(void)ADDRESS;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer breath_INDEX,u16_t 수,pbuf_type 종류){
    (void)breath_INDEX;(void)종류;struct pbuf *dàta=calloc(1,sizeof(*dàta)+수);assert(dàta);dàta->payload=dàta+1;dàta->len=dàta->tot_len=수;return dàta;
}
u8_t pbuf_free(struct pbuf *dàta){free(dàta);return 1;}
err_t pbuf_take(struct pbuf *dàta,const void *원본,u16_t 수){assert(수<=dàta->len);memcpy(dàta->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *dàta,void *ceann_uidhe_VALUE,u16_t 수,u16_t ruith){assert(ruith+수<=dàta->len);memcpy(ceann_uidhe_VALUE,(char*)dàta->payload+ruith,수);return 수;}
static err_t gabh_ris_ceangal(struct pbuf *dàta,struct netif *uidheam_VALUE){(void)uidheam_VALUE;assert(dàta->len==60);assert(((unsigned char*)dàta->payload)[0]==0x42);들어온수++;pbuf_free(dàta);return ERR_OK;}
int main(void){
    struct netif uidheam_VALUE;memset(&uidheam_VALUE,0,sizeof(uidheam_VALUE));uidheam_VALUE.input=gabh_ris_ceangal;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(유선망준비(&uidheam_VALUE)==ERR_OK);assert(유선.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&uidheam_VALUE);assert(netif_is_link_up(&uidheam_VALUE));assert(유선.속도==1000);
    유선.생산=유선.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&uidheam_VALUE,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=유선.생산;}
    assert(유선.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(유선.cuir[0][0]==0x42&&유선.cuir[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(유선.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&uidheam_VALUE,전문)==ERR_MEM);pbuf_free(전문);
    memset(유선.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&uidheam_VALUE);assert(들어온수==1&&유선.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&uidheam_VALUE);
    assert(유선.소비==0&&들어온수==1&&유선.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&uidheam_VALUE);assert(!netif_is_link_up(&uidheam_VALUE));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
