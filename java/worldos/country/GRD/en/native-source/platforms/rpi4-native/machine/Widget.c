#include "../naming/machineLinkNames.h"
#include "screenInformation.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t boardPixel(uintptr_t,uintptr_t,uintptr_t),boardTerminal(uintptr_t);
extern void terminalGlyph(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int categoryValue,parent,xCoordinate,yCoordinate,requestedWidthValue,requestedHeightValue,isShown,manualLayout,layoutPolicy;unsigned text[128],lengthValue; } widgetState;
static widgetState nodes[4][32];
static int focused[4],eventList[4][16];static unsigned firstEntry[4],entryCount[4],unsignedResult[4],unsignedLongValue[4];
static void event(int ownerObject,int value){if(entryCount[ownerObject]<16){eventList[ownerObject][(firstEntry[ownerObject]+entryCount[ownerObject])%16]=value;entryCount[ownerObject]++;}}
static widgetState *elementValue(int ownerObject,int identifierValue){return ownerObject>=0&&ownerObject<4&&identifierValue>0&&identifierValue<=32&&nodes[ownerObject][identifierValue-1].categoryValue?&nodes[ownerObject][identifierValue-1]:0;}
static void rectangularRegion(int xCoordinate,int yCoordinate,int requestedWidthValue,int requestedHeightValue,unsigned pixelColour){boardRectangleFill(xCoordinate,yCoordinate,requestedWidthValue,requestedHeightValue,pixelColour);}
int screenVisible(int ownerObject){if(ownerObject<0||ownerObject>=4)return 0;for(int ordinalIndex=0;ordinalIndex<32;ordinalIndex++)if(nodes[ownerObject][ordinalIndex].categoryValue==1&&nodes[ownerObject][ordinalIndex].isShown)return 1;return 0;}
void initializeScreen(int ownerObject){memset(nodes[ownerObject],0,sizeof(nodes[ownerObject]));entryCount[ownerObject]=firstEntry[ownerObject]=focused[ownerObject]=unsignedLongValue[ownerObject]=0;}
static void position(int ownerObject,widgetState *requestedWidthValue,int *xCoordinate,int *yCoordinate){*xCoordinate=requestedWidthValue->xCoordinate;*yCoordinate=requestedWidthValue->yCoordinate;int dataPosition=requestedWidthValue->parent;for(int itemCount=0;dataPosition&&itemCount<32;itemCount++){widgetState *upperSide=elementValue(ownerObject,dataPosition);if(!upperSide)break;*xCoordinate+=upperSide->xCoordinate;*yCoordinate+=upperSide->yCoordinate+(upperSide->categoryValue==1?30:0);dataPosition=upperSide->parent;}}
static int isDisplayed(int ownerObject,widgetState *requestedWidthValue){for(int itemCount=0;itemCount<32;itemCount++){if(!requestedWidthValue->isShown)return 0;if(requestedWidthValue->categoryValue==1)return 1;requestedWidthValue=elementValue(ownerObject,requestedWidthValue->parent);if(!requestedWidthValue)return 0;}return 0;}
static void text(int xCoordinate,int yCoordinate,widgetState *requestedWidthValue,int maximumData,unsigned pixelColour,unsigned backgroundColour){int currentPosition=0;for(unsigned ordinalIndex=0;ordinalIndex<requestedWidthValue->lengthValue;ordinalIndex++){unsigned characterEncoding=requestedWidthValue->text[ordinalIndex],widthValue=characterEncoding>=256?16:8;if(currentPosition+(int)widthValue>maximumData)break;terminalGlyph(xCoordinate+currentPosition,yCoordinate,characterEncoding,pixelColour,backgroundColour);currentPosition+=widthValue;}}
void redrawScreen(int ownerObject){
    if(!screenVisible(ownerObject))return;
    for(int processingOrder=1;processingOrder<=5;processingOrder++)for(int ordinalIndex=0;ordinalIndex<32;ordinalIndex++){
        widgetState *requestedWidthValue=&nodes[ownerObject][ordinalIndex];if(requestedWidthValue->categoryValue!=processingOrder||!isDisplayed(ownerObject,requestedWidthValue))continue;int xCoordinate,yCoordinate;position(ownerObject,requestedWidthValue,&xCoordinate,&yCoordinate);
        if(processingOrder==1){rectangularRegion(xCoordinate,yCoordinate,requestedWidthValue->requestedWidthValue,requestedWidthValue->requestedHeightValue,0xeee9e0);rectangularRegion(xCoordinate,yCoordinate,requestedWidthValue->requestedWidthValue,30,0x905020);text(xCoordinate+10,yCoordinate+7,requestedWidthValue,requestedWidthValue->requestedWidthValue-50,0xffffff,0x905020);rectangularRegion(xCoordinate+requestedWidthValue->requestedWidthValue-28,yCoordinate+4,24,22,0x5555b8);terminalGlyph(xCoordinate+requestedWidthValue->requestedWidthValue-20,yCoordinate+7,'X',0xffffff,0x5555b8);}
        if(processingOrder==2)rectangularRegion(xCoordinate,yCoordinate,requestedWidthValue->requestedWidthValue,requestedWidthValue->requestedHeightValue,0xeee9e0);
        if(processingOrder>=3){unsigned backgroundColour=processingOrder==4?0xc0ab86:processingOrder==5?0xffffff:0xeee9e0;if(processingOrder!=3)rectangularRegion(xCoordinate,yCoordinate,requestedWidthValue->requestedWidthValue,requestedWidthValue->requestedHeightValue,backgroundColour);text(xCoordinate+4,yCoordinate+4,requestedWidthValue,requestedWidthValue->requestedWidthValue-8,0x201a15,backgroundColour);if(processingOrder==5&&focused[ownerObject]==ordinalIndex+1)rectangularRegion(xCoordinate,yCoordinate+requestedWidthValue->requestedHeightValue-2,requestedWidthValue->requestedWidthValue,2,0x905020);}
    }
}
int screenOverlay(int ownerObject,int xCoordinate,int yCoordinate){
    if(!screenVisible(ownerObject))return 0;
    for(int ordinalIndex=0;ordinalIndex<32;ordinalIndex++){
        widgetState *window=&nodes[ownerObject][ordinalIndex];
        if(window->categoryValue==1&&window->isShown&&xCoordinate>=window->xCoordinate&&yCoordinate>=window->yCoordinate&&
           xCoordinate<window->xCoordinate+window->requestedWidthValue&&yCoordinate<window->yCoordinate+window->requestedHeightValue)return 1;
    }return 0;
}
int screenPointer(int ownerObject,unsigned isPressed,int xCoordinate,int yCoordinate){
    if(!screenVisible(ownerObject))return 0;
    if(isPressed&1)for(int ordinalIndex=31;ordinalIndex>=0;ordinalIndex--){widgetState *requestedWidthValue=&nodes[ownerObject][ordinalIndex];if(!requestedWidthValue->categoryValue||!isDisplayed(ownerObject,requestedWidthValue))continue;int windowX,windowY;position(ownerObject,requestedWidthValue,&windowX,&windowY);
        if(xCoordinate<windowX||yCoordinate<windowY||xCoordinate>=windowX+requestedWidthValue->requestedWidthValue||yCoordinate>=windowY+requestedWidthValue->requestedHeightValue)continue;
        if(requestedWidthValue->categoryValue==1&&yCoordinate<windowY+30&&xCoordinate>=windowX+requestedWidthValue->requestedWidthValue-28){if(requestedWidthValue->layoutPolicy!=0)requestedWidthValue->isShown=0;event(ownerObject,0x10000+ordinalIndex+1);boardTerminal(3);return 1;}
        if(requestedWidthValue->categoryValue==4){event(ownerObject,ordinalIndex+1);return 1;}if(requestedWidthValue->categoryValue==5){focused[ownerObject]=ordinalIndex+1;boardTerminal(3);return 1;}
        if(requestedWidthValue->categoryValue==1)return 1;
    }return 0;
}
void screenPress(int ownerObject,unsigned secondValue){
    widgetState *requestedWidthValue=elementValue(ownerObject,focused[ownerObject]);if(!requestedWidthValue||requestedWidthValue->categoryValue!=5)return;
    if(secondValue==13||secondValue==10){event(ownerObject,focused[ownerObject]);return;}
    if(secondValue==8||secondValue==127){if(requestedWidthValue->lengthValue)requestedWidthValue->lengthValue--;unsignedLongValue[ownerObject]=0;}
    else{
        unsigned characterEncoding=secondValue;
        if(unsignedLongValue[ownerObject]){if((secondValue&192)!=128){unsignedLongValue[ownerObject]=0;return;}unsignedResult[ownerObject]=(unsignedResult[ownerObject]<<6)|(secondValue&63);if(--unsignedLongValue[ownerObject])return;characterEncoding=unsignedResult[ownerObject];}
        else if(secondValue>=0xc2&&secondValue<=0xf4){unsignedLongValue[ownerObject]=secondValue<0xe0?1:secondValue<0xf0?2:3;unsignedResult[ownerObject]=secondValue&((1u<<(6-unsignedLongValue[ownerObject]))-1);return;}
        else if(secondValue<32||secondValue>=128)return;
        if(characterEncoding>0x10ffff||(characterEncoding>=0xd800&&characterEncoding<=0xdfff))return;if(requestedWidthValue->lengthValue<127)requestedWidthValue->text[requestedWidthValue->lengthValue++]=characterEncoding;
    }
    boardTerminal(3);
}
int invokeScreen(int ownerObject,unsigned action,int identifierValue,int firstValue,int secondValue,int characterCode,int destinationData){
    if(ownerObject<0||ownerObject>=4)return -22;widgetState *requestedWidthValue=elementValue(ownerObject,identifierValue);
    if(action==0){if(identifierValue<1||identifierValue>5)return -22;for(int ordinalIndex=0;ordinalIndex<32;ordinalIndex++)if(nodes[ownerObject][ordinalIndex].categoryValue==0){requestedWidthValue=&nodes[ownerObject][ordinalIndex];memset(requestedWidthValue,0,sizeof(*requestedWidthValue));requestedWidthValue->categoryValue=identifierValue;requestedWidthValue->isShown=identifierValue!=1;requestedWidthValue->requestedWidthValue=identifierValue==1?380:220;requestedWidthValue->requestedHeightValue=identifierValue==1?240:28;requestedWidthValue->layoutPolicy=1;requestedWidthValue->xCoordinate=identifierValue==1?130:16;requestedWidthValue->yCoordinate=identifierValue==1?110:16;return ordinalIndex+1;}return -28;}
    if(action==5){if(!entryCount[ownerObject])return 0;int returnedValue=eventList[ownerObject][firstEntry[ownerObject]];firstEntry[ownerObject]=(firstEntry[ownerObject]+1)%16;entryCount[ownerObject]--;return returnedValue;}
    if(action==6)return screenVisible(ownerObject);
    if(!requestedWidthValue)return -9;
    int wasShown=isDisplayed(ownerObject,requestedWidthValue);
    if(action==1){int backgroundWidth=boardScreenWidth(),backgroundHeight=boardScreenHeight();if(firstValue<0||secondValue<0||characterCode<1||destinationData<1||firstValue>backgroundWidth||secondValue>backgroundHeight||characterCode>backgroundWidth-firstValue||destinationData>backgroundHeight-secondValue)return -22;requestedWidthValue->xCoordinate=firstValue;requestedWidthValue->yCoordinate=secondValue;requestedWidthValue->requestedWidthValue=characterCode;requestedWidthValue->requestedHeightValue=destinationData;requestedWidthValue->manualLayout=1;}
    else if(action==2){widgetState *childElement=elementValue(ownerObject,firstValue);if(!childElement||childElement==requestedWidthValue||childElement->categoryValue==1)return -22;int dataPosition=identifierValue;for(int depthValue=0;dataPosition&&depthValue<32;depthValue++){if(dataPosition==firstValue)return -22;widgetState *upperSide=elementValue(ownerObject,dataPosition);dataPosition=upperSide?upperSide->parent:0;}childElement->parent=identifierValue;if(!childElement->manualLayout){int siblings=0;for(int ordinalIndex=0;ordinalIndex<32;ordinalIndex++)if(&nodes[ownerObject][ordinalIndex]!=childElement&&nodes[ownerObject][ordinalIndex].parent==identifierValue)siblings++;childElement->yCoordinate=16+siblings*36;}}
    else if(action==3)requestedWidthValue->isShown=firstValue!=0;
    else if(action==4)requestedWidthValue->isShown=0;
    else if(action==7)requestedWidthValue->layoutPolicy=firstValue;
    else if(action==8)return requestedWidthValue->lengthValue;
    else if(action==9)return firstValue>=0&&(unsigned)firstValue<requestedWidthValue->lengthValue?requestedWidthValue->text[firstValue]:-22;
    else return -22;
    if(wasShown||isDisplayed(ownerObject,requestedWidthValue))boardTerminal(3);return 0;
}
int screenText(int ownerObject,int identifierValue,const uint32_t *data,unsigned itemCount){widgetState *requestedWidthValue=elementValue(ownerObject,identifierValue);if(!requestedWidthValue)return -9;if(itemCount>127)return -22;for(unsigned ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++){unsigned characterEncoding=data[ordinalIndex];if(characterEncoding>0x10ffff||(characterEncoding>=0xd800&&characterEncoding<=0xdfff))return -22;}for(unsigned ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)requestedWidthValue->text[ordinalIndex]=data[ordinalIndex];requestedWidthValue->lengthValue=itemCount;if(isDisplayed(ownerObject,requestedWidthValue))boardTerminal(3);return 0;}
