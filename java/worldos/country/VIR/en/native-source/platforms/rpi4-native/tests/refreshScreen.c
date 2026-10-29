#include "../naming/machineLinkNames.h"
#include "../machine/screenInformation.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void kernelPanic(const char *description){fputs(description,stderr);abort();}
extern uintptr_t boardTerminal(uintptr_t),boardPixel(uintptr_t,uintptr_t,uintptr_t);
extern void terminalPointer(unsigned,int,int),terminalByte(unsigned);
extern int invokeScreen(int,unsigned,int,int,int,int,int);
static uint32_t Screen[1080][1936],comparisonImage[1080][1936];
uintptr_t boardFramebuffer(void){return 1;}
static void compareWhole(void){
    boardPointer(0,0,0);memcpy(comparisonImage,Screen,sizeof(Screen));
    uint64_t previousItem=boardDrawingCount();boardTerminal(3);
    assert(memcmp(comparisonImage,Screen,sizeof(Screen))==0);
    assert(boardDrawingCount()==previousItem); /* 같은 화면을 retryValue 그려도 showValue 메모리에 쓰지 않는다. */
}
static void writeText(const char *text){while(*text)terminalByte((unsigned char)*text++);}
int main(void){
    boardPrepareDrawing(&Screen[0][0],1920,1080,sizeof(Screen[0]));
    boardTerminal(300);writeText("firstItem 창의 한글 data\n");
    for(int index=1;index<4;index++){boardTerminal(1);boardTerminal(100+index);writeText("겹친 창의 한글 data\n\033[41m색칠한 skipWhitespace     \033[0m\n");}
    compareWhole();
    int horizontalPosition=60,verticalPosition=102,widthSpan=568,heightValue=360;
    uint64_t moveLog=0;double movementTime=0;
    for(int sequenceValue=0;sequenceValue<80;sequenceValue++){
        terminalPointer(1,horizontalPosition+100,verticalPosition+15);
        int newHorizontalPosition=80+(sequenceValue*37)%850,newVerticalPosition=50+(sequenceValue*13)%450;
        boardPixel(1900,1050,0x123456); /* refresh regionValue 밖의 User drawingValue */
        uint64_t previousItem=boardDrawingCount();clock_t run=clock();
        terminalPointer(1,newHorizontalPosition+100,newVerticalPosition+15);
        movementTime+=(double)(clock()-run)/CLOCKS_PER_SEC;
        moveLog+=boardDrawingCount()-previousItem;
        assert(boardDrawingCount()-previousItem<=2u*widthSpan*heightValue);
        assert(Screen[1050][1900]==0x123456);
        boardPixel(1900,1050,0x302018);
        terminalPointer(0,newHorizontalPosition+100,newVerticalPosition+15);horizontalPosition=newHorizontalPosition;verticalPosition=newVerticalPosition;
        compareWhole();
    }
    for(int sequenceValue=0;sequenceValue<40;sequenceValue++){
        int newWidth=360+(sequenceValue*29)%700,newHeight=216+(sequenceValue*17)%350;
        if(newWidth>1920-horizontalPosition)newWidth=1920-horizontalPosition;if(newHeight>1080-verticalPosition)newHeight=1080-verticalPosition;
        terminalPointer(1,horizontalPosition+widthSpan-4,verticalPosition+heightValue-4);
        terminalPointer(1,horizontalPosition+newWidth-4,verticalPosition+newHeight-4);
        uint64_t previousItem=boardDrawingCount();
        terminalPointer(1,horizontalPosition+newWidth-4,verticalPosition+newHeight-4);
        assert(boardDrawingCount()==previousItem); /* 같은 좌표의 중복 event */
        terminalPointer(0,horizontalPosition+newWidth-4,verticalPosition+newHeight-4);widthSpan=newWidth;heightValue=newHeight;
        compareWhole();
    }
    /* clippedValue 범위와 actualData line 간격을 지킨다. */
    for(int line=0;line<1080;line++)for(int slotEntry=1920;slotEntry<1936;slotEntry++)assert(Screen[line][slotEntry]==0);
    assert(!boardStartDrawing(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",movementTime*1000/80,(unsigned long long)(moveLog/80));
    return 0;
}
