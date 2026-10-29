/* actualData Screen 메모리와 기존 C invoke 규약만 연결한다. 합성 구현은 source/FramebufferComposer.java. */
#include "../naming/machineLinkNames.h"
#include "screenInformation.h"
static volatile uint32_t *pixelsList;
static unsigned screenRowWordCount, screenWidth, screenHeight;
extern void jdrawPrepare(int,int),jdrawEnd(void),jdrawRectangle(int,int,int,int,int),jdrawPointer(int,int,int);
extern int jdrawWidth(void),jdrawHeight(void),jdrawCountLow(void),jdrawCountHigh(void);
extern int jdrawClip(int,int,int,int),jdrawClipValue(int),jdrawBegin(int,int,int,int),jdrawPixel(int,int,int);
uintptr_t boardFramebufferRead(uintptr_t horizontalPosition,uintptr_t verticalPosition){
    return pixelsList&&horizontalPosition<screenWidth&&verticalPosition<screenHeight?pixelsList[verticalPosition*screenRowWordCount+horizontalPosition]:0;
}
void boardFramebufferWrite(uintptr_t horizontalPosition,uintptr_t verticalPosition,uintptr_t colourValue){
    if(pixelsList&&horizontalPosition<screenWidth&&verticalPosition<screenHeight)pixelsList[verticalPosition*screenRowWordCount+horizontalPosition]=(uint32_t)colourValue;
}
void boardPrepareDrawing(volatile uint32_t *data,unsigned widthSpan,unsigned lengthValue,unsigned lineSpacingValue){
    pixelsList=data;screenWidth=widthSpan;screenHeight=lengthValue;screenRowWordCount=lineSpacingValue/4;jdrawPrepare((int)widthSpan,(int)lengthValue);
}
uintptr_t boardScreenWidth(void){return (unsigned)jdrawWidth();}
uintptr_t boardScreenHeight(void){return (unsigned)jdrawHeight();}
uint64_t boardDrawingCount(void){return ((uint64_t)(uint32_t)jdrawCountHigh()<<32)|(uint32_t)jdrawCountLow();}
uint32_t boardReadScreen(unsigned horizontalPosition,unsigned verticalPosition){return (uint32_t)boardFramebufferRead(horizontalPosition,verticalPosition);}
int boardDrawingBounds(int *horizontalPosition,int *verticalPosition,int *widthSpan,int *lengthValue){
    if(!jdrawClip(*horizontalPosition,*verticalPosition,*widthSpan,*lengthValue))return 0;
    *horizontalPosition=jdrawClipValue(0);*verticalPosition=jdrawClipValue(1);*widthSpan=jdrawClipValue(2);*lengthValue=jdrawClipValue(3);return 1;
}
int boardStartDrawing(int horizontalPosition,int verticalPosition,int widthSpan,int lengthValue){return jdrawBegin(horizontalPosition,verticalPosition,widthSpan,lengthValue);}
void boardFinishDrawing(void){jdrawEnd();}
uintptr_t boardPixel(uintptr_t horizontalPosition,uintptr_t verticalPosition,uintptr_t colourValue){return (unsigned)jdrawPixel((int)horizontalPosition,(int)verticalPosition,(int)colourValue);}
void boardRectangleFill(int horizontalPosition,int verticalPosition,int widthSpan,int lengthValue,uint32_t colourValue){jdrawRectangle(horizontalPosition,verticalPosition,widthSpan,lengthValue,(int)colourValue);}
void boardPointer(int horizontalPosition,int verticalPosition,unsigned shapeValue){jdrawPointer(horizontalPosition,verticalPosition,(int)shapeValue);}
