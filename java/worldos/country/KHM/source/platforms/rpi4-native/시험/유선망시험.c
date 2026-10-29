/* 가짜 MMIO/MDIO 장치로 រង្វិលជុំ_តំលៃ ការហៀរ_តំលៃ·ប្រវែង_តំលៃ·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ចុះឈ្មោះ_តំលៃ[0x10000/4];
#define 유선저장기(អ៊ីម៉ែល) ចុះឈ្មោះ_តំលៃ[(អ៊ីម៉ែល)/4]
#define JKOROS_GENET_TEST 1
#include "../ណិតវឺក_គរ/ដែលប្រើខ្សែ_ណិតវឺក.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t ពាក្យ_អត្ថបទ=유선저장기(0xe14);
    if(물리작동&&(ពាក្យ_អត្ថបទ&(1u<<29))){unsigned អ៊ីម៉ែល=(ពាក្យ_អត្ថបទ>>21)&31,សន្ទស្សន៏=(ពាក្យ_អត្ថបទ>>16)&31;
        if(អ៊ីម៉ែល!=1)유선저장기(0xe14)=1<<28;
        else{if(((ពាក្យ_អត្ថបទ>>26)&3)==1)물리값[សន្ទស្សន៏]=ពាក្យ_អត្ថបទ&65535;유선저장기(0xe14)=물리값[សន្ទស្សន៏];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ផ្ទាំង_ម៉ាស៊ីន_អ៊ីម៉ែល(unsigned char *អ៊ីម៉ែល){const unsigned char តំលៃ[]={2,1,2,3,4,5};memcpy(អ៊ីម៉ែល,តំលៃ,6);return 1;}
void netif_set_link_up(struct netif *ឧបករណ៍_តំលៃ){ឧបករណ៍_តំលៃ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ឧបករណ៍_តំលៃ){ឧបករណ៍_តំលៃ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ឧបករណ៍_តំលៃ,struct pbuf *전문,const ip4_addr_t *អ៊ីម៉ែល){(void)ឧបករណ៍_តំលៃ;(void)전문;(void)អ៊ីម៉ែល;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ស្រទាប់_សន្ទស្សន៏,u16_t 수,pbuf_type 종류){
    (void)ស្រទាប់_សន្ទស្សន៏;(void)종류;struct pbuf *ទិន្នន័យ=calloc(1,sizeof(*ទិន្នន័យ)+수);assert(ទិន្នន័យ);ទិន្នន័យ->payload=ទិន្នន័យ+1;ទិន្នន័យ->len=ទិន្នន័យ->tot_len=수;return ទិន្នន័យ;
}
u8_t pbuf_free(struct pbuf *ទិន្នន័យ){free(ទិន្នន័យ);return 1;}
err_t pbuf_take(struct pbuf *ទិន្នន័យ,const void *원본,u16_t 수){assert(수<=ទិន្នន័យ->len);memcpy(ទិន្នន័យ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ទិន្នន័យ,void *ទិសដៅ_តំលៃ,u16_t 수,u16_t រត់){assert(រត់+수<=ទិន្នន័យ->len);memcpy(ទិសដៅ_តំលៃ,(char*)ទិន្នន័យ->payload+រត់,수);return 수;}
static err_t ទទួល_យក_ការភ្ជាប់(struct pbuf *ទិន្នន័យ,struct netif *ឧបករណ៍_តំលៃ){(void)ឧបករណ៍_តំលៃ;assert(ទិន្នន័យ->len==60);assert(((unsigned char*)ទិន្នន័យ->payload)[0]==0x42);들어온수++;pbuf_free(ទិន្នន័យ);return ERR_OK;}
int main(void){
    struct netif ឧបករណ៍_តំលៃ;memset(&ឧបករណ៍_តំលៃ,0,sizeof(ឧបករណ៍_តំលៃ));ឧបករណ៍_តំលៃ.input=ទទួល_យក_ការភ្ជាប់;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(រៀបចំ_ដែលប្រើខ្សែ_ណិតវឺក(&ឧបករណ៍_តំលៃ)==ERR_OK);assert(ដែលប្រើខ្សែ_តំលៃ.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ឧបករណ៍_តំលៃ);assert(netif_is_link_up(&ឧបករណ៍_តំលៃ));assert(ដែលប្រើខ្សែ_តំលៃ.속도==1000);
    ដែលប្រើខ្សែ_តំលៃ.생산=ដែលប្រើខ្សែ_តំលៃ.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ឧបករណ៍_តំលៃ,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ដែលប្រើខ្សែ_តំលៃ.생산;}
    assert(ដែលប្រើខ្សែ_តំលៃ.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ដែលប្រើខ្សែ_តំលៃ.ផ្ញើ[0][0]==0x42&&ដែលប្រើខ្សែ_តំលៃ.ផ្ញើ[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ដែលប្រើខ្សែ_តំលៃ.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ឧបករណ៍_តំលៃ,전문)==ERR_MEM);pbuf_free(전문);
    memset(ដែលប្រើខ្សែ_តំលៃ.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ឧបករណ៍_តំលៃ);assert(들어온수==1&&ដែលប្រើខ្សែ_តំលៃ.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ឧបករណ៍_តំលៃ);
    assert(ដែលប្រើខ្សែ_តំលៃ.소비==0&&들어온수==1&&ដែលប្រើខ្សែ_តំលៃ.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ឧបករណ៍_តំលៃ);assert(!netif_is_link_up(&ឧបករណ៍_តំលៃ));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
