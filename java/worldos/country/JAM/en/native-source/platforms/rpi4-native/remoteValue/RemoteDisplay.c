/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 connect, 제한된 inputValue lengthValue, 비동기 sendValue, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 Screen data 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "remoteValue.h"
#include "cryptographySupport.h"
#include "profile.h"
#include "../networkStack/networkStack.h"
#include "../machine/screenInformation.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(screenPassword)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t boardMillis(void);
extern uintptr_t boardTerminal(uintptr_t);
void remoteKeyStroke(unsigned,int);
void initializeRemoteKeyStroke(void);
void commitRemoteKey(void);
static int listeningEndpoint=-1,peerValue=-1,stageValue,willClose;
static uintptr_t connectionTime,onReceiveAgain;
static unsigned char inputValue[8192],Output[4096],challengeValue[16];
static unsigned inputCount,outputCount,sentCount;
static unsigned widthValue,heightValue,pixelSize=4,bigEndianValue,redMaximum=255,greenMaximum=255,blueMaximum=255,redShift=16,greenShift=8,blueShift;
static uint32_t previousSummary[60*68];
static unsigned short changedTile[60*68];
static unsigned tileCount,tilePosition,requestedX,requestedY,requestedSpan,requestedHeight;
static unsigned read16(const unsigned char *dataPosition){return(unsigned)dataPosition[0]*256+dataPosition[1];}
static uint32_t read32(const unsigned char *dataPosition){return(uint32_t)dataPosition[0]<<24|(uint32_t)dataPosition[1]<<16|(uint32_t)dataPosition[2]<<8|dataPosition[3];}
static void write16(unsigned char *dataPosition,unsigned value){dataPosition[0]=value>>8;dataPosition[1]=value;}
static void write32(unsigned char *dataPosition,uint32_t value){dataPosition[0]=value>>24;dataPosition[1]=value>>16;dataPosition[2]=value>>8;dataPosition[3]=value;}
static void close(void){if(peerValue>=0)closeNetwork(peerValue);peerValue=-1;stageValue=0;inputCount=outputCount=sentCount=0;tileCount=tilePosition=0;willClose=0;initializeRemoteKeyStroke();onReceiveAgain=boardMillis()+500;}
static void emitValue(const void *data,unsigned number){memcpy(Output,data,number);outputCount=number;sentCount=0;}
static void consumeValue(unsigned number){inputCount-=number;memmove(inputValue,inputValue+number,inputCount);}
int controlRemoteDisplay(unsigned action){
    if(action==0){close();if(listeningEndpoint>=0)closeNetwork(listeningEndpoint);listeningEndpoint=-1;return 0;}
    if(action!=1)return listeningEndpoint>=0;
    if(listeningEndpoint>=0)return 0;
    int portValue=createSocketEndpoint(1);if(portValue<0)return portValue;reuseSocketAddress(portValue);
    int result=netBind(portValue,0,5900);if(!result)result=netListen(portValue);
    if(result<0){closeNetwork(portValue);return result;}listeningEndpoint=portValue;return 0;
}
static uint32_t tileSummary(unsigned horizontalPosition,unsigned verticalPosition){
    uint32_t value=2166136261u;
    for(unsigned yCoordinate=verticalPosition;yCoordinate<verticalPosition+16&&yCoordinate<heightValue;yCoordinate++)for(unsigned xCoordinate=horizontalPosition;xCoordinate<horizontalPosition+32&&xCoordinate<widthValue;xCoordinate++)value=(value^boardReadScreen(xCoordinate,yCoordinate))*16777619u;
    return value;
}
static void screenRequest(const unsigned char *dataPosition){
    requestedX=read16(dataPosition+2);requestedY=read16(dataPosition+4);requestedSpan=read16(dataPosition+6);requestedHeight=read16(dataPosition+8);
    if(requestedX>=widthValue||requestedY>=heightValue)requestedSpan=requestedHeight=0;
    if(requestedSpan>widthValue-requestedX&&requestedX<widthValue)requestedSpan=widthValue-requestedX;
    if(requestedHeight>heightValue-requestedY&&requestedY<heightValue)requestedHeight=heightValue-requestedY;
    tileCount=tilePosition=0;
    if(requestedSpan&&requestedHeight)for(unsigned yCoordinate=requestedY/16;yCoordinate<=(requestedY+requestedHeight-1)/16;yCoordinate++)for(unsigned xCoordinate=requestedX/32;xCoordinate<=(requestedX+requestedSpan-1)/32;xCoordinate++){
        unsigned positionIndex=yCoordinate*60+xCoordinate;uint32_t summaryValue=tileSummary(xCoordinate*32,yCoordinate*16);
        if(!dataPosition[1]||previousSummary[positionIndex]!=summaryValue)changedTile[tileCount++]=positionIndex;
    }
    Output[0]=Output[1]=0;write16(Output+2,tileCount);outputCount=4;sentCount=0;
}
static void sendTile(void){
    unsigned positionIndex=changedTile[tilePosition++],horizontalPosition=(positionIndex%60)*32,verticalPosition=(positionIndex/60)*16;
    unsigned endX=horizontalPosition+32,endY=verticalPosition+16;if(endX>widthValue)endX=widthValue;if(endY>heightValue)endY=heightValue;
    /* subpartValue 타일 request 뒤에도 remainderValue 화소를 보낸 것으로 처리하지 않는다. */
    int allValues=horizontalPosition>=requestedX&&verticalPosition>=requestedY&&endX<=requestedX+requestedSpan&&endY<=requestedY+requestedHeight;
    if(allValues)previousSummary[positionIndex]=tileSummary(horizontalPosition,verticalPosition);
    if(horizontalPosition<requestedX)horizontalPosition=requestedX;if(verticalPosition<requestedY)verticalPosition=requestedY;
    if(endX>requestedX+requestedSpan)endX=requestedX+requestedSpan;if(endY>requestedY+requestedHeight)endY=requestedY+requestedHeight;
    write16(Output,horizontalPosition);write16(Output+2,verticalPosition);write16(Output+4,endX-horizontalPosition);write16(Output+6,endY-verticalPosition);write32(Output+8,0);
    outputCount=12;sentCount=0;
    for(unsigned yCoordinate=verticalPosition;yCoordinate<endY;yCoordinate++)for(unsigned xCoordinate=horizontalPosition;xCoordinate<endX;xCoordinate++){
        uint32_t colourValue=boardReadScreen(xCoordinate,yCoordinate),value=(((colourValue>>16)&255)*redMaximum/255)<<redShift|
            (((colourValue>>8)&255)*greenMaximum/255)<<greenShift|((colourValue&255)*blueMaximum/255)<<blueShift;
        for(unsigned ordinalIndex=0;ordinalIndex<pixelSize;ordinalIndex++)Output[outputCount++]=value>>(8*(bigEndianValue?pixelSize-1-ordinalIndex:ordinalIndex));
    }
}
void inspectRemoteDisplay(void){
    if(listeningEndpoint<0)return;
    if(peerValue<0){if(boardMillis()<onReceiveAgain)return;peerValue=netAccept(listeningEndpoint);if(peerValue<0)return;
        connectionTime=boardMillis();stageValue=1;emitValue("RFB 003.008\n",12);memset(previousSummary,0,sizeof(previousSummary));
        pixelSize=4;bigEndianValue=0;redMaximum=greenMaximum=blueMaximum=255;redShift=16;greenShift=8;blueShift=0;}
    if(stageValue<5&&boardMillis()-connectionTime>15000){close();return;}
    if(outputCount){int number=netWrite(peerValue,Output+sentCount,outputCount-sentCount);if(number>0){sentCount+=number;if(sentCount==outputCount)outputCount=sentCount=0;}else if(number!=-11){close();return;}}
    if(!outputCount&&willClose){close();return;}
    if(!outputCount&&tilePosition<tileCount)sendTile();
    if(inputCount==sizeof(inputValue)){close();return;}
    int receivedCount=netRead(peerValue,inputValue+inputCount,sizeof(inputValue)-inputCount);
    if(receivedCount==0||(receivedCount<0&&receivedCount!=-11)){close();return;}if(receivedCount>0)inputCount+=receivedCount;
    if(outputCount||tilePosition<tileCount)return;
    if(stageValue==1&&inputCount>=12){if(memcmp(inputValue,"RFB 003.008\n",12)){close();return;}consumeValue(12);const unsigned char authenticationMethod[]={1,2};emitValue(authenticationMethod,2);stageValue=2;return;}
    if(stageValue==2&&inputCount){if(inputValue[0]!=2||remoteRandom(challengeValue,16)){close();return;}consumeValue(1);emitValue(challengeValue,16);stageValue=3;return;}
    if(stageValue==3&&inputCount>=16){unsigned char keyMaterial[8],correctAnswer[16];br_des_ct_cbcenc_keys passwordValue;
        for(unsigned ordinalIndex=0;ordinalIndex<8;ordinalIndex++){unsigned value=screenPassword[ordinalIndex],isInverted=0;for(unsigned innerOrdinal=0;innerOrdinal<8;innerOrdinal++){isInverted=(isInverted<<1)|(value&1);value>>=1;}keyMaterial[ordinalIndex]=isInverted;}
        br_des_ct_cbcenc_init(&passwordValue,keyMaterial,8);memcpy(correctAnswer,challengeValue,16);
        for(unsigned ordinalIndex=0;ordinalIndex<16;ordinalIndex+=8){unsigned char vectorValue[8]={0};br_des_ct_cbcenc_run(&passwordValue,vectorValue,correctAnswer+ordinalIndex,8);memset(vectorValue,0,8);}
        unsigned differenceValue=0;for(unsigned ordinalIndex=0;ordinalIndex<16;ordinalIndex++)differenceValue|=correctAnswer[ordinalIndex]^inputValue[ordinalIndex];consumeValue(16);memset(&passwordValue,0,sizeof(passwordValue));memset(keyMaterial,0,8);memset(correctAnswer,0,16);memset(challengeValue,0,16);
        write32(Output,differenceValue?1:0);outputCount=4;sentCount=0;
        if(differenceValue){write32(Output+4,19);memcpy(Output+8,"Authentication fail",19);outputCount=27;willClose=1;}else stageValue=4;return;}
    if(stageValue==4&&inputCount){consumeValue(1);widthValue=boardScreenWidth();heightValue=boardScreenHeight();if(!widthValue||!heightValue||widthValue>1920||heightValue>1080){close();return;}
        if(!boardTerminal(7)){const unsigned char event[]={30,2,1,0,0,0,0};feedRemoteInput(event,7);}
        memset(Output,0,40);write16(Output,widthValue);write16(Output+2,heightValue);Output[4]=32;Output[5]=24;Output[7]=1;
        write16(Output+8,255);write16(Output+10,255);write16(Output+12,255);Output[14]=16;Output[15]=8;
        const char *name="jkoros native";write32(Output+20,strlen(name));memcpy(Output+24,name,strlen(name));outputCount=24+strlen(name);sentCount=0;stageValue=5;return;}
    if(stageValue!=5||!inputCount)return;
    unsigned typeCategory=inputValue[0],neededValue=typeCategory==0?20:typeCategory==2?4:typeCategory==3?10:typeCategory==4?8:typeCategory==5?6:typeCategory==6?8:0;
    if(!neededValue){close();return;}if(inputCount<neededValue)return;
    if(typeCategory==2){unsigned number=read16(inputValue+2);if(number>128){close();return;}neededValue+=number*4;}
    if(typeCategory==6){unsigned number=read32(inputValue+4);if(number>4096){close();return;}neededValue+=number;}
    if(inputCount<neededValue)return;
    if(typeCategory==0){unsigned bitValue=inputValue[4],redChannelMaximum=read16(inputValue+8),secondsValue=read16(inputValue+10),blueChannelMaximum=read16(inputValue+12),redChannelShift=inputValue[14],greenChannelShift=inputValue[15],blueChannelShift=inputValue[16];
        if((bitValue!=16&&bitValue!=32)||!inputValue[7]||inputValue[6]>1||!redChannelMaximum||!secondsValue||!blueChannelMaximum||redChannelMaximum>255||secondsValue>255||blueChannelMaximum>255||redChannelShift>24||greenChannelShift>24||blueChannelShift>24||
           ((uint64_t)redChannelMaximum<<redChannelShift)>((1ull<<bitValue)-1)||((uint64_t)secondsValue<<greenChannelShift)>((1ull<<bitValue)-1)||((uint64_t)blueChannelMaximum<<blueChannelShift)>((1ull<<bitValue)-1)){close();return;}
        pixelSize=bitValue/8;bigEndianValue=inputValue[6];redMaximum=redChannelMaximum;greenMaximum=secondsValue;blueMaximum=blueChannelMaximum;redShift=redChannelShift;greenShift=greenChannelShift;blueShift=blueChannelShift;memset(previousSummary,0,sizeof(previousSummary));
    }else if(typeCategory==3)screenRequest(inputValue);
    else if(typeCategory==4)remoteKeyStroke(read32(inputValue+4),inputValue[1]!=0);
    else if(typeCategory==5){unsigned xCoordinate=read16(inputValue+2),yCoordinate=read16(inputValue+4);if(xCoordinate>=widthValue)xCoordinate=widthValue-1;if(yCoordinate>=heightValue)yCoordinate=heightValue-1;
        if(inputValue[1])commitRemoteKey();
        unsigned char event[]={30,1,inputValue[1],xCoordinate&255,xCoordinate>>8,yCoordinate&255,yCoordinate>>8};feedRemoteInput(event,sizeof(event));}
    consumeValue(neededValue);
}
