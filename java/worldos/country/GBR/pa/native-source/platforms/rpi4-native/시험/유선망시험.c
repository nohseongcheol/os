/* 가짜 MMIO/MDIO 장치로 ਲੂਪ_ਕੀਮਤ ਓਵਰਫ਼ਲੋ_ਕੀਮਤ·ਲੰਬਾਈ_ਕੀਮਤ·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ਰਜਿਸਟਰ_ਕਰੋ_ਕੀਮਤ[0x10000/4];
#define 유선저장기(ਪਤਾ) ਰਜਿਸਟਰ_ਕਰੋ_ਕੀਮਤ[(ਪਤਾ)/4]
#define JKOROS_GENET_TEST 1
#include "../ਨੈਟਵਰਕ_ਸਟੈਕ/ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਨੈਟਵਰਕ.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t ਸ਼ਬਦ_ਪਾਠ=유선저장기(0xe14);
    if(물리작동&&(ਸ਼ਬਦ_ਪਾਠ&(1u<<29))){unsigned ਪਤਾ=(ਸ਼ਬਦ_ਪਾਠ>>21)&31,ਅਨੁਕ੍ਰਮਣਿਕਾ=(ਸ਼ਬਦ_ਪਾਠ>>16)&31;
        if(ਪਤਾ!=1)유선저장기(0xe14)=1<<28;
        else{if(((ਸ਼ਬਦ_ਪਾਠ>>26)&3)==1)물리값[ਅਨੁਕ੍ਰਮਣਿਕਾ]=ਸ਼ਬਦ_ਪਾਠ&65535;유선저장기(0xe14)=물리값[ਅਨੁਕ੍ਰਮਣਿਕਾ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ਬੋਰਡ_ਮਸ਼ੀਨ_ਪਤਾ(unsigned char *ਪਤਾ){const unsigned char ਕੀਮਤ[]={2,1,2,3,4,5};memcpy(ਪਤਾ,ਕੀਮਤ,6);return 1;}
void netif_set_link_up(struct netif *ਤਜਵੀਜ_ਕੀਮਤ){ਤਜਵੀਜ_ਕੀਮਤ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ਤਜਵੀਜ_ਕੀਮਤ){ਤਜਵੀਜ_ਕੀਮਤ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ਤਜਵੀਜ_ਕੀਮਤ,struct pbuf *전문,const ip4_addr_t *ਪਤਾ){(void)ਤਜਵੀਜ_ਕੀਮਤ;(void)전문;(void)ਪਤਾ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ਲੇਅਰ_ਅਨੁਕ੍ਰਮਣਿਕਾ,u16_t 수,pbuf_type 종류){
    (void)ਲੇਅਰ_ਅਨੁਕ੍ਰਮਣਿਕਾ;(void)종류;struct pbuf *ਸਮੱਗਰੀ=calloc(1,sizeof(*ਸਮੱਗਰੀ)+수);assert(ਸਮੱਗਰੀ);ਸਮੱਗਰੀ->payload=ਸਮੱਗਰੀ+1;ਸਮੱਗਰੀ->len=ਸਮੱਗਰੀ->tot_len=수;return ਸਮੱਗਰੀ;
}
u8_t pbuf_free(struct pbuf *ਸਮੱਗਰੀ){free(ਸਮੱਗਰੀ);return 1;}
err_t pbuf_take(struct pbuf *ਸਮੱਗਰੀ,const void *원본,u16_t 수){assert(수<=ਸਮੱਗਰੀ->len);memcpy(ਸਮੱਗਰੀ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ਸਮੱਗਰੀ,void *ਮੰਜਿਲ_ਕੀਮਤ,u16_t 수,u16_t ਚਲਾਓ_2){assert(ਚਲਾਓ_2+수<=ਸਮੱਗਰੀ->len);memcpy(ਮੰਜਿਲ_ਕੀਮਤ,(char*)ਸਮੱਗਰੀ->payload+ਚਲਾਓ_2,수);return 수;}
static err_t ਸਵੀਕਾਰ_ਕਰੋ_ਸਬੰਧ(struct pbuf *ਸਮੱਗਰੀ,struct netif *ਤਜਵੀਜ_ਕੀਮਤ){(void)ਤਜਵੀਜ_ਕੀਮਤ;assert(ਸਮੱਗਰੀ->len==60);assert(((unsigned char*)ਸਮੱਗਰੀ->payload)[0]==0x42);들어온수++;pbuf_free(ਸਮੱਗਰੀ);return ERR_OK;}
int main(void){
    struct netif ਤਜਵੀਜ_ਕੀਮਤ;memset(&ਤਜਵੀਜ_ਕੀਮਤ,0,sizeof(ਤਜਵੀਜ_ਕੀਮਤ));ਤਜਵੀਜ_ਕੀਮਤ.input=ਸਵੀਕਾਰ_ਕਰੋ_ਸਬੰਧ;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(ਤਿਆਰ_ਕਰੋ_ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਨੈਟਵਰਕ(&ਤਜਵੀਜ_ਕੀਮਤ)==ERR_OK);assert(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ਤਜਵੀਜ_ਕੀਮਤ);assert(netif_is_link_up(&ਤਜਵੀਜ_ਕੀਮਤ));assert(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.속도==1000);
    ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산=ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ਤਜਵੀਜ_ਕੀਮਤ,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산;}
    assert(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਈਮੇਲ[0][0]==0x42&&ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਈਮੇਲ[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ਤਜਵੀਜ_ਕੀਮਤ,전문)==ERR_MEM);pbuf_free(전문);
    memset(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ਤਜਵੀਜ_ਕੀਮਤ);assert(들어온수==1&&ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ਤਜਵੀਜ_ਕੀਮਤ);
    assert(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비==0&&들어온수==1&&ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ਤਜਵੀਜ_ਕੀਮਤ);assert(!netif_is_link_up(&ਤਜਵੀਜ_ਕੀਮਤ));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
