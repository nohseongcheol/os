/* 가짜 MMIO/MDIO 장치로 લૂપ_મૂલ્ય ઓવરફ્લો_મૂલ્ય·લંબાઈ_મૂલ્ય·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t રજિસ્ટર_કરો_મૂલ્ય[0x10000/4];
#define 유선저장기(સરનામું) રજિસ્ટર_કરો_મૂલ્ય[(સરનામું)/4]
#define JKOROS_GENET_TEST 1
#include "../નેટવર્ક_સ્ટેક/વાયર્ડ_નેટવર્ક.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t શબ્દ_પાઠ=유선저장기(0xe14);
    if(물리작동&&(શબ્દ_પાઠ&(1u<<29))){unsigned સરનામું=(શબ્દ_પાઠ>>21)&31,અનુક્રમણિકા=(શબ્દ_પાઠ>>16)&31;
        if(સરનામું!=1)유선저장기(0xe14)=1<<28;
        else{if(((શબ્દ_પાઠ>>26)&3)==1)물리값[અનુક્રમણિકા]=શબ્દ_પાઠ&65535;유선저장기(0xe14)=물리값[અનુક્રમણિકા];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int બોર્ડ_મશીન_સરનામું(unsigned char *સરનામું){const unsigned char મૂલ્ય[]={2,1,2,3,4,5};memcpy(સરનામું,મૂલ્ય,6);return 1;}
void netif_set_link_up(struct netif *ડિવાઇસ_મૂલ્ય){ડિવાઇસ_મૂલ્ય->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ડિવાઇસ_મૂલ્ય){ડિવાઇસ_મૂલ્ય->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ડિવાઇસ_મૂલ્ય,struct pbuf *전문,const ip4_addr_t *સરનામું){(void)ડિવાઇસ_મૂલ્ય;(void)전문;(void)સરનામું;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer થર_અનુક્રમણિકા,u16_t 수,pbuf_type 종류){
    (void)થર_અનુક્રમણિકા;(void)종류;struct pbuf *ડેટા=calloc(1,sizeof(*ડેટા)+수);assert(ડેટા);ડેટા->payload=ડેટા+1;ડેટા->len=ડેટા->tot_len=수;return ડેટા;
}
u8_t pbuf_free(struct pbuf *ડેટા){free(ડેટા);return 1;}
err_t pbuf_take(struct pbuf *ડેટા,const void *원본,u16_t 수){assert(수<=ડેટા->len);memcpy(ડેટા->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ડેટા,void *ગંતવ્ય_મૂલ્ય,u16_t 수,u16_t ચલાવો_2){assert(ચલાવો_2+수<=ડેટા->len);memcpy(ગંતવ્ય_મૂલ્ય,(char*)ડેટા->payload+ચલાવો_2,수);return 수;}
static err_t સ્વીકારો_કનેક્શન(struct pbuf *ડેટા,struct netif *ડિવાઇસ_મૂલ્ય){(void)ડિવાઇસ_મૂલ્ય;assert(ડેટા->len==60);assert(((unsigned char*)ડેટા->payload)[0]==0x42);들어온수++;pbuf_free(ડેટા);return ERR_OK;}
int main(void){
    struct netif ડિવાઇસ_મૂલ્ય;memset(&ડિવાઇસ_મૂલ્ય,0,sizeof(ડિવાઇસ_મૂલ્ય));ડિવાઇસ_મૂલ્ય.input=સ્વીકારો_કનેક્શન;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(તૈયાર_કરો_વાયર્ડ_નેટવર્ક(&ડિવાઇસ_મૂલ્ય)==ERR_OK);assert(વાયર્ડ_મૂલ્ય.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ડિવાઇસ_મૂલ્ય);assert(netif_is_link_up(&ડિવાઇસ_મૂલ્ય));assert(વાયર્ડ_મૂલ્ય.속도==1000);
    વાયર્ડ_મૂલ્ય.생산=વાયર્ડ_મૂલ્ય.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ડિવાઇસ_મૂલ્ય,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=વાયર્ડ_મૂલ્ય.생산;}
    assert(વાયર્ડ_મૂલ્ય.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(વાયર્ડ_મૂલ્ય.મોકલો[0][0]==0x42&&વાયર્ડ_મૂલ્ય.મોકલો[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(વાયર્ડ_મૂલ્ય.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ડિવાઇસ_મૂલ્ય,전문)==ERR_MEM);pbuf_free(전문);
    memset(વાયર્ડ_મૂલ્ય.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ડિવાઇસ_મૂલ્ય);assert(들어온수==1&&વાયર્ડ_મૂલ્ય.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ડિવાઇસ_મૂલ્ય);
    assert(વાયર્ડ_મૂલ્ય.소비==0&&들어온수==1&&વાયર્ડ_મૂલ્ય.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ડિવાઇસ_મૂલ્ય);assert(!netif_is_link_up(&ડિવાઇસ_મૂલ્ય));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
