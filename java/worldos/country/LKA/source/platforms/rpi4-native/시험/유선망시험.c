/* 가짜 MMIO/MDIO 장치로 ලූපය_අගය පිටාරය_අගය·දිග_අගය·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ලියාපදිංචිය_අගය[0x10000/4];
#define 유선저장기(යොමුව) ලියාපදිංචිය_අගය[(යොමුව)/4]
#define JKOROS_GENET_TEST 1
#include "../ජාලය_කැටිය/පරිපථගත_ජාලය.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t 말=유선저장기(0xe14);
    if(물리작동&&(말&(1u<<29))){unsigned යොමුව=(말>>21)&31,සූචිය=(말>>16)&31;
        if(යොමුව!=1)유선저장기(0xe14)=1<<28;
        else{if(((말>>26)&3)==1)물리값[සූචිය]=말&65535;유선저장기(0xe14)=물리값[සූචිය];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int 보드기계주소(unsigned char *යොමුව){const unsigned char අගය[]={2,1,2,3,4,5};memcpy(යොමුව,අගය,6);return 1;}
void netif_set_link_up(struct netif *ජංගම_අගය){ජංගම_අගය->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ජංගම_අගය){ජංගම_අගය->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ජංගම_අගය,struct pbuf *전문,const ip4_addr_t *යොමුව){(void)ජංගම_අගය;(void)전문;(void)යොමුව;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ස්තරය_සූචිය,u16_t 수,pbuf_type 종류){
    (void)ස්තරය_සූචිය;(void)종류;struct pbuf *දත්ත=calloc(1,sizeof(*දත්ත)+수);assert(දත්ත);දත්ත->payload=දත්ත+1;දත්ත->len=දත්ත->tot_len=수;return දත්ත;
}
u8_t pbuf_free(struct pbuf *දත්ත){free(දත්ත);return 1;}
err_t pbuf_take(struct pbuf *දත්ත,const void *원본,u16_t 수){assert(수<=දත්ත->len);memcpy(දත්ත->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *දත්ත,void *ගමනාන්තය_අගය,u16_t 수,u16_t ක්_රියාත්මක_කරන්න_2){assert(ක්_රියාත්මක_කරන්න_2+수<=දත්ත->len);memcpy(ගමනාන්තය_අගය,(char*)දත්ත->payload+ක්_රියාත්මක_කරන්න_2,수);return 수;}
static err_t පිළිගන්න_සබැඳුම(struct pbuf *දත්ත,struct netif *ජංගම_අගය){(void)ජංගම_අගය;assert(දත්ත->len==60);assert(((unsigned char*)දත්ත->payload)[0]==0x42);들어온수++;pbuf_free(දත්ත);return ERR_OK;}
int main(void){
    struct netif ජංගම_අගය;memset(&ජංගම_අගය,0,sizeof(ජංගම_අගය));ජංගම_අගය.input=පිළිගන්න_සබැඳුම;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(පිළියෙල_කරන්න_පරිපථගත_ජාලය(&ජංගම_අගය)==ERR_OK);assert(පරිපථගත_අගය.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ජංගම_අගය);assert(netif_is_link_up(&ජංගම_අගය));assert(පරිපථගත_අගය.속도==1000);
    පරිපථගත_අගය.생산=පරිපථගත_අගය.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ජංගම_අගය,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=පරිපථගත_අගය.생산;}
    assert(පරිපථගත_අගය.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(පරිපථගත_අගය.ඊමේල්[0][0]==0x42&&පරිපථගත_අගය.ඊමේල්[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(පරිපථගත_අගය.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ජංගම_අගය,전문)==ERR_MEM);pbuf_free(전문);
    memset(පරිපථගත_අගය.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ජංගම_අගය);assert(들어온수==1&&පරිපථගත_අගය.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ජංගම_අගය);
    assert(පරිපථගත_අගය.소비==0&&들어온수==1&&පරිපථගත_අගය.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ජංගම_අගය);assert(!netif_is_link_up(&ජංගම_අගය));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
