/* 가짜 MMIO/MDIO 장치로 לולאה_ערך גלישה_ערך·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t אוגר_ערך[0x10000/4];
#define 유선저장기(למען) אוגר_ערך[(למען)/4]
#define JKOROS_GENET_TEST 1
#include "../רשת_רמז/קווי_רשת.c"
static uintptr_t חותמת_זמן_ערך;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t מילים_טקסט=유선저장기(0xe14);
    if(물리작동&&(מילים_טקסט&(1u<<29))){unsigned למען=(מילים_טקסט>>21)&31,מדד=(מילים_טקסט>>16)&31;
        if(למען!=1)유선저장기(0xe14)=1<<28;
        else{if(((מילים_טקסט>>26)&3)==1)물리값[מדד]=מילים_טקסט&65535;유선저장기(0xe14)=물리값[מדד];}}
    return חותמת_זמן_ערך++;
}
int 보드실물(void){return 실물;}
int לוח_כתובת_ממשית(unsigned char *למען){const unsigned char ערך[]={2,1,2,3,4,5};memcpy(למען,ערך,6);return 1;}
void netif_set_link_up(struct netif *התקן_ערך_e13f0cd9){התקן_ערך_e13f0cd9->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *התקן_ערך_e13f0cd9){התקן_ערך_e13f0cd9->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *התקן_ערך_e13f0cd9,struct pbuf *יחידת_נתונים,const ip4_addr_t *למען){(void)התקן_ערך_e13f0cd9;(void)יחידת_נתונים;(void)למען;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer שכבה_מדד,u16_t 수,pbuf_type 종류){
    (void)שכבה_מדד;(void)종류;struct pbuf *נתונים=calloc(1,sizeof(*נתונים)+수);assert(נתונים);נתונים->payload=נתונים+1;נתונים->len=נתונים->tot_len=수;return נתונים;
}
u8_t pbuf_free(struct pbuf *נתונים){free(נתונים);return 1;}
err_t pbuf_take(struct pbuf *נתונים,const void *원본,u16_t 수){assert(수<=נתונים->len);memcpy(נתונים->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *נתונים,void *יעד_ערך,u16_t 수,u16_t הפעלה){assert(הפעלה+수<=נתונים->len);memcpy(יעד_ערך,(char*)נתונים->payload+הפעלה,수);return 수;}
static err_t לקבל_קשר(struct pbuf *נתונים,struct netif *התקן_ערך_e13f0cd9){(void)התקן_ערך_e13f0cd9;assert(נתונים->len==60);assert(((unsigned char*)נתונים->payload)[0]==0x42);들어온수++;pbuf_free(נתונים);return ERR_OK;}
int main(void){
    struct netif התקן_ערך_e13f0cd9;memset(&התקן_ערך_e13f0cd9,0,sizeof(התקן_ערך_e13f0cd9));התקן_ערך_e13f0cd9.input=לקבל_קשר;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(להכין_קווי_רשת(&התקן_ערך_e13f0cd9)==ERR_OK);assert(קווי_ערך.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&התקן_ערך_e13f0cd9);assert(netif_is_link_up(&התקן_ערך_e13f0cd9));assert(קווי_ערך.속도==1000);
    קווי_ערך.생산=קווי_ערך.לצרוך_ערך=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *יחידת_נתונים=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(יחידת_נתונים->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(שלח_יחידת_נתונים(&התקן_ערך_e13f0cd9,יחידת_נתונים)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=קווי_ערך.생산;}
    assert(קווי_ערך.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(קווי_ערך.שלח[0][0]==0x42&&קווי_ערך.שלח[0][59]==0);pbuf_free(יחידת_נתונים);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(קווי_ערך.생산-255)&65535;יחידת_נתונים=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(שלח_יחידת_נתונים(&התקן_ערך_e13f0cd9,יחידת_נתונים)==ERR_MEM);pbuf_free(יחידת_נתונים);
    memset(קווי_ערך.לקבל[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&התקן_ערך_e13f0cd9);assert(들어온수==1&&קווי_ערך.לצרוך_ערך==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&התקן_ערך_e13f0cd9);
    assert(קווי_ערך.לצרוך_ערך==0&&들어온수==1&&קווי_ערך.집계[4]==1);
    물리값[1]=0;חותמת_זמן_ערך+=1000;유선망살피기(&התקן_ערך_e13f0cd9);assert(!netif_is_link_up(&התקן_ערך_e13f0cd9));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
