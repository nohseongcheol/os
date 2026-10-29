#include "../naming/machineLinkNames.h"
#include "invoke.h"
extern int main(int,char **);
static char argumentArray[8][256];
int userStart(int unused){
    (void)unused;char *argumentList[9];int argumentsCount=userInvoke(15,UINTPTR_MAX,0,0,0,0,0);
    if(argumentsCount<0||argumentsCount>8)return 126;
    for(int ordinalIndex=0;ordinalIndex<argumentsCount;ordinalIndex++){if(userInvoke(15,ordinalIndex,(uintptr_t)argumentArray[ordinalIndex],256,0,0,0)<0)return 126;argumentList[ordinalIndex]=argumentArray[ordinalIndex];}argumentList[argumentsCount]=0;
    return main(argumentsCount,argumentList);
}
void *memset(void*dataPosition,int characterCode,size_t itemCount){unsigned char*destinationData=dataPosition;while(itemCount--)*destinationData++=characterCode;return dataPosition;}
void *memcpy(void*destinationData,const void*stringData,size_t itemCount){unsigned char*firstValue=destinationData;const unsigned char*secondValue=stringData;while(itemCount--)*firstValue++=*secondValue++;return destinationData;}
/* 게스트 ELF는 16 KiB 이하: 두 이름이 같은 SVC 본문을 복제하지 않게 한다. */
__attribute__((noinline)) int pk_rectangle(unsigned xCoordinate,unsigned yCoordinate,unsigned widthValue,unsigned heightValue,unsigned pixelColour){return screenRectangle(xCoordinate,yCoordinate,widthValue,heightValue,pixelColour);}
__attribute__((noinline)) unsigned pk_ticks_ms(void){return userInvoke(7,0,0,0,0,0,0);}
__attribute__((noinline)) int pk_graphics_wait(void){return waitForScreenKey();}
int drawRectangle(unsigned horizontalPosition,unsigned verticalPosition,unsigned widthValue,unsigned heightValue,unsigned pixelColour){return pk_rectangle(horizontalPosition,verticalPosition,widthValue,heightValue,pixelColour);}
unsigned milliseconds(void){return pk_ticks_ms();}
int waitForDrawing(void){return pk_graphics_wait();}
int screenWidth(void){return readScreenWidth();}
int screenHeight(void){return readScreenHeight();}
