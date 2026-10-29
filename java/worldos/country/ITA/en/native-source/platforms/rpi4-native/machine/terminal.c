#include "../naming/machineLinkNames.h"
#include "screenInformation.h"
/* Native 네 window 합성과 UTF-8 terminal. 바뀐 영역의 completedValue 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t machineWord;
extern machineWord boardPixel(machineWord,machineWord,machineWord),boardFramebuffer(void);
extern void *memset(void *,int,size_t);
extern const unsigned char terminalFont[];
#define maximumColumns 237
#define historyLineCount 160
typedef struct {
    uint32_t characterCells[historyLineCount][maximumColumns]; uint8_t shapesList[historyLineCount][maximumColumns];
    unsigned widthValue,heightValue,columns,rowCount,wasResized;
    unsigned isLiving,xCoordinate,yCoordinate,rowPosition,columnPosition,topEntry,scroll,foregroundColour,backgroundColour,escape,parameterValue[4],parameterIndex,savedRow,savedCol;
    unsigned unsignedResult,unsignedLongValue,smallValue,alternate,caretVisible;
} Terminal;
static Terminal windowsList[4];
static int focus=-1,output,orderValue[4],entryCount,dragValue=-1,dragX,dragY;
static unsigned isPending,buttons,desktopView,hangulInput;
static const uint32_t pixelColours[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int screenVisible(int),screenPointer(int,unsigned,int,int);
extern void redrawScreen(int);
static Terminal *terminalEntry;
static unsigned wideCharacter(unsigned characterCode){return characterCode>=256?2:1;}
static void rectangularRegion(unsigned xCoordinate,unsigned yCoordinate,unsigned requestedWidthValue,unsigned requestedHeightValue,unsigned pixelColour){
    boardRectangleFill(xCoordinate,yCoordinate,requestedWidthValue,requestedHeightValue,pixelColour);
}
void terminalGlyph(unsigned xCoordinate,unsigned yCoordinate,unsigned characterCode,unsigned foregroundColour,unsigned backgroundColour){
    unsigned widthValue=wideCharacter(characterCode)*8;if(characterCode==0xffffffffu)return;
    int leftSide=xCoordinate,upperSide=yCoordinate,widthSpan=widthValue,lengthValue=16;
    if(!boardDrawingBounds(&leftSide,&upperSide,&widthSpan,&lengthValue))return;
    if(characterCode==' '){boardRectangleFill(leftSide,upperSide,widthSpan,lengthValue,backgroundColour);return;}
    unsigned lookupIndex=characterCode<65536?characterCode:characterCode>=0x1f600&&characterCode<0x1f650?65536+characterCode-0x1f600:0xfffd;
    const unsigned char *fontValue=terminalFont+lookupIndex*32;
    for(int line=upperSide;line<upperSide+lengthValue;line++){unsigned bitsList=fontValue[(line-yCoordinate)*2]*256+fontValue[(line-yCoordinate)*2+1];for(int slotEntry=leftSide;slotEntry<leftSide+widthSpan;slotEntry++)boardPixel(slotEntry,line,(bitsList&(0x8000>>(slotEntry-xCoordinate)))?foregroundColour:backgroundColour);}
}
static void nameTable(unsigned xCoordinate,unsigned yCoordinate,const char *stringData,unsigned foregroundColour,unsigned backgroundColour){while(*stringData){unsigned characterCode=(unsigned char)*stringData++, remainingCount=0;if(characterCode>=0xc0){remainingCount=characterCode<0xe0?1:characterCode<0xf0?2:3;characterCode&=(1u<<(6-remainingCount))-1;while(remainingCount--&&*stringData)characterCode=(characterCode<<6)|((unsigned char)*stringData++&63);}terminalGlyph(xCoordinate,yCoordinate,characterCode,foregroundColour,backgroundColour);xCoordinate+=wideCharacter(characterCode)*8;}}
static unsigned firstEntry(void){return terminalEntry->topEntry;}
static int isShown(void){return terminalEntry->isLiving&&focus>=0&&terminalEntry==&windowsList[focus]&&!screenVisible(focus);}
static void paintScreen(unsigned rowPosition,unsigned columnPosition){
    if(!isShown()||rowPosition<firstEntry()-terminalEntry->scroll||rowPosition>=firstEntry()-terminalEntry->scroll+terminalEntry->rowCount||columnPosition>=terminalEntry->columns)return;
    unsigned characterCode=terminalEntry->characterCells[rowPosition%historyLineCount][columnPosition],stringData=terminalEntry->shapesList[rowPosition%historyLineCount][columnPosition];
    if(wideCharacter(characterCode)==2&&columnPosition+1>=terminalEntry->columns)characterCode=' ';
    terminalGlyph(terminalEntry->xCoordinate+12+columnPosition*8,terminalEntry->yCoordinate+36+(rowPosition-firstEntry()+terminalEntry->scroll)*16,characterCode?characterCode:' ',pixelColours[stringData&15],pixelColours[stringData>>4]);
}
static void caretValue(int showWindow){if(!isShown()||terminalEntry->scroll||terminalEntry->columnPosition>=terminalEntry->columns||terminalEntry->rowPosition<terminalEntry->topEntry||terminalEntry->rowPosition>=terminalEntry->topEntry+terminalEntry->rowCount)return;
    if(!showWindow||!terminalEntry->caretVisible)paintScreen(terminalEntry->rowPosition,terminalEntry->columnPosition);else rectangularRegion(terminalEntry->xCoordinate+12+terminalEntry->columnPosition*8,terminalEntry->yCoordinate+36+(terminalEntry->rowPosition-terminalEntry->topEntry)*16+14,8,2,pixelColours[terminalEntry->foregroundColour]);}
static void contentValue(void){
    rectangularRegion(terminalEntry->xCoordinate+12,terminalEntry->yCoordinate+36,terminalEntry->columns*8,terminalEntry->rowCount*16,pixelColours[0]);
    int horizontalPosition=terminalEntry->xCoordinate+12,verticalPosition=terminalEntry->yCoordinate+36,widthSpan=terminalEntry->columns*8,lengthValue=terminalEntry->rowCount*16;
    if(boardDrawingBounds(&horizontalPosition,&verticalPosition,&widthSpan,&lengthValue)){
    unsigned firstLine=(verticalPosition-terminalEntry->yCoordinate-36)/16,lastLine=(verticalPosition+lengthValue-terminalEntry->yCoordinate-36+15)/16;
    unsigned firstSlot=(horizontalPosition-terminalEntry->xCoordinate-12)/8,lastSlot=(horizontalPosition+widthSpan-terminalEntry->xCoordinate-12+7)/8;
    if(firstSlot)firstSlot--; /* 잘림 boundaryValue 왼쪽에서 시작한 두 slotEntry 글자도 그린다. */
    for(unsigned returnedValue=firstLine;returnedValue<lastLine;returnedValue++)for(unsigned characterCode=firstSlot;characterCode<lastSlot;characterCode++){
        unsigned rowPosition=firstEntry()-terminalEntry->scroll+returnedValue,characterValue=terminalEntry->characterCells[rowPosition%historyLineCount][characterCode],stringData=terminalEntry->shapesList[rowPosition%historyLineCount][characterCode];
        if(wideCharacter(characterValue)==2&&characterCode+1>=terminalEntry->columns)characterValue=' ';
        if((characterValue==0||characterValue==' ')&&(stringData>>4)==0)continue;
        terminalGlyph(terminalEntry->xCoordinate+12+characterCode*8,terminalEntry->yCoordinate+36+returnedValue*16,characterValue?characterValue:' ',pixelColours[stringData&15],pixelColours[stringData>>4]);
    }}
    nameTable(terminalEntry->xCoordinate+12,terminalEntry->yCoordinate+terminalEntry->heightValue-18,terminalEntry->scroll?"PgDn: recent output":terminalEntry->widthValue>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);caretValue(1);
}
static void executionFrame(int identifierValue){
    terminalEntry=&windowsList[identifierValue];
    int horizontalPosition=terminalEntry->xCoordinate,verticalPosition=terminalEntry->yCoordinate,widthSpan=terminalEntry->widthValue,lengthValue=terminalEntry->heightValue;
    if(!boardDrawingBounds(&horizontalPosition,&verticalPosition,&widthSpan,&lengthValue))return;
    rectangularRegion(terminalEntry->xCoordinate,terminalEntry->yCoordinate,terminalEntry->widthValue,terminalEntry->heightValue,0x403127);
    unsigned pixelColour=identifierValue==focus?0x905020:0x604438;rectangularRegion(terminalEntry->xCoordinate,terminalEntry->yCoordinate,terminalEntry->widthValue,30,pixelColour);
    nameTable(terminalEntry->xCoordinate+12,terminalEntry->yCoordinate+7,"JKOROS Terminal",0xffffff,pixelColour);
    char numericValue[2]={(char)('1'+identifierValue),0};nameTable(terminalEntry->xCoordinate+148,terminalEntry->yCoordinate+7,numericValue,0xffffff,pixelColour);
    nameTable(terminalEntry->xCoordinate+240,terminalEntry->yCoordinate+7,terminalEntry->widthValue>=500?(hangulInput?"[EN] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(hangulInput?"[EN]":"[EN]"),0xffffff,pixelColour);
    rectangularRegion(terminalEntry->xCoordinate+terminalEntry->widthValue-32,terminalEntry->yCoordinate+4,26,22,0x5555b8);nameTable(terminalEntry->xCoordinate+terminalEntry->widthValue-24,terminalEntry->yCoordinate+7,"X",0xffffff,0x5555b8);
    contentValue();
}
static void drawScene(void){
    if(!desktopView)return;rectangularRegion(0,0,boardScreenWidth(),boardScreenHeight(),0x302018);rectangularRegion(0,0,boardScreenWidth(),32,0x403127);
    rectangularRegion(6,4,136,24,0x905020);nameTable(14,8,"+ New terminal",0xffffff,0x905020);
    for(int ordinalIndex=0;ordinalIndex<4;ordinalIndex++)if(windowsList[ordinalIndex].isLiving){unsigned characterCode=focus==ordinalIndex?0x905020:0x604438;rectangularRegion(154+ordinalIndex*112,4,106,24,characterCode);nameTable(160+ordinalIndex*112,8,"Terminal",0xffffff,characterCode);char stringData[2]={(char)('1'+ordinalIndex),0};nameTable(232+ordinalIndex*112,8,stringData,0xffffff,characterCode);}
    if(!entryCount)nameTable(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int ordinalIndex=0;ordinalIndex<entryCount;ordinalIndex++)executionFrame(orderValue[ordinalIndex]);redrawScreen(focus);terminalEntry=&windowsList[output];
}
static void paintRegion(int horizontalPosition,int verticalPosition,int widthSpan,int lengthValue){
    if(!desktopView||!boardDrawingBounds(&horizontalPosition,&verticalPosition,&widthSpan,&lengthValue))return;
    for(int line=verticalPosition;line<verticalPosition+lengthValue;line+=32){
        int bandHeight=verticalPosition+lengthValue-line;if(bandHeight>32)bandHeight=32;
        if(boardStartDrawing(horizontalPosition,line,widthSpan,bandHeight)){drawScene();boardFinishDrawing();}
    }
}
static void redraw(void){paintRegion(0,0,boardScreenWidth(),boardScreenHeight());}
/* 서로 겹치지 않는 새 window 영역과 previousItem 자리의 네 띠를 복구한다. */
static void paintWindowBounds(int horizontalPosition,int verticalPosition,int widthSpan,int lengthValue,Terminal *window){
    int leftSide=horizontalPosition>(int)window->xCoordinate?horizontalPosition:(int)window->xCoordinate;
    int upperSide=verticalPosition>(int)window->yCoordinate?verticalPosition:(int)window->yCoordinate;
    int right=horizontalPosition+widthSpan<(int)(window->xCoordinate+window->widthValue)?horizontalPosition+widthSpan:(int)(window->xCoordinate+window->widthValue);
    int lowerSide=verticalPosition+lengthValue<(int)(window->yCoordinate+window->heightValue)?verticalPosition+lengthValue:(int)(window->yCoordinate+window->heightValue);
    paintRegion(window->xCoordinate,window->yCoordinate,window->widthValue,window->heightValue);
    if(leftSide>=right||upperSide>=lowerSide){paintRegion(horizontalPosition,verticalPosition,widthSpan,lengthValue);return;}
    paintRegion(horizontalPosition,verticalPosition,widthSpan,upperSide-verticalPosition);
    paintRegion(horizontalPosition,lowerSide,widthSpan,verticalPosition+lengthValue-lowerSide);
    paintRegion(horizontalPosition,upperSide,leftSide-horizontalPosition,lowerSide-upperSide);
    paintRegion(right,upperSide,horizontalPosition+widthSpan-right,lowerSide-upperSide);
}
static void signalFocus(void){isPending=(isPending&~15u)|(unsigned)(focus+1)|0x10000;}
void terminalInputMode(unsigned korean){
    hangulInput=korean!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(focus>=0){
        Terminal *windowEntry=&windowsList[focus];
        nameTable(windowEntry->xCoordinate+240,windowEntry->yCoordinate+7,windowEntry->widthValue>=500?(hangulInput?"[EN] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(hangulInput?"[EN]":"[EN]"),0xffffff,0x905020);
    }
}
static void bringToFront(int identifierValue){if(identifierValue<0||identifierValue>=4||!windowsList[identifierValue].isLiving)return;int currentPosition=0;while(currentPosition<entryCount&&orderValue[currentPosition]!=identifierValue)currentPosition++;for(;currentPosition+1<entryCount;currentPosition++)orderValue[currentPosition]=orderValue[currentPosition+1];orderValue[entryCount-1]=identifierValue;focus=identifierValue;signalFocus();redraw();}
static void blank(unsigned rowPosition){for(unsigned characterCode=0;characterCode<maximumColumns;characterCode++){terminalEntry->characterCells[rowPosition%historyLineCount][characterCode]=0;terminalEntry->shapesList[rowPosition%historyLineCount][characterCode]=terminalEntry->foregroundColour|(terminalEntry->backgroundColour<<4);}}
static void clearContents(void){terminalEntry->rowPosition=terminalEntry->columnPosition=terminalEntry->topEntry=terminalEntry->scroll=0;for(unsigned returnedValue=0;returnedValue<historyLineCount;returnedValue++)blank(returnedValue);if(isShown())contentValue();}
static int createEntry(void){
    if(!boardFramebuffer())return -19;int identifierValue=0;while(identifierValue<4&&windowsList[identifierValue].isLiving)identifierValue++;if(identifierValue==4)return -28;
    desktopView=1;terminalEntry=&windowsList[identifierValue];memset(terminalEntry,0,sizeof(*terminalEntry));terminalEntry->isLiving=1;terminalEntry->widthValue=568;terminalEntry->heightValue=360;terminalEntry->columns=68;terminalEntry->rowCount=19;terminalEntry->xCoordinate=12+identifierValue*16;terminalEntry->yCoordinate=48+identifierValue*18;terminalEntry->foregroundColour=7;terminalEntry->caretVisible=1;
    for(unsigned returnedValue=0;returnedValue<historyLineCount;returnedValue++)blank(returnedValue);orderValue[entryCount++]=identifierValue;focus=identifierValue;isPending|=1u<<(4+identifierValue);signalFocus();redraw();return identifierValue+1;
}
static void closeWindow(int identifierValue){
    if(identifierValue<0||identifierValue>=4||!windowsList[identifierValue].isLiving)return;windowsList[identifierValue].isLiving=0;isPending|=1u<<(8+identifierValue);
    int currentPosition=0;while(currentPosition<entryCount&&orderValue[currentPosition]!=identifierValue)currentPosition++;for(;currentPosition+1<entryCount;currentPosition++)orderValue[currentPosition]=orderValue[currentPosition+1];entryCount--;
    if(focus==identifierValue)focus=entryCount?orderValue[entryCount-1]:-1;signalFocus();redraw();
}
static void newline(void){terminalEntry->columnPosition=0;terminalEntry->rowPosition++;if(terminalEntry->rowPosition>=terminalEntry->topEntry+terminalEntry->rowCount){terminalEntry->topEntry++;blank(terminalEntry->rowPosition);if(isShown())contentValue();}}
static void codePoint(unsigned characterCode){
    if(characterCode==13){terminalEntry->columnPosition=0;return;}if(characterCode==10){newline();return;}if(characterCode==8){if(terminalEntry->columnPosition)terminalEntry->columnPosition--;return;}
    if(characterCode==9){unsigned itemCount=8-terminalEntry->columnPosition%8;while(itemCount--)codePoint(' ');return;}if(characterCode<32||characterCode==127)return;
    unsigned requestedWidthValue=wideCharacter(characterCode);if(terminalEntry->columnPosition+requestedWidthValue>terminalEntry->columns)newline();
    if(terminalEntry->characterCells[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition]==0xffffffffu&&terminalEntry->columnPosition){terminalEntry->characterCells[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition-1]=' ';paintScreen(terminalEntry->rowPosition,terminalEntry->columnPosition-1);}
    if(wideCharacter(terminalEntry->characterCells[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition])==2&&terminalEntry->columnPosition+1<terminalEntry->columns){terminalEntry->characterCells[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition+1]=' ';paintScreen(terminalEntry->rowPosition,terminalEntry->columnPosition+1);}
    terminalEntry->characterCells[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition]=characterCode;terminalEntry->shapesList[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition]=terminalEntry->foregroundColour|(terminalEntry->backgroundColour<<4);
    if(requestedWidthValue==2)terminalEntry->characterCells[terminalEntry->rowPosition%historyLineCount][terminalEntry->columnPosition+1]=0xffffffffu;
    paintScreen(terminalEntry->rowPosition,terminalEntry->columnPosition);terminalEntry->columnPosition+=requestedWidthValue;
}
static void handleControlSequence(unsigned characterCode){
    unsigned itemCount=terminalEntry->parameterValue[0]?terminalEntry->parameterValue[0]:1;
    if(characterCode=='m')for(unsigned ordinalIndex=0;ordinalIndex<=terminalEntry->parameterIndex;ordinalIndex++){unsigned dataPosition=terminalEntry->parameterValue[ordinalIndex];if(!dataPosition){terminalEntry->foregroundColour=7;terminalEntry->backgroundColour=0;}if(dataPosition==1&&terminalEntry->foregroundColour<8)terminalEntry->foregroundColour+=8;if(dataPosition==7){unsigned retainValue=terminalEntry->foregroundColour;terminalEntry->foregroundColour=terminalEntry->backgroundColour;terminalEntry->backgroundColour=retainValue;}if(dataPosition>=30&&dataPosition<=37)terminalEntry->foregroundColour=dataPosition-30;if(dataPosition>=90&&dataPosition<=97)terminalEntry->foregroundColour=dataPosition-90+8;if(dataPosition>=40&&dataPosition<=47)terminalEntry->backgroundColour=dataPosition-40;if(dataPosition>=100&&dataPosition<=107)terminalEntry->backgroundColour=dataPosition-100+8;if(dataPosition==39)terminalEntry->foregroundColour=7;if(dataPosition==49)terminalEntry->backgroundColour=0;}
    if(characterCode=='J'&&(terminalEntry->parameterValue[0]==2||terminalEntry->parameterValue[0]==3))clearContents();
    if(characterCode=='K'){unsigned departurePosition=terminalEntry->parameterValue[0]==2?0:terminalEntry->columnPosition,arrivalPosition=terminalEntry->parameterValue[0]==1?terminalEntry->columnPosition+1:terminalEntry->columns;if(terminalEntry->parameterValue[0]==1)departurePosition=0;for(unsigned ordinalIndex=departurePosition;ordinalIndex<arrivalPosition&&ordinalIndex<terminalEntry->columns;ordinalIndex++){
        unsigned rowValue=terminalEntry->rowPosition%historyLineCount,characterValue=terminalEntry->characterCells[rowValue][ordinalIndex],shapeValue=terminalEntry->foregroundColour|(terminalEntry->backgroundColour<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fontValue 화소를 되풀이해 칠하지 않는다. */
        int isModified=(characterValue!=0&&characterValue!=' ')||terminalEntry->shapesList[rowValue][ordinalIndex]!=shapeValue;
        terminalEntry->characterCells[rowValue][ordinalIndex]=' ';terminalEntry->shapesList[rowValue][ordinalIndex]=shapeValue;
        if(isModified)paintScreen(terminalEntry->rowPosition,ordinalIndex);
    }}
    if(characterCode=='D')terminalEntry->columnPosition=itemCount>terminalEntry->columnPosition?0:terminalEntry->columnPosition-itemCount;if(characterCode=='C')terminalEntry->columnPosition=terminalEntry->columnPosition+itemCount>=terminalEntry->columns?terminalEntry->columns-1:terminalEntry->columnPosition+itemCount;
    if(characterCode=='G')terminalEntry->columnPosition=itemCount>terminalEntry->columns?terminalEntry->columns-1:itemCount-1;if(characterCode=='A')terminalEntry->rowPosition=itemCount>terminalEntry->rowPosition-terminalEntry->topEntry?terminalEntry->topEntry:terminalEntry->rowPosition-itemCount;
    if(characterCode=='B')terminalEntry->rowPosition=terminalEntry->rowPosition+itemCount>=terminalEntry->topEntry+terminalEntry->rowCount?terminalEntry->topEntry+terminalEntry->rowCount-1:terminalEntry->rowPosition+itemCount;
    if(characterCode=='H'||characterCode=='f'){terminalEntry->rowPosition=terminalEntry->topEntry+(itemCount>terminalEntry->rowCount?terminalEntry->rowCount:itemCount)-1;unsigned xCoordinate=terminalEntry->parameterValue[1]?terminalEntry->parameterValue[1]:1;terminalEntry->columnPosition=(xCoordinate>terminalEntry->columns?terminalEntry->columns:xCoordinate)-1;}
    if(characterCode=='s'){terminalEntry->savedRow=terminalEntry->rowPosition;terminalEntry->savedCol=terminalEntry->columnPosition;}if(characterCode=='u'){terminalEntry->rowPosition=terminalEntry->savedRow;terminalEntry->columnPosition=terminalEntry->savedCol<terminalEntry->columns?terminalEntry->savedCol:terminalEntry->columns-1;}
    if((characterCode=='h'||characterCode=='l')&&terminalEntry->parameterValue[0]==25)terminalEntry->caretVisible=characterCode=='h';
}
void terminalByte(unsigned secondValue){
    terminalEntry=&windowsList[output];if(!terminalEntry->isLiving)return;caretValue(0);if(terminalEntry->scroll){terminalEntry->scroll=0;if(isShown())contentValue();}
    if(terminalEntry->escape==1){terminalEntry->escape=secondValue=='['?2:0;terminalEntry->parameterIndex=0;for(unsigned ordinalIndex=0;ordinalIndex<4;ordinalIndex++)terminalEntry->parameterValue[ordinalIndex]=0;}
    else if(terminalEntry->escape==2){if(secondValue=='?'){}else if(secondValue>='0'&&secondValue<='9'){if(terminalEntry->parameterValue[terminalEntry->parameterIndex]<10000)terminalEntry->parameterValue[terminalEntry->parameterIndex]=terminalEntry->parameterValue[terminalEntry->parameterIndex]*10+secondValue-'0';}else if(secondValue==';'&&terminalEntry->parameterIndex<3)terminalEntry->parameterIndex++;else{handleControlSequence(secondValue);terminalEntry->escape=0;}}
    else if(secondValue==27){terminalEntry->unsignedLongValue=0;terminalEntry->escape=1;}else{
        if(terminalEntry->unsignedLongValue&&(secondValue&0xc0)!=0x80){terminalEntry->unsignedLongValue=0;codePoint(0xfffd);}
        if(terminalEntry->unsignedLongValue){terminalEntry->unsignedResult=terminalEntry->unsignedResult*64+(secondValue&63);if(--terminalEntry->unsignedLongValue==0)codePoint(terminalEntry->unsignedResult<terminalEntry->smallValue||terminalEntry->unsignedResult>0x10ffff||(terminalEntry->unsignedResult>=0xd800&&terminalEntry->unsignedResult<=0xdfff)?0xfffd:terminalEntry->unsignedResult);}
        else if(secondValue<128)codePoint(secondValue);else if(secondValue>=0xc2&&secondValue<=0xf4){terminalEntry->unsignedLongValue=secondValue<0xe0?1:secondValue<0xf0?2:3;terminalEntry->unsignedResult=secondValue&((1u<<(6-terminalEntry->unsignedLongValue))-1);terminalEntry->smallValue=terminalEntry->unsignedLongValue==1?128:terminalEntry->unsignedLongValue==2?2048:65536;}else codePoint(0xfffd);
    }caretValue(1);
}
int terminalPending(void){return isPending!=0;}
/* cornerValue index: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int resizeDrag=-1,grabbedCorner,grabbedX,grabbedY,initialHorizontalPosition,initialVerticalPosition,initialWidthValue,initialHeightValue;
static int pointedWindow(int horizontalPosition,int verticalPosition) {
    for(int sequenceValue=entryCount-1;sequenceValue>=0;sequenceValue--){
        int identifierValue=orderValue[sequenceValue];Terminal *window=&windowsList[identifierValue];
        if(horizontalPosition>=(int)window->xCoordinate&&verticalPosition>=(int)window->yCoordinate&&
           horizontalPosition<(int)(window->xCoordinate+window->widthValue)&&verticalPosition<(int)(window->yCoordinate+window->heightValue))return identifierValue;
    }return -1;
}
static int findCorner(int identifierValue,int horizontalPosition,int verticalPosition) {
    if(identifierValue<0)return 0;Terminal *window=&windowsList[identifierValue];
    int leftSide=horizontalPosition<(int)window->xCoordinate+8,right=horizontalPosition>=(int)(window->xCoordinate+window->widthValue)-8;
    int upperSide=verticalPosition<(int)window->yCoordinate+8,lowerSide=verticalPosition>=(int)(window->yCoordinate+window->heightValue)-8;
    return (leftSide||right)&&(upperSide||lowerSide)?1+right+lowerSide*2:0;
}
static int separatorValue(int value,int minimumValue,int maximumValue){return value<minimumValue?minimumValue:value>maximumValue?maximumValue:value;}
static void moveResize(int horizontalPosition,int verticalPosition) {
    Terminal *window=&windowsList[resizeDrag];int leftSide=initialHorizontalPosition,upperSide=initialVerticalPosition,right=initialHorizontalPosition+initialWidthValue,lowerSide=initialVerticalPosition+initialHeightValue;
    if(grabbedCorner==1||grabbedCorner==3)leftSide=separatorValue(initialHorizontalPosition+horizontalPosition-grabbedX,0,right-360);
    else right=separatorValue(initialHorizontalPosition+initialWidthValue+horizontalPosition-grabbedX,leftSide+360,boardScreenWidth());
    if(grabbedCorner<=2)upperSide=separatorValue(initialVerticalPosition+verticalPosition-grabbedY,34,lowerSide-216);
    else lowerSide=separatorValue(initialVerticalPosition+initialHeightValue+verticalPosition-grabbedY,upperSide+216,boardScreenHeight());
    unsigned columns=(right-leftSide-24)/8,rowCount=(lowerSide-upperSide-56)/16;
    if(window->columns!=columns||window->rowCount!=rowCount){
        window->wasResized=1;window->columns=columns;window->rowCount=rowCount;
        if(window->columnPosition>=columns)window->columnPosition=columns-1;
        if(window->rowPosition>=window->topEntry+rowCount)window->topEntry=window->rowPosition-rowCount+1;
        unsigned capacityLimit=window->topEntry;if(capacityLimit>historyLineCount-rowCount)capacityLimit=historyLineCount-rowCount;
        if(window->scroll>capacityLimit)window->scroll=capacityLimit;
    }
    int oldHorizontalPosition=window->xCoordinate,oldVerticalPosition=window->yCoordinate,oldWidth=window->widthValue,oldLength=window->heightValue;
    if(oldHorizontalPosition==leftSide&&oldVerticalPosition==upperSide&&oldWidth==right-leftSide&&oldLength==lowerSide-upperSide)return;
    window->xCoordinate=leftSide;window->yCoordinate=upperSide;window->widthValue=right-leftSide;window->heightValue=lowerSide-upperSide;
    paintWindowBounds(oldHorizontalPosition,oldVerticalPosition,oldWidth,oldLength,window);
}
void terminalPointer(unsigned nextItem,int xCoordinate,int yCoordinate){
    unsigned isPressed=nextItem&~buttons;buttons=nextItem;
    if(!desktopView){dragValue=-1;resizeDrag=-1;boardPointer(xCoordinate,yCoordinate,1);return;}
    if(!(nextItem&1)){dragValue=-1;resizeDrag=-1;}
    if(resizeDrag>=0&&!windowsList[resizeDrag].isLiving)resizeDrag=-1;
    if(dragValue>=0&&!windowsList[dragValue].isLiving)dragValue=-1;
    if(resizeDrag>=0){
        moveResize(xCoordinate,yCoordinate);boardPointer(xCoordinate,yCoordinate,grabbedCorner==1||grabbedCorner==4?2:3);return;
    }
    boardPointer(xCoordinate,yCoordinate,1);
    if(dragValue>=0){
        Terminal *window=&windowsList[dragValue];
        int oldHorizontalPosition=window->xCoordinate,oldVerticalPosition=window->yCoordinate;
        window->xCoordinate=separatorValue(xCoordinate-dragX,0,boardScreenWidth()-window->widthValue);
        window->yCoordinate=separatorValue(yCoordinate-dragY,34,boardScreenHeight()-window->heightValue);
        if(oldHorizontalPosition!=(int)window->xCoordinate||oldVerticalPosition!=(int)window->yCoordinate)paintWindowBounds(oldHorizontalPosition,oldVerticalPosition,window->widthValue,window->heightValue,window);
        return;
    }
    extern int screenOverlay(int,int,int);
    if(screenOverlay(focus,xCoordinate,yCoordinate)){screenPointer(focus,isPressed,xCoordinate,yCoordinate);return;}
    int identifierValue=pointedWindow(xCoordinate,yCoordinate),cornerValue=findCorner(identifierValue,xCoordinate,yCoordinate);
    if(cornerValue)boardPointer(xCoordinate,yCoordinate,cornerValue==1||cornerValue==4?2:3);
    if(isPressed&1){
        if(cornerValue){
            Terminal *window=&windowsList[identifierValue];resizeDrag=identifierValue;grabbedCorner=cornerValue;grabbedX=xCoordinate;grabbedY=yCoordinate;
            initialHorizontalPosition=window->xCoordinate;initialVerticalPosition=window->yCoordinate;initialWidthValue=window->widthValue;initialHeightValue=window->heightValue;
            if(identifierValue!=focus)bringToFront(identifierValue);return;
        }
        if(yCoordinate<32&&xCoordinate>=6&&xCoordinate<142){createEntry();return;}
        if(yCoordinate<32&&xCoordinate>=154&&xCoordinate<602){bringToFront((xCoordinate-154)/112);return;}
        if(identifierValue>=0){
            Terminal *window=&windowsList[identifierValue];
            if(yCoordinate<(int)window->yCoordinate+30&&xCoordinate>=(int)(window->xCoordinate+window->widthValue)-32){closeWindow(identifierValue);return;}
            if(identifierValue!=focus)bringToFront(identifierValue);
            if(yCoordinate<(int)window->yCoordinate+30){dragValue=identifierValue;dragX=xCoordinate-window->xCoordinate;dragY=yCoordinate-window->yCoordinate;}return;
        }
    }
    if(focus>=0&&(isPressed&(8|16))){terminalEntry=&windowsList[focus];if(isPressed&8){unsigned capacityLimit=terminalEntry->topEntry;if(capacityLimit>historyLineCount-terminalEntry->rowCount)capacityLimit=historyLineCount-terminalEntry->rowCount;terminalEntry->scroll=terminalEntry->scroll+9>capacityLimit?capacityLimit:terminalEntry->scroll+9;}else terminalEntry->scroll=terminalEntry->scroll<9?0:terminalEntry->scroll-9;redraw();}
}
void terminalHotkey(unsigned pressedValue){if(pressedValue==1)createEntry();if(pressedValue==2&&entryCount)bringToFront(orderValue[0]);if(pressedValue==3)closeWindow(focus);}
machineWord boardTerminal(machineWord action){
    if(action==300){if(!windowsList[output].isLiving)return createEntry();desktopView=1;redraw();return 0;}
    if(action==0){closeWindow(focus);return 0;}if(action==1)return (uint32_t)createEntry();if(action==2)return focus>=0;
    if(action==9){desktopView=0;return 0;}if(action==7)return entryCount;if(action==10)return focus+1;if(action==11)return output;
    if(action==13){Terminal *window=&windowsList[output];return window->isLiving?(window->rowCount<<16)|window->columns:(19<<16)|68;}
    if(action==14){unsigned value=windowsList[output].wasResized;windowsList[output].wasResized=0;return value;}
    if(action==12){unsigned value=isPending;isPending=0;return value;}
    if(action>=20&&action<24)return windowsList[action-20].isLiving;
    if(action>=100&&action<104){output=action-100;terminalEntry=&windowsList[output];return 0;}
    if(action>=200&&action<204){bringToFront(action-200);return 0;}
    if(action==3){redraw();return 0;}terminalEntry=&windowsList[output];if(!terminalEntry->isLiving)return 0;
    if(action==4)clearContents();if(action==5||action==6){unsigned previousItem=buttons;terminalPointer(action==5?8:16,0,0);buttons=previousItem;}return 1;
}
