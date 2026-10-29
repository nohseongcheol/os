/* 가짜 MMIO/MDIO 장치로 లూప్_మూల్యం అతివ్యాప్తి_మూల్యం·పొడవు_మూల్యం·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t నమోదు_చేయి_మూల్యం[0x10000/4];
#define 유선저장기(ఇమెయిల్) నమోదు_చేయి_మూల్యం[(ఇమెయిల్)/4]
#define JKOROS_GENET_TEST 1
#include "../నెట్_వర్క్_దొంతర/తంత్రీసంధాన_నెట్_వర్క్.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t పదం_పాఠం=유선저장기(0xe14);
    if(물리작동&&(పదం_పాఠం&(1u<<29))){unsigned ఇమెయిల్=(పదం_పాఠం>>21)&31,సూచీ=(పదం_పాఠం>>16)&31;
        if(ఇమెయిల్!=1)유선저장기(0xe14)=1<<28;
        else{if(((పదం_పాఠం>>26)&3)==1)물리값[సూచీ]=పదం_పాఠం&65535;유선저장기(0xe14)=물리값[సూచీ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int బోర్డు_యంత్రం_ఇమెయిల్(unsigned char *ఇమెయిల్){const unsigned char మూల్యం[]={2,1,2,3,4,5};memcpy(ఇమెయిల్,మూల్యం,6);return 1;}
void netif_set_link_up(struct netif *పరికరం_మూల్యం){పరికరం_మూల్యం->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *పరికరం_మూల్యం){పరికరం_మూల్యం->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *పరికరం_మూల్యం,struct pbuf *전문,const ip4_addr_t *ఇమెయిల్){(void)పరికరం_మూల్యం;(void)전문;(void)ఇమెయిల్;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer పొర_సూచీ,u16_t 수,pbuf_type 종류){
    (void)పొర_సూచీ;(void)종류;struct pbuf *డేటా=calloc(1,sizeof(*డేటా)+수);assert(డేటా);డేటా->payload=డేటా+1;డేటా->len=డేటా->tot_len=수;return డేటా;
}
u8_t pbuf_free(struct pbuf *డేటా){free(డేటా);return 1;}
err_t pbuf_take(struct pbuf *డేటా,const void *원본,u16_t 수){assert(수<=డేటా->len);memcpy(డేటా->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *డేటా,void *గమ్యం_మూల్యం,u16_t 수,u16_t నడుపుము){assert(నడుపుము+수<=డేటా->len);memcpy(గమ్యం_మూల్యం,(char*)డేటా->payload+నడుపుము,수);return 수;}
static err_t ఆమోదించు_కనెక్షన్(struct pbuf *డేటా,struct netif *పరికరం_మూల్యం){(void)పరికరం_మూల్యం;assert(డేటా->len==60);assert(((unsigned char*)డేటా->payload)[0]==0x42);들어온수++;pbuf_free(డేటా);return ERR_OK;}
int main(void){
    struct netif పరికరం_మూల్యం;memset(&పరికరం_మూల్యం,0,sizeof(పరికరం_మూల్యం));పరికరం_మూల్యం.input=ఆమోదించు_కనెక్షన్;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(సిద్ధం_చేయు_తంత్రీసంధాన_నెట్_వర్క్(&పరికరం_మూల్యం)==ERR_OK);assert(తంత్రీసంధాన_మూల్యం.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&పరికరం_మూల్యం);assert(netif_is_link_up(&పరికరం_మూల్యం));assert(తంత్రీసంధాన_మూల్యం.속도==1000);
    తంత్రీసంధాన_మూల్యం.생산=తంత్రీసంధాన_మూల్యం.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&పరికరం_మూల్యం,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=తంత్రీసంధాన_మూల్యం.생산;}
    assert(తంత్రీసంధాన_మూల్యం.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(తంత్రీసంధాన_మూల్యం.పంపు[0][0]==0x42&&తంత్రీసంధాన_మూల్యం.పంపు[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(తంత్రీసంధాన_మూల్యం.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&పరికరం_మూల్యం,전문)==ERR_MEM);pbuf_free(전문);
    memset(తంత్రీసంధాన_మూల్యం.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&పరికరం_మూల్యం);assert(들어온수==1&&తంత్రీసంధాన_మూల్యం.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&పరికరం_మూల్యం);
    assert(తంత్రీసంధాన_మూల్యం.소비==0&&들어온수==1&&తంత్రీసంధాన_మూల్యం.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&పరికరం_మూల్యం);assert(!netif_is_link_up(&పరికరం_మూల్యం));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
