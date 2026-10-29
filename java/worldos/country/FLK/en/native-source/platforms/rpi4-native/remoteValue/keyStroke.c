#include "remoteValue.h"
#include <string.h>
#include "twoSetKeyboardTable.h"
static unsigned controlValue,shiftKey,hangulText;
typedef struct {unsigned firstItem,middle,ending;} compositionState;
static compositionState compositionValue,logRecord[16];
static unsigned logCount;
void commitRemoteKey(void){memset(&compositionValue,0,sizeof(compositionValue));logCount=0;}
void initializeRemoteKeyStroke(void){controlValue=shiftKey=hangulText=0;commitRemoteKey();}
static void putText(unsigned value){
    unsigned char text[4];unsigned number;
    if(value<128){text[0]=value;number=1;}else if(value<2048){text[0]=0xc0|(value>>6);text[1]=0x80|(value&63);number=2;}
    else if(value<65536){text[0]=0xe0|(value>>12);text[1]=0x80|((value>>6)&63);text[2]=0x80|(value&63);number=3;}
    else{text[0]=0xf0|(value>>18);text[1]=0x80|((value>>12)&63);text[2]=0x80|((value>>6)&63);text[3]=0x80|(value&63);number=4;}
    feedRemoteInput(text,number);
}
static int findEntry(const unsigned *entryList,unsigned number,unsigned value){for(unsigned ordinalIndex=0;ordinalIndex<number;ordinalIndex++)if(entryList[ordinalIndex]==value)return ordinalIndex;return -1;}
static unsigned findDuplicate(const unsigned lookupTable[][3],unsigned number,unsigned firstOperand,unsigned secondOperand){for(unsigned ordinalIndex=0;ordinalIndex<number;ordinalIndex++)if(lookupTable[ordinalIndex][0]==firstOperand&&lookupTable[ordinalIndex][1]==secondOperand)return lookupTable[ordinalIndex][2];return 0;}
static unsigned composedText(void){
    if(compositionValue.firstItem&&compositionValue.middle)return 0xac00+(findEntry(initialJamoTable,19,compositionValue.firstItem)*21+findEntry(medialJamoTable,21,compositionValue.middle))*28+(compositionValue.ending?findEntry(finalJamoTable,28,compositionValue.ending):0);
    return compositionValue.firstItem?compositionValue.firstItem:compositionValue.middle;
}
static int feedHangul(unsigned keyStroke){
    unsigned jamoValue=0;for(unsigned ordinalIndex=0;ordinalIndex<sizeof(keyLayout)/sizeof(keyLayout[0]);ordinalIndex++)if(keyLayout[ordinalIndex][0]==keyStroke)jamoValue=keyLayout[ordinalIndex][1];
    if(!jamoValue&&keyStroke>='A'&&keyStroke<='Z')return feedHangul(keyStroke+32);if(!jamoValue)return 0;
    unsigned previousItem=composedText(),commitValue=0;compositionState beforeValue=compositionValue;
    if(logCount<16)logRecord[logCount++]=beforeValue;
    if(findEntry(initialJamoTable,19,jamoValue)>=0){
        if(compositionValue.firstItem&&compositionValue.middle&&!compositionValue.ending&&findEntry(finalJamoTable,28,jamoValue)>=0)compositionValue.ending=jamoValue;
        else{unsigned overlayValue=findDuplicate(compoundFinalJamo,11,compositionValue.ending,jamoValue);if(compositionValue.ending&&overlayValue)compositionValue.ending=overlayValue;
            else{commitValue=previousItem;commitRemoteKey();compositionValue.firstItem=jamoValue;logCount=1;memset(logRecord,0,sizeof(compositionState));}}
    }else if(compositionValue.ending){
        unsigned leftSide=0,right=compositionValue.ending;for(unsigned ordinalIndex=0;ordinalIndex<11;ordinalIndex++)if(compoundFinalJamo[ordinalIndex][2]==compositionValue.ending){leftSide=compoundFinalJamo[ordinalIndex][0];right=compoundFinalJamo[ordinalIndex][1];break;}
        compositionValue.ending=leftSide;commitValue=composedText();commitRemoteKey();compositionValue.firstItem=right;compositionValue.middle=jamoValue;logCount=2;
        memset(logRecord,0,2*sizeof(compositionState));logRecord[1].firstItem=right;
    }else if(compositionValue.middle){unsigned overlayValue=findDuplicate(compoundMedialJamo,7,compositionValue.middle,jamoValue);
        if(overlayValue)compositionValue.middle=overlayValue;else{commitValue=previousItem;commitRemoteKey();compositionValue.middle=jamoValue;logCount=1;memset(logRecord,0,sizeof(compositionState));}
    }else compositionValue.middle=jamoValue;
    if(previousItem)putText(127);if(commitValue)putText(commitValue);unsigned nowValue=composedText();if(nowValue)putText(nowValue);return 1;
}
void remoteKeyStroke(unsigned symbol,int pressValue){
    if(symbol==0xffe3||symbol==0xffe4){controlValue=pressValue;return;}
    if(symbol==0xffe1||symbol==0xffe2){shiftKey=pressValue;return;}
    if(!pressValue)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&shiftKey&&!controlValue)){
        commitRemoteKey();hangulText=!hangulText;unsigned char event[]={30,3,hangulText,0,0,0,0};feedRemoteInput(event,7);return;
    }
    if(symbol==0xff08&&hangulText&&!controlValue&&logCount){compositionValue=logRecord[--logCount];putText(127);unsigned text=composedText();if(text)putText(text);return;}
    if(hangulText&&!controlValue&&symbol<128&&feedHangul(symbol))return;
    commitRemoteKey();
    if((controlValue&&shiftKey&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char event[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};feedRemoteInput(event,7);return;}
    const char *specialValue=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(specialValue){feedRemoteInput((const unsigned char*)specialValue,strlen(specialValue));return;}
    unsigned value=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(value>0x10ffff||(value>=0xd800&&value<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(controlValue){if(value>='a'&&value<='z')value-=96;else if(value>='A'&&value<='Z')value-=64;}
    putText(value);
}
