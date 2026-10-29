/* 가짜 MMIO/MDIO 장치로 loopValue overflowValue·lengthValue·링크 전환을 검사한다. physicalHardware 시험은 아니다. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
static uint32_t registerValue[0x10000/4];
#define wiredRegisters(address) registerValue[(address)/4]
#define JKOROS_GENET_TEST 1
#include "../networkStack/wiredNetwork.c"
static uintptr_t timestampValue;
static int physicalOperation=1,physicalHardware=1,incomingCount;
static unsigned short physicalValue[32];
uintptr_t boardMillis(void){
    uint32_t wordText=wiredRegisters(0xe14);
    if(physicalOperation&&(wordText&(1u<<29))){unsigned address=(wordText>>21)&31,index=(wordText>>16)&31;
        if(address!=1)wiredRegisters(0xe14)=1<<28;
        else{if(((wordText>>26)&3)==1)physicalValue[index]=wordText&65535;wiredRegisters(0xe14)=physicalValue[index];}}
    return timestampValue++;
}
int boardPhysicalHardware(void){return physicalHardware;}
int boardMachineAddress(unsigned char *address){const unsigned char value[]={2,1,2,3,4,5};memcpy(address,value,6);return 1;}
void netif_set_link_up(struct netif *deviceValue){deviceValue->flags|=NETIF_FLAG_LINK_UP;}
void netif_set_link_down(struct netif *deviceValue){deviceValue->flags&=~NETIF_FLAG_LINK_UP;}
err_t etharp_output(struct netif *deviceValue,struct pbuf *datagram,const ip4_addr_t *address){(void)deviceValue;(void)datagram;(void)address;return ERR_OK;}
struct pbuf *pbuf_alloc(pbuf_layer layerIndex,u16_t number,pbuf_type kindValue){
    (void)layerIndex;(void)kindValue;struct pbuf *data=calloc(1,sizeof(*data)+number);assert(data);data->payload=data+1;data->len=data->tot_len=number;return data;
}
u8_t pbuf_free(struct pbuf *data){free(data);return 1;}
err_t pbuf_take(struct pbuf *data,const void *original,u16_t number){assert(number<=data->len);memcpy(data->payload,original,number);return ERR_OK;}
u16_t pbuf_copy_partial(const struct pbuf *data,void *destinationValue,u16_t number,u16_t run){assert(run+number<=data->len);memcpy(destinationValue,(char*)data->payload+run,number);return number;}
static err_t acceptConnection(struct pbuf *data,struct netif *deviceValue){(void)deviceValue;assert(data->len==60);assert(((unsigned char*)data->payload)[0]==0x42);incomingCount++;pbuf_free(data);return ERR_OK;}
int main(void){
    struct netif deviceValue;memset(&deviceValue,0,sizeof(deviceValue));deviceValue.input=acceptConnection;
    wiredRegisters(0)=6u<<24;physicalValue[2]=0x600d;physicalValue[1]=4;physicalValue[25]=7<<8;
    physicalHardware=0;assert(!hasWiredDevice());physicalHardware=1;assert(hasWiredDevice());
    
    assert(prepareWiredNetwork(&deviceValue)==ERR_OK);assert(wiredValue.physicalAddress==1);
    assert(wiredRegisters(GENET_RX_DMA_CTRL)==0x20001&&wiredRegisters(GENET_TX_DMA_CTRL)==0x20001);
    assert(wiredRegisters(0x80c)==0x02010203&&wiredRegisters(0x810)==0x0405);
    inspectWiredNetwork(&deviceValue);assert(netif_is_link_up(&deviceValue));assert(wiredValue.speedValue==1000);
    wiredValue.produceValue=wiredValue.consumeValue=65534;wiredRegisters(GENET_TX_DMA_CONS_INDEX(16))=65534;
    struct pbuf *datagram=pbuf_alloc(PBUF_RAW,40,PBUF_RAM);memset(datagram->payload,0x42,40);
    for(unsigned ordinalIndex=0;ordinalIndex<3;ordinalIndex++){assert(sendDatagram(&deviceValue,datagram)==ERR_OK);wiredRegisters(GENET_TX_DMA_CONS_INDEX(16))=wiredValue.produceValue;}
    assert(wiredValue.produceValue==1);assert((wiredRegisters(0x4000)>>16)==60);assert(wiredValue.send[0][0]==0x42&&wiredValue.send[0][59]==0);pbuf_free(datagram);
    wiredRegisters(GENET_TX_DMA_CONS_INDEX(16))=(wiredValue.produceValue-255)&65535;datagram=pbuf_alloc(PBUF_RAW,60,PBUF_RAM);assert(sendDatagram(&deviceValue,datagram)==ERR_MEM);pbuf_free(datagram);
    memset(wiredValue.receive[254],0x42,64);wiredRegisters(0x2000+254*12)=(62<<16)|0x6000;wiredRegisters(GENET_RX_DMA_PROD_INDEX(16))=65535;
    inspectWiredNetwork(&deviceValue);assert(incomingCount==1&&wiredValue.consumeValue==65535);
    wiredRegisters(0x2000+255*12)=(4095u<<16)|0x6000;wiredRegisters(GENET_RX_DMA_PROD_INDEX(16))=0;inspectWiredNetwork(&deviceValue);
    assert(wiredValue.consumeValue==0&&incomingCount==1&&wiredValue.statisticsValue[4]==1);
    physicalValue[1]=0;timestampValue+=1000;inspectWiredNetwork(&deviceValue);assert(!netif_is_link_up(&deviceValue));
    physicalOperation=0;assert(physicalTransfer(1,2,0,0)==-1);
    puts("GENET mock PASS: initialization, DMA wrap, full TX, RX bounds, link, MDIO timeout");return 0;
}
