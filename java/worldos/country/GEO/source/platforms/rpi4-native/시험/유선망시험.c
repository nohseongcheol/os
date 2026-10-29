/* 가짜 MMIO/MDIO 장치로 ციკლი_მნიშვნელობა_201e2521 გადავსება_მნიშვნელობა·სიგრძე_მნიშვნელობა·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t დარეგისტრირება_მნიშვნელობა[0x10000/4];
#define 유선저장기(მისამართი) დარეგისტრირება_მნიშვნელობა[(მისამართი)/4]
#define JKOROS_GENET_TEST 1
#include "../ქსელი_დასტა/სადენიანი_ქსელი.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t სიტყვები_ტექსტი=유선저장기(0xe14);
    if(물리작동&&(სიტყვები_ტექსტი&(1u<<29))){unsigned მისამართი=(სიტყვები_ტექსტი>>21)&31,ინდექსი=(სიტყვები_ტექსტი>>16)&31;
        if(მისამართი!=1)유선저장기(0xe14)=1<<28;
        else{if(((სიტყვები_ტექსტი>>26)&3)==1)물리값[ინდექსი]=სიტყვები_ტექსტი&65535;유선저장기(0xe14)=물리값[ინდექსი];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int დაფა_კომპიუტერი_მისამართი(unsigned char *მისამართი){const unsigned char მნიშვნელობა[]={2,1,2,3,4,5};memcpy(მისამართი,მნიშვნელობა,6);return 1;}
void netif_set_link_up(struct netif *მობილური_მნიშვნელობა){მობილური_მნიშვნელობა->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *მობილური_მნიშვნელობა){მობილური_მნიშვნელობა->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *მობილური_მნიშვნელობა,struct pbuf *전문,const ip4_addr_t *მისამართი){(void)მობილური_მნიშვნელობა;(void)전문;(void)მისამართი;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer შრე_ინდექსი,u16_t 수,pbuf_type 종류){
    (void)შრე_ინდექსი;(void)종류;struct pbuf *მონაცემები=calloc(1,sizeof(*მონაცემები)+수);assert(მონაცემები);მონაცემები->payload=მონაცემები+1;მონაცემები->len=მონაცემები->tot_len=수;return მონაცემები;
}
u8_t pbuf_free(struct pbuf *მონაცემები){free(მონაცემები);return 1;}
err_t pbuf_take(struct pbuf *მონაცემები,const void *원본,u16_t 수){assert(수<=მონაცემები->len);memcpy(მონაცემები->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *მონაცემები,void *მიმართულება_მნიშვნელობა,u16_t 수,u16_t გაშვება){assert(გაშვება+수<=მონაცემები->len);memcpy(მიმართულება_მნიშვნელობა,(char*)მონაცემები->payload+გაშვება,수);return 수;}
static err_t მიღება_კავშირი(struct pbuf *მონაცემები,struct netif *მობილური_მნიშვნელობა){(void)მობილური_მნიშვნელობა;assert(მონაცემები->len==60);assert(((unsigned char*)მონაცემები->payload)[0]==0x42);들어온수++;pbuf_free(მონაცემები);return ERR_OK;}
int main(void){
    struct netif მობილური_მნიშვნელობა;memset(&მობილური_მნიშვნელობა,0,sizeof(მობილური_მნიშვნელობა));მობილური_მნიშვნელობა.input=მიღება_კავშირი;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(მომზადება_სადენიანი_ქსელი(&მობილური_მნიშვნელობა)==ERR_OK);assert(სადენიანი_მნიშვნელობა.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&მობილური_მნიშვნელობა);assert(netif_is_link_up(&მობილური_მნიშვნელობა));assert(სადენიანი_მნიშვნელობა.속도==1000);
    სადენიანი_მნიშვნელობა.생산=სადენიანი_მნიშვნელობა.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&მობილური_მნიშვნელობა,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=სადენიანი_მნიშვნელობა.생산;}
    assert(სადენიანი_მნიშვნელობა.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(სადენიანი_მნიშვნელობა.გაგზავნა[0][0]==0x42&&სადენიანი_მნიშვნელობა.გაგზავნა[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(სადენიანი_მნიშვნელობა.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&მობილური_მნიშვნელობა,전문)==ERR_MEM);pbuf_free(전문);
    memset(სადენიანი_მნიშვნელობა.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&მობილური_მნიშვნელობა);assert(들어온수==1&&სადენიანი_მნიშვნელობა.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&მობილური_მნიშვნელობა);
    assert(სადენიანი_მნიშვნელობა.소비==0&&들어온수==1&&სადენიანი_მნიშვნელობა.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&მობილური_მნიშვნელობა);assert(!netif_is_link_up(&მობილური_მნიშვნელობა));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
