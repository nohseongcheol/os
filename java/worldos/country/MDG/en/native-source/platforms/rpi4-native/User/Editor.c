/* vi-style UTF-8 editor, a protected EL0 program using only JKOROS syscalls. */
#include "invoke.h"
#include "FileABI.h"
#define editorCapacity 16384
static unsigned char text[editorCapacity],undoData[editorCapacity],copiedData[editorCapacity],resultData[1024];
static int lengthValue,indexValue,topEntry,leftSide,wasChanged,insert,undoLength,upperSide,undoChanges,haveUndo,copyLength,usedCapacity,columns=68,rowCount=19;
static char fileEntryName[64],command[128],findEntry[128];
static const char *noticeText="NORMAL  i:insert  :w:save  :q:quit";
static unsigned pendingKey;
static int helpCategory,stateImage,stateQueue;
static void flush(void){if(usedCapacity){userInvoke(1,1,(uintptr_t)resultData,usedCapacity,0,0,0);usedCapacity=0;}}
static void byteData(unsigned characterCode){if(stateImage){if((characterCode&192)!=128){stateQueue+=characterCode>=196?2:1;}if(stateQueue>=columns)return;}if(usedCapacity==(int)sizeof(resultData))flush();resultData[usedCapacity++]=characterCode;}
static void emitText(const char *stringData){while(*stringData)byteData((unsigned char)*stringData++);}
static void numericValue(unsigned itemCount){char secondValue[12];int ordinalIndex=0;do{secondValue[ordinalIndex++]='0'+itemCount%10;itemCount/=10;}while(itemCount);while(ordinalIndex)byteData(secondValue[--ordinalIndex]);}
static void moveValue(int rowPosition,int columnPosition){emitText("\033[");numericValue(rowPosition);byteData(';');numericValue(columnPosition);byteData('H');}
static int previous(int dataPosition){if(dataPosition){dataPosition--;while(dataPosition>0&&(text[dataPosition]&192)==128)dataPosition--;}return dataPosition;}
static int nextItem(int dataPosition){if(dataPosition<lengthValue){dataPosition++;while(dataPosition<lengthValue&&(text[dataPosition]&192)==128)dataPosition++;}return dataPosition;}
static int run(int dataPosition){while(dataPosition>0&&text[dataPosition-1]!='\n')dataPosition--;return dataPosition;}
static int endOffset(int dataPosition){while(dataPosition<lengthValue&&text[dataPosition]!='\n')dataPosition++;return dataPosition;}
static int widthValue(unsigned characterCode){return characterCode>=196?2:1;}
static int column(int dataPosition){int characterCode=0;for(int ordinalIndex=run(dataPosition);ordinalIndex<dataPosition;ordinalIndex=nextItem(ordinalIndex))characterCode+=text[ordinalIndex]=='\t'?4-characterCode%4:widthValue(text[ordinalIndex]);return characterCode;}
static void checkpoint(void){for(int ordinalIndex=0;ordinalIndex<lengthValue;ordinalIndex++)undoData[ordinalIndex]=text[ordinalIndex];undoLength=lengthValue;upperSide=indexValue;undoChanges=wasChanged;haveUndo=1;}
static void clearBytes(int departurePosition,int arrivalPosition){checkpoint();for(int ordinalIndex=arrivalPosition;ordinalIndex<lengthValue;ordinalIndex++)text[departurePosition+ordinalIndex-arrivalPosition]=text[ordinalIndex];lengthValue-=arrivalPosition-departurePosition;indexValue=departurePosition;wasChanged=1;}
static int appendValue(const unsigned char *stringData,int itemCount){if(itemCount>editorCapacity-lengthValue){noticeText="File full (16384 bytes)";return 0;}checkpoint();for(int ordinalIndex=lengthValue-1;ordinalIndex>=indexValue;ordinalIndex--)text[ordinalIndex+itemCount]=text[ordinalIndex];for(int ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)text[indexValue+ordinalIndex]=stringData[ordinalIndex];lengthValue+=itemCount;indexValue+=itemCount;wasChanged=1;return 1;}
static void vertical(int differenceValue){int columnPosition=column(indexValue),dataPosition=run(indexValue);if(differenceValue<0){if(!dataPosition)return;dataPosition=run(dataPosition-1);}else{dataPosition=endOffset(dataPosition);if(dataPosition==lengthValue)return;dataPosition++;}int characterCode=0;while(dataPosition<lengthValue&&text[dataPosition]!='\n'&&characterCode<columnPosition){characterCode+=text[dataPosition]=='\t'?4-characterCode%4:widthValue(text[dataPosition]);dataPosition=nextItem(dataPosition);}indexValue=dataPosition;}
static void drawScreen(void){
    if(indexValue>lengthValue)indexValue=lengthValue;if(topEntry>indexValue)topEntry=run(indexValue);topEntry=run(topEntry);
    int rowPosition=0;for(int ordinalIndex=topEntry;ordinalIndex<indexValue;ordinalIndex++)if(text[ordinalIndex]=='\n')rowPosition++;
    while(rowPosition>=rowCount-1){topEntry=endOffset(topEntry);if(topEntry<lengthValue)topEntry++;rowPosition--;}
    int columnPosition=column(indexValue);if(columnPosition<leftSide)leftSide=columnPosition;if(columnPosition-leftSide>=columns-1)leftSide=columnPosition-columns+2;
    emitText("\033[?25l");int dataPosition=topEntry;
    for(int returnedValue=0;returnedValue<rowCount-1;returnedValue++){
        moveValue(returnedValue+1,1);emitText("\033[0m\033[2K");int characterCode=0,isPainted=0;
        if(dataPosition>=lengthValue&&returnedValue>rowPosition){emitText("\033[90m~\033[0m");continue;}
        while(dataPosition<lengthValue&&text[dataPosition]!='\n'){
            int nextOffset=nextItem(dataPosition),requestedWidthValue=text[dataPosition]=='\t'?4-characterCode%4:widthValue(text[dataPosition]);
            if(characterCode>=leftSide&&characterCode-leftSide+requestedWidthValue<columns){
                if(text[dataPosition]=='\t'){for(int innerOrdinal=0;innerOrdinal<requestedWidthValue;innerOrdinal++)byteData(' ');}else if(text[dataPosition]<32||text[dataPosition]==127){byteData('?');}else for(int innerOrdinal=dataPosition;innerOrdinal<nextOffset;innerOrdinal++)byteData(text[innerOrdinal]);isPainted+=requestedWidthValue;
            }characterCode+=requestedWidthValue;dataPosition=nextOffset;
        }
        (void)isPainted;if(dataPosition<lengthValue)dataPosition++;
    }
    moveValue(rowCount,1);emitText("\033[7m\033[2K");stateImage=1;stateQueue=0;emitText(insert?"INSERT ":"NORMAL ");
    int namebytes=0;while(fileEntryName[namebytes]&&namebytes<30)byteData(fileEntryName[namebytes++]);emitText(wasChanged?" [+] ":" ");
    emitText("L");int line=1;for(int ordinalIndex=0;ordinalIndex<indexValue;ordinalIndex++)if(text[ordinalIndex]=='\n')line++;numericValue(line);emitText(" ");
    // A second status is printed only when it fits; command/message is ASCII.
    if(noticeText){int itemCount=0;emitText(" | ");while(noticeText[itemCount]&&itemCount<20)byteData(noticeText[itemCount++]);}
    stateImage=0;emitText("\033[0m");moveValue(rowPosition+1,columnPosition-leftSide+1);emitText("\033[?25h");flush();
}
static int pressedValue(void){
    if(pendingKey){int thirdIndex=pendingKey;pendingKey=0;return thirdIndex;}
    for(;;){
        int thirdIndex=userInvoke(16,1,0,0,0,0,0);
        unsigned size=userInvoke(16,3,0,0,0,0,0);
        if(columns!=(int)(size&65535)||rowCount!=(int)(size>>16)){
            columns=size&65535;rowCount=size>>16;drawScreen();
            if(helpCategory){moveValue(rowCount,1);emitText("\033[0m\033[2K");byteData(helpCategory);emitText(command);flush();}
        }
        if(thirdIndex>=0)return thirdIndex;
    }
}
static int escaped(void){
    unsigned currentPosition=userInvoke(7,0,0,0,0,0,0);int thirdIndex=-1;
    while((unsigned)userInvoke(7,0,0,0,0,0,0)-currentPosition<100){thirdIndex=userInvoke(16,1,0,0,0,0,0);if(thirdIndex>=0)break;}
    if(thirdIndex<0)return 27;if(thirdIndex!='['&&thirdIndex!='O'){pendingKey=thirdIndex;return 27;}
    int itemCount=0;for(int ordinalIndex=0;ordinalIndex<12;ordinalIndex++){thirdIndex=pressedValue();if(thirdIndex>='0'&&thirdIndex<='9'){itemCount=itemCount*10+thirdIndex-'0';continue;}if(thirdIndex=='A')return 1001;if(thirdIndex=='B')return 1002;if(thirdIndex=='C')return 1003;if(thirdIndex=='D')return 1004;if(thirdIndex=='H')return 1005;if(thirdIndex=='F')return 1006;if(thirdIndex=='~')return itemCount==3?1007:itemCount==5?1008:itemCount==6?1009:itemCount==1?1005:itemCount==4?1006:27;return 27;}return 27;
}
static int storeValue(void){
    int fileHandle=openFile(fileEntryName,ReadWrite|CreateIfMissing|TruncateContents,0600);if(fileHandle<0){noticeText="Cannot open for save";return 0;}
    intptr_t itemCount=writeFileData(fileHandle,text,lengthValue);closeFile(fileHandle);if(itemCount!=lengthValue){noticeText="Write failed";return 0;}wasChanged=0;noticeText="Saved (RAM)";return 1;
}
static int equal(const char *firstValue,const char *secondValue){while(*firstValue&&*firstValue==*secondValue){firstValue++;secondValue++;}return *firstValue==*secondValue;}
static void findNext(void){int itemCount=0;while(findEntry[itemCount])itemCount++;if(!itemCount){noticeText="No search pattern";return;}for(int ordinalIndex=1;ordinalIndex<=lengthValue;ordinalIndex++){int dataPosition=(indexValue+ordinalIndex)%(lengthValue?lengthValue:1),innerOrdinal=0;while(innerOrdinal<itemCount&&dataPosition+innerOrdinal<lengthValue&&text[dataPosition+innerOrdinal]==(unsigned char)findEntry[innerOrdinal])innerOrdinal++;if(innerOrdinal==itemCount){indexValue=dataPosition;noticeText="Match";return;}}noticeText="Pattern not found";}
static int prompt(int categoryValue){
    int itemCount=0;command[0]=0;
    for(;;){moveValue(rowCount,1);emitText("\033[0m\033[2K");byteData(categoryValue);emitText(command);flush();helpCategory=categoryValue;int thirdIndex=pressedValue();helpCategory=0;
        if(thirdIndex==27||thirdIndex==3)return 0;if(thirdIndex==13||thirdIndex==10)break;
        if(thirdIndex==127||thirdIndex==8){if(itemCount){itemCount--;while(itemCount>0&&((unsigned char)command[itemCount]&192)==128)itemCount--;command[itemCount]=0;}continue;}
        if(thirdIndex>=32&&thirdIndex<256&&itemCount<120){command[itemCount++]=thirdIndex;command[itemCount]=0;}
    }
    if(categoryValue=='/'){for(int ordinalIndex=0;ordinalIndex<=itemCount;ordinalIndex++)findEntry[ordinalIndex]=command[ordinalIndex];findNext();return 0;}
    if(equal(command,"q!"))return 1;
    if(equal(command,"q")){if(!wasChanged)return 1;noticeText="Unsaved: :w or :q!";return 0;}
    if(equal(command,"wq")||equal(command,"x"))return storeValue();
    if(equal(command,"w")){storeValue();return 0;}
    if(command[0]=='w'&&command[1]==' '){int ordinalIndex=2;while(command[ordinalIndex]==' ')ordinalIndex++;int size=itemCount-ordinalIndex;if(size<1||size>63){noticeText="Invalid file name";return 0;}for(int innerOrdinal=0;innerOrdinal<size;innerOrdinal++)fileEntryName[innerOrdinal]=command[ordinalIndex+innerOrdinal];fileEntryName[size]=0;storeValue();return 0;}
    int line=0;for(int ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++){if(command[ordinalIndex]<'0'||command[ordinalIndex]>'9'){line=0;break;}line=line*10+command[ordinalIndex]-'0';if(line>16384){line=0;break;}}
    if(line){indexValue=0;while(--line&&indexValue<lengthValue){indexValue=endOffset(indexValue);if(indexValue<lengthValue)indexValue++;}return 0;}
    noticeText="Unknown vi command";return 0;
}
int startUserProgram(int ignoredValue){
    (void)ignoredValue;if(userArgumentCount()!=1||userArgument(0,fileEntryName,sizeof(fileEntryName))<0){emitText("Usage: vi FILE\n");flush();return 2;}
    int fileHandle=openFile(fileEntryName,readOnlyValue,0);
    if(fileHandle>=0){int itemCount=fileSize(fileHandle);if(itemCount<0||itemCount>editorCapacity){closeFile(fileHandle);return 1;}lengthValue=readFileData(fileHandle,text,itemCount);closeFile(fileHandle);if(lengthValue!=itemCount)return 1;for(int ordinalIndex=0;ordinalIndex<lengthValue;ordinalIndex++)if(!text[ordinalIndex]){emitText("vi: NUL byte in text file\n");flush();return 1;}}
    else if(errorNumber!=2){emitText("vi: cannot read file\n");flush();return 1;}
    int dimColour=userInvoke(16,0,0,0,0,0,0);if(dimColour<0){emitText("vi: use a standalone interactive command\n");flush();return 1;}columns=dimColour&65535;rowCount=(unsigned)dimColour>>16;
    emitText("\033[2J\033[H");flush();
    int leadingPart=0,quitProgram=0;
    while(!quitProgram){drawScreen();int thirdIndex=pressedValue();if(thirdIndex==27)thirdIndex=escaped();noticeText=0;
        if(thirdIndex==1001){vertical(-1);continue;}if(thirdIndex==1002){vertical(1);continue;}if(thirdIndex==1003){indexValue=nextItem(indexValue);continue;}if(thirdIndex==1004){indexValue=previous(indexValue);continue;}
        if(thirdIndex==1005){indexValue=run(indexValue);continue;}if(thirdIndex==1006){indexValue=endOffset(indexValue);continue;}
        if(thirdIndex==1008||thirdIndex==1009){for(int ordinalIndex=0;ordinalIndex<rowCount-2;ordinalIndex++)vertical(thirdIndex==1008?-1:1);continue;}
        if(insert){
            if(thirdIndex==27||thirdIndex==3){insert=0;continue;}
            if(thirdIndex==127||thirdIndex==8){if(indexValue)clearBytes(previous(indexValue),indexValue);continue;}
            if(thirdIndex==1007){if(indexValue<lengthValue)clearBytes(indexValue,nextItem(indexValue));continue;}
            if(thirdIndex==13)thirdIndex=10;if(thirdIndex==10||thirdIndex==9||(thirdIndex>=32&&thirdIndex<256)){
                unsigned char secondValue[4];secondValue[0]=thirdIndex;int itemCount=thirdIndex<128?1:thirdIndex>=0xc2&&thirdIndex<0xe0?2:thirdIndex<0xf0?3:thirdIndex<=0xf4?4:0;
                if(!itemCount){noticeText="Invalid UTF-8";continue;}int valid=1;for(int ordinalIndex=1;ordinalIndex<itemCount;ordinalIndex++){int characterCode=pressedValue();if(characterCode<128||characterCode>191){pendingKey=characterCode;valid=0;break;}secondValue[ordinalIndex]=characterCode;}
                if(valid)appendValue(secondValue,itemCount);
            }continue;
        }
        if(leadingPart){int dataPosition=leadingPart;leadingPart=0;if(dataPosition=='g'&&thirdIndex=='g'){indexValue=0;continue;}if(dataPosition=='Z'&&thirdIndex=='Z'){quitProgram=storeValue();continue;}if((dataPosition=='d'&&thirdIndex=='d')||(dataPosition=='y'&&thirdIndex=='y')){int firstValue=run(indexValue),secondValue=endOffset(indexValue);if(secondValue<lengthValue)secondValue++;copyLength=secondValue-firstValue;for(int ordinalIndex=0;ordinalIndex<copyLength;ordinalIndex++)copiedData[ordinalIndex]=text[firstValue+ordinalIndex];if(dataPosition=='d')clearBytes(firstValue,secondValue);continue;}}
        if(thirdIndex=='i'){insert=1;continue;}if(thirdIndex=='a'){if(indexValue<endOffset(indexValue))indexValue=nextItem(indexValue);insert=1;continue;}
        if(thirdIndex=='I'){indexValue=run(indexValue);insert=1;continue;}if(thirdIndex=='A'){indexValue=endOffset(indexValue);insert=1;continue;}
        if(thirdIndex=='o'||thirdIndex=='O'){unsigned char lineEnd='\n';indexValue=thirdIndex=='o'?endOffset(indexValue):run(indexValue);if(appendValue(&lineEnd,1)){if(thirdIndex=='O')indexValue--;insert=1;}continue;}
        if(thirdIndex=='h'){indexValue=previous(indexValue);continue;}if(thirdIndex=='l'){indexValue=nextItem(indexValue);continue;}if(thirdIndex=='j'){vertical(1);continue;}if(thirdIndex=='k'){vertical(-1);continue;}
        if(thirdIndex=='0'){indexValue=run(indexValue);continue;}if(thirdIndex=='$'){indexValue=endOffset(indexValue);continue;}if(thirdIndex=='G'){indexValue=run(lengthValue);continue;}
        if(thirdIndex=='g'||thirdIndex=='d'||thirdIndex=='y'||thirdIndex=='Z'){leadingPart=thirdIndex;continue;}
        if(thirdIndex=='x'||thirdIndex==1007){if(indexValue<lengthValue)clearBytes(indexValue,nextItem(indexValue));continue;}
        if(thirdIndex=='p'&&copyLength){indexValue=endOffset(indexValue);if(indexValue<lengthValue)indexValue++;appendValue(copiedData,copyLength);continue;}
        if(thirdIndex=='u'&&haveUndo){for(int ordinalIndex=0;ordinalIndex<editorCapacity;ordinalIndex++){unsigned char secondValue=text[ordinalIndex];text[ordinalIndex]=undoData[ordinalIndex];undoData[ordinalIndex]=secondValue;}int itemCount=lengthValue;lengthValue=undoLength;undoLength=itemCount;itemCount=indexValue;indexValue=upperSide;upperSide=itemCount;itemCount=wasChanged;wasChanged=undoChanges;undoChanges=itemCount;continue;}
        if(thirdIndex==':'||thirdIndex=='/'){quitProgram=prompt(thirdIndex);continue;}if(thirdIndex=='n'){findNext();continue;}
    }
    emitText("\033[0m\033[?25h\033[2J\033[H");flush();userInvoke(16,2,0,0,0,0,0);return 0;
}
