/* 가짜 MMIO/MDIO 장치로 ຫ່ວງ_ຄ່າ ລົ້ນ_ຄ່າ·ຄວາມຍາວ_ຄ່າ·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ລົງທະບຽນ_ຄ່າ[0x10000/4];
#define 유선저장기(ອີເມວ) ລົງທະບຽນ_ຄ່າ[(ອີເມວ)/4]
#define JKOROS_GENET_TEST 1
#include "../ເຄືອຂ່າຍ_ກຸ່ມບັດ/ເປັນສາຍ_ເຄືອຂ່າຍ.c"
static uintptr_t 시각;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ=유선저장기(0xe14);
    if(물리작동&&(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ&(1u<<29))){unsigned ອີເມວ=(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ>>21)&31,ດັດຊະນີ=(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ>>16)&31;
        if(ອີເມວ!=1)유선저장기(0xe14)=1<<28;
        else{if(((ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ>>26)&3)==1)물리값[ດັດຊະນີ]=ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ&65535;유선저장기(0xe14)=물리값[ດັດຊະນີ];}}
    return 시각++;
}
int 보드실물(void){return 실물;}
int ກະດານ_ເຄື່ອງຈັກ_ອີເມວ(unsigned char *ອີເມວ){const unsigned char ຄ່າ[]={2,1,2,3,4,5};memcpy(ອີເມວ,ຄ່າ,6);return 1;}
void netif_set_link_up(struct netif *ມືຖື_ຄ່າ){ມືຖື_ຄ່າ->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *ມືຖື_ຄ່າ){ມືຖື_ຄ່າ->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *ມືຖື_ຄ່າ,struct pbuf *전문,const ip4_addr_t *ອີເມວ){(void)ມືຖື_ຄ່າ;(void)전문;(void)ອີເມວ;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer ຊັ້ນ_ດັດຊະນີ,u16_t 수,pbuf_type 종류){
    (void)ຊັ້ນ_ດັດຊະນີ;(void)종류;struct pbuf *ຂໍ້ມູນ=calloc(1,sizeof(*ຂໍ້ມູນ)+수);assert(ຂໍ້ມູນ);ຂໍ້ມູນ->payload=ຂໍ້ມູນ+1;ຂໍ້ມູນ->len=ຂໍ້ມູນ->tot_len=수;return ຂໍ້ມູນ;
}
u8_t pbuf_free(struct pbuf *ຂໍ້ມູນ){free(ຂໍ້ມູນ);return 1;}
err_t pbuf_take(struct pbuf *ຂໍ້ມູນ,const void *원본,u16_t 수){assert(수<=ຂໍ້ມູນ->len);memcpy(ຂໍ້ມູນ->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ຂໍ້ມູນ,void *ປາຍທາງ_ຄ່າ,u16_t 수,u16_t ແລ່ນ){assert(ແລ່ນ+수<=ຂໍ້ມູນ->len);memcpy(ປາຍທາງ_ຄ່າ,(char*)ຂໍ້ມູນ->payload+ແລ່ນ,수);return 수;}
static err_t ຕອບຮັບ_ການເຊື່ອມຕໍ່(struct pbuf *ຂໍ້ມູນ,struct netif *ມືຖື_ຄ່າ){(void)ມືຖື_ຄ່າ;assert(ຂໍ້ມູນ->len==60);assert(((unsigned char*)ຂໍ້ມູນ->payload)[0]==0x42);들어온수++;pbuf_free(ຂໍ້ມູນ);return ERR_OK;}
int main(void){
    struct netif ມືຖື_ຄ່າ;memset(&ມືຖື_ຄ່າ,0,sizeof(ມືຖື_ຄ່າ));ມືຖື_ຄ່າ.input=ຕອບຮັບ_ການເຊື່ອມຕໍ່;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(ກະ_ກຽມ_ເປັນສາຍ_ເຄືອຂ່າຍ(&ມືຖື_ຄ່າ)==ERR_OK);assert(ເປັນສາຍ_ຄ່າ.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&ມືຖື_ຄ່າ);assert(netif_is_link_up(&ມືຖື_ຄ່າ));assert(ເປັນສາຍ_ຄ່າ.속도==1000);
    ເປັນສາຍ_ຄ່າ.생산=ເປັນສາຍ_ຄ່າ.소비=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *전문=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(전문->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(전문보내기(&ມືຖື_ຄ່າ,전문)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ເປັນສາຍ_ຄ່າ.생산;}
    assert(ເປັນສາຍ_ຄ່າ.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ເປັນສາຍ_ຄ່າ.ສົ່ງ[0][0]==0x42&&ເປັນສາຍ_ຄ່າ.ສົ່ງ[0][59]==0);pbuf_free(전문);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ເປັນສາຍ_ຄ່າ.생산-255)&65535;전문=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(전문보내기(&ມືຖື_ຄ່າ,전문)==ERR_MEM);pbuf_free(전문);
    memset(ເປັນສາຍ_ຄ່າ.받기[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&ມືຖື_ຄ່າ);assert(들어온수==1&&ເປັນສາຍ_ຄ່າ.소비==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&ມືຖື_ຄ່າ);
    assert(ເປັນສາຍ_ຄ່າ.소비==0&&들어온수==1&&ເປັນສາຍ_ຄ່າ.집계[4]==1);
    물리값[1]=0;시각+=1000;유선망살피기(&ມືຖື_ຄ່າ);assert(!netif_is_link_up(&ມືຖື_ຄ່າ));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
