/* 가짜 MMIO/MDIO 장치로 βρόχος_τιμή Υπερχείλιση_τιμή·διάρκεια_τιμή·링크 전환을 검사한다. 실물 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t δήλωση_τιμή[0x10000/4];
#define 유선저장기(διεύθυνση) δήλωση_τιμή[(διεύθυνση)/4]
#define JKOROS_GENET_TEST 1
#include "../δίκτυο_δέσμη/ενσύρματος_δίκτυο.c"
static uintptr_t χρονική_σήμανση_τιμή;
static int 물리작동=1,실물=1,들어온수;
static unsigned short 물리값[32];
uintptr_t 보드밀리초(void){
    uint32_t λέξη_μήνυμα=유선저장기(0xe14);
    if(물리작동&&(λέξη_μήνυμα&(1u<<29))){unsigned διεύθυνση=(λέξη_μήνυμα>>21)&31,Ευρετήριο=(λέξη_μήνυμα>>16)&31;
        if(διεύθυνση!=1)유선저장기(0xe14)=1<<28;
        else{if(((λέξη_μήνυμα>>26)&3)==1)물리값[Ευρετήριο]=λέξη_μήνυμα&65535;유선저장기(0xe14)=물리값[Ευρετήριο];}}
    return χρονική_σήμανση_τιμή++;
}
int 보드실물(void){return 실물;}
int Πίνακας_απόλυτη_διεύθυνση(unsigned char *διεύθυνση){const unsigned char τιμή[]={2,1,2,3,4,5};memcpy(διεύθυνση,τιμή,6);return 1;}
void netif_set_link_up(struct netif *συσκευή_τιμή){συσκευή_τιμή->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *συσκευή_τιμή){συσκευή_τιμή->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *συσκευή_τιμή,struct pbuf *αυτοδύναμο_πακέτο,const ip4_addr_t *διεύθυνση){(void)συσκευή_τιμή;(void)αυτοδύναμο_πακέτο;(void)διεύθυνση;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer επίπεδο_Ευρετήριο,u16_t 수,pbuf_type 종류){
    (void)επίπεδο_Ευρετήριο;(void)종류;struct pbuf *δεδομένα=calloc(1,sizeof(*δεδομένα)+수);assert(δεδομένα);δεδομένα->payload=δεδομένα+1;δεδομένα->len=δεδομένα->tot_len=수;return δεδομένα;
}
u8_t pbuf_free(struct pbuf *δεδομένα){free(δεδομένα);return 1;}
err_t pbuf_take(struct pbuf *δεδομένα,const void *원본,u16_t 수){assert(수<=δεδομένα->len);memcpy(δεδομένα->payload,원본,수);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *δεδομένα,void *προορισμός_τιμή,u16_t 수,u16_t Εκτέλεση_2){assert(Εκτέλεση_2+수<=δεδομένα->len);memcpy(προορισμός_τιμή,(char*)δεδομένα->payload+Εκτέλεση_2,수);return 수;}
static err_t αποδέχομαι_σύνδεση(struct pbuf *δεδομένα,struct netif *συσκευή_τιμή){(void)συσκευή_τιμή;assert(δεδομένα->len==60);assert(((unsigned char*)δεδομένα->payload)[0]==0x42);들어온수++;pbuf_free(δεδομένα);return ERR_OK;}
int main(void){
    struct netif συσκευή_τιμή;memset(&συσκευή_τιμή,0,sizeof(συσκευή_τιμή));συσκευή_τιμή.input=αποδέχομαι_σύνδεση;
    유선저장기(0)=6u<<24;물리값[2]=0x600d;물리값[1]=4;물리값[25]=7<<8;
    실물=0;assert(!유선장치있음());실물=1;assert(유선장치있음());
    
    assert(Προετοίμασε_ενσύρματος_δίκτυο(&συσκευή_τιμή)==ERR_OK);assert(ενσύρματος_τιμή.물리주소==1);
    assert(유선저장기(GENET_RX_DMA_CTRL)==0x20001&&유선저장기(GENET_TX_DMA_CTRL)==0x20001);
    assert(유선저장기(0x80c)==0x02010203&&유선저장기(0x810)==0x0405);
    유선망살피기(&συσκευή_τιμή);assert(netif_is_link_up(&συσκευή_τιμή));assert(ενσύρματος_τιμή.속도==1000);
    ενσύρματος_τιμή.생산=ενσύρματος_τιμή.ανάλωση_τιμή=65534;유선저장기(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *αυτοδύναμο_πακέτο=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(αυτοδύναμο_πακέτο->payload,0x42,40);
    for(unsigned 순번=0;순번<3;순번++){assert(στέλνω_αυτοδύναμο_πακέτο(&συσκευή_τιμή,αυτοδύναμο_πακέτο)==ERR_OK);유선저장기(GENET_TX_DMA_CONS_INDEX(16))=ενσύρματος_τιμή.생산;}
    assert(ενσύρματος_τιμή.생산==1);assert((유선저장기(0x4000)>>16)==60);assert(ενσύρματος_τιμή.στέλνω[0][0]==0x42&&ενσύρματος_τιμή.στέλνω[0][59]==0);pbuf_free(αυτοδύναμο_πακέτο);
    유선저장기(GENET_TX_DMA_CONS_INDEX(16))=(ενσύρματος_τιμή.생산-255)&65535;αυτοδύναμο_πακέτο=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(στέλνω_αυτοδύναμο_πακέτο(&συσκευή_τιμή,αυτοδύναμο_πακέτο)==ERR_MEM);pbuf_free(αυτοδύναμο_πακέτο);
    memset(ενσύρματος_τιμή.λαμβάνω[254],0x42,64);유선저장기(0x2000+254*12)=(62<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=65535;
    유선망살피기(&συσκευή_τιμή);assert(들어온수==1&&ενσύρματος_τιμή.ανάλωση_τιμή==65535);
    유선저장기(0x2000+255*12)=(4095u<<16)|0x6000;유선저장기(GENET_RX_DMA_PROD_INDEX(16))=0;유선망살피기(&συσκευή_τιμή);
    assert(ενσύρματος_τιμή.ανάλωση_τιμή==0&&들어온수==1&&ενσύρματος_τιμή.Στατιστικά_τιμή[4]==1);
    물리값[1]=0;χρονική_σήμανση_τιμή+=1000;유선망살피기(&συσκευή_τιμή);assert(!netif_is_link_up(&συσκευή_τιμή));
    물리작동=0;assert(물리전송(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
