/* 가짜 MMIO/MDIO 장치로 วน_ค่า ยาวเกิน_ค่า·길이·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t ทะเบียน_ค่า[0x10000/4];
#define 유선저장기(อีเมล) ทะเบียน_ค่า[(อีเมล)/4]
#define JKOROS_GENET_TEST 1
#include "../เครือข่าย_สแตก/แบบผ่านสาย_เครือข่าย.c"
static uintptr_t ประทับเวลา_ค่า;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t คํา_ข้อความ=유선저장기(0xe14);
    if(물리작동&&(คํา_ข้อความ&(1u<<29))){unsigned อีเมล=(คํา_ข้อความ>>21)&31,ดัชนี=(คํา_ข้อความ>>16)&31;
        if(อีเมล!=1)유선저장기(0xe14)=1<<28;
        else{if(((คํา_ข้อความ>>26)&3)==1)물리값[ดัชนี]=คํา_ข้อความ&65535;유선저장기(0xe14)=물리값[ดัชนี];}}
    return ประทับเวลา_ค่า++;
}
int 보드실물(void){return 실물;}
int บอร์ด_เลขที่อยู่จริง(unsigned char *อีเมล){const unsigned char ค่า[]={2,1,2,3,4,5};memcpy(อีเมล,ค่า,6);return 1;}
void netif_set_link_up(struct netif *อุปกรณ์_ค่า){อุปกรณ์_ค่า->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *อุปกรณ์_ค่า){อุปกรณ์_ค่า->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *อุปกรณ์_ค่า,struct pbuf *เดตาแกรม,const ip4_addr_t *อีเมล){(void)อุปกรณ์_ค่า;(void)เดตาแกรม;(void)อีเมล;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer เลเยอร์_ดัชนี,u16_t หมายเลข,pbuf_type 종류){
    (void)เลเยอร์_ดัชนี;(void)종류;struct pbuf *ข้อมูล=calloc(1,sizeof(*ข้อมูล)+หมายเลข);assert(ข้อมูล);ข้อมูล->payload=ข้อมูล+1;ข้อมูล->len=ข้อมูล->tot_len=หมายเลข;return ข้อมูล;
}
u8_t pbuf_free(struct pbuf *ข้อมูล){free(ข้อมูล);return 1;}
err_t pbuf_take(struct pbuf *ข้อมูล,const void *원본,u16_t หมายเลข){assert(หมายเลข<=ข้อมูล->len);memcpy(ข้อมูล->payload,원본,หมายเลข);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *ข้อมูล,void *ปลายทาง_ค่า_a0fbc067,u16_t หมายเลข,u16_t เรียกใช้งาน){assert(เรียกใช้งาน+หมายเลข<=ข้อมูล->len);memcpy(ปลายทาง_ค่า_a0fbc067,(char*)ข้อมูล->payload+เรียกใช้งาน,หมายเลข);return หมายเลข;}
static err_t ยอมรับ_เพื่อน(struct pbuf *ข้อมูล,struct netif *อุปกรณ์_ค่า){(void)อุปกรณ์_ค่า;assert(ข้อมูล->len==60);assert(((unsigned char*)ข้อมูล->payload)[0]==0x42);들어온수++;pbuf_free(ข้อมูล);return ERR_OK;}
int main(void){
    struct netif อุปกรณ์_ค่า;memset(&อุปกรณ์_ค่า,0,sizeof(อุปกรณ์_ค่า));อุปกรณ์_ค่า.input=ยอมรับ_เพื่อน;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(จัดเตรียม_แบบผ่านสาย_เครือข่าย(&อุปกรณ์_ค่า)==ERR_OK);assert(แบบผ่านสาย_ค่า.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&อุปกรณ์_ค่า);assert(netif_is_link_up(&อุปกรณ์_ค่า));assert(แบบผ่านสาย_ค่า.속도==1000);
    แบบผ่านสาย_ค่า.생산=แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *เดตาแกรม=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(เดตาแกรม->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(ส่ง_เดตาแกรม(&อุปกรณ์_ค่า,เดตาแกรม)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=แบบผ่านสาย_ค่า.생산;}
    assert(แบบผ่านสาย_ค่า.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(แบบผ่านสาย_ค่า.ส่ง[0][0]==0x42&&แบบผ่านสาย_ค่า.ส่ง[0][59]==0);pbuf_free(เดตาแกรม);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(แบบผ่านสาย_ค่า.생산-255)&65535;เดตาแกรม=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(ส่ง_เดตาแกรม(&อุปกรณ์_ค่า,เดตาแกรม)==ERR_MEM);pbuf_free(เดตาแกรม);
    memset(แบบผ่านสาย_ค่า.รับ[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&อุปกรณ์_ค่า);assert(들어온수==1&&แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&อุปกรณ์_ค่า);
    assert(แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8==0&&들어온수==1&&แบบผ่านสาย_ค่า.집계[4]==1);
    물리값[1]=0;ประทับเวลา_ค่า+=1000;유선망살피기(&อุปกรณ์_ค่า);assert(!netif_is_link_up(&อุปกรณ์_ค่า));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
