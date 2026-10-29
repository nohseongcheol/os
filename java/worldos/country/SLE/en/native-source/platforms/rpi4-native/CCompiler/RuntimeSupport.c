#include "../naming/machineLinkNames.h"
/* Freestanding compiler support. All file I/O goes through the native SVC ABI. */
#include "invoke.h"
#include "stdio.h"
#include <stdarg.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "resources.h"
static int error;
int *__errno_location(void){return &error;}
void exit(int stateValue){userInvoke(6,stateValue,0,0,0,0,0);for(;;){}}
void __assert_fail(const char *checkExpression,const char *file,unsigned line,const char *methodEntryName){fprintf(stderr,"cc assertion: %s %s:%u %s\n",checkExpression,file,line,methodEntryName);exit(1);}
size_t strlen(const char*stringData){const char*dataPosition=stringData;while(*dataPosition)dataPosition++;return dataPosition-stringData;}
int strcmp(const char*firstValue,const char*secondValue){while(*firstValue&&*firstValue==*secondValue){firstValue++;secondValue++;}return (unsigned char)*firstValue-(unsigned char)*secondValue;}
int strncmp(const char*firstValue,const char*secondValue,size_t itemCount){while(itemCount--){unsigned char xCoordinate=*firstValue++,yCoordinate=*secondValue++;if(xCoordinate!=yCoordinate)return xCoordinate-yCoordinate;if(!xCoordinate)return 0;}return 0;}
char *strcpy(char*destinationData,const char*stringData){char*returnedValue=destinationData;while((*destinationData++=*stringData++)){}return returnedValue;}
char *strchr(const char*stringData,int characterCode){do{if(*stringData==(char)characterCode)return (char*)stringData;}while(*stringData++);return 0;}
char *strrchr(const char*stringData,int characterCode){const char*returnedValue=0;do{if(*stringData==(char)characterCode)returnedValue=stringData;}while(*stringData++);return (char*)returnedValue;}
char *strstr(const char*stringData,const char*terminalEntry){size_t itemCount=strlen(terminalEntry);for(;*stringData;stringData++)if(!strncmp(stringData,terminalEntry,itemCount))return (char*)stringData;return itemCount?0:(char*)stringData;}
int memcmp(const void*firstValue,const void*secondValue,size_t itemCount){const unsigned char*xCoordinate=firstValue,*yCoordinate=secondValue;while(itemCount--){if(*xCoordinate!=*yCoordinate)return *xCoordinate-*yCoordinate;xCoordinate++;yCoordinate++;}return 0;}
void *memmove(void*destinationData,const void*stringData,size_t itemCount){unsigned char*xCoordinate=destinationData;const unsigned char*yCoordinate=stringData;if(xCoordinate<yCoordinate){for(size_t ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)xCoordinate[ordinalIndex]=yCoordinate[ordinalIndex];}else while(itemCount){itemCount--;xCoordinate[itemCount]=yCoordinate[itemCount];}return destinationData;}
static unsigned char allocationArena[6*1024*1024] __attribute__((aligned(16)));
typedef struct dataBlock {size_t size;struct dataBlock*nextItem;int remainingCapacity;int padding;uint64_t alignmentUnit;} dataBlock;
static dataBlock *firstEntry;
void free(void*dataPosition){if(!dataPosition)return;dataBlock*secondValue=(dataBlock*)dataPosition-1;secondValue->remainingCapacity=1;for(dataBlock*nextOffset=firstEntry;nextOffset&&nextOffset->nextItem;){if(nextOffset->remainingCapacity&&nextOffset->nextItem->remainingCapacity){nextOffset->size+=sizeof(dataBlock)+nextOffset->nextItem->size;nextOffset->nextItem=nextOffset->nextItem->nextItem;}else nextOffset=nextOffset->nextItem;}}
void *realloc(void*dataPosition,size_t itemCount){
    if(!itemCount){free(dataPosition);return 0;}if(itemCount>sizeof(allocationArena)-sizeof(dataBlock))return 0;itemCount=(itemCount+15)&~(size_t)15;
    if(!firstEntry){firstEntry=(dataBlock*)allocationArena;firstEntry->size=sizeof(allocationArena)-sizeof(dataBlock);firstEntry->remainingCapacity=1;firstEntry->nextItem=0;}
    dataBlock*previousItem=dataPosition?(dataBlock*)dataPosition-1:0;if(previousItem&&previousItem->size>=itemCount)return dataPosition;
    for(dataBlock*secondValue=firstEntry;secondValue;secondValue=secondValue->nextItem)if(secondValue->remainingCapacity&&secondValue->size>=itemCount){
        if(secondValue->size>=itemCount+sizeof(dataBlock)+16){dataBlock*remainingPart=(dataBlock*)((unsigned char*)(secondValue+1)+itemCount);remainingPart->size=secondValue->size-itemCount-sizeof(dataBlock);remainingPart->nextItem=secondValue->nextItem;remainingPart->remainingCapacity=1;secondValue->nextItem=remainingPart;secondValue->size=itemCount;}
        secondValue->remainingCapacity=0;void*returnedValue=secondValue+1;if(previousItem){memcpy(returnedValue,dataPosition,previousItem->size);free(dataPosition);}return returnedValue;
    }error=12;return 0;
}
void *malloc(size_t itemCount){return realloc(0,itemCount);}
void *calloc(size_t itemCount,size_t stringData){if(stringData&&itemCount>SIZE_MAX/stringData)return 0;void*dataPosition=malloc(itemCount*stringData);if(dataPosition)memset(dataPosition,0,itemCount*stringData);return dataPosition;}
unsigned long long strtoull(const char*stringData,char**endOffset,int backgroundValue){
    const char*startOffset=stringData;while(*stringData==' '||(*stringData>=9&&*stringData<=13))stringData++;int isNegative=0;if(*stringData=='-'||*stringData=='+')isNegative=*stringData++=='-';
    if((!backgroundValue||backgroundValue==16)&&stringData[0]=='0'&&(stringData[1]=='x'||stringData[1]=='X')){backgroundValue=16;stringData+=2;}if(!backgroundValue)backgroundValue=*stringData=='0'?8:10;
    unsigned long long temporaryData=0;int anyValue=0;for(;;){unsigned characterCode=*stringData,destinationData=characterCode>='0'&&characterCode<='9'?characterCode-'0':characterCode>='a'&&characterCode<='z'?characterCode-'a'+10:characterCode>='A'&&characterCode<='Z'?characterCode-'A'+10:99;if(destinationData>=(unsigned)backgroundValue)break;anyValue=1;stringData++;if(temporaryData>(~0ull-destinationData)/(unsigned)backgroundValue){temporaryData=~0ull;error=34;}else temporaryData=temporaryData*backgroundValue+destinationData;}
    if(endOffset)*endOffset=(char*)(anyValue?stringData:startOffset);return isNegative?0-temporaryData:temporaryData;
}
unsigned long strtoul(const char*stringData,char**auxiliaryEntry,int secondValue){return strtoull(stringData,auxiliaryEntry,secondValue);}
long strtol(const char*stringData,char**auxiliaryEntry,int secondValue){return (long)strtoull(stringData,auxiliaryEntry,secondValue);}
int atoi(const char*stringData){return (int)strtol(stringData,0,10);}
long double ldexpl(long double xCoordinate,int itemCount){while(itemCount>0){xCoordinate*=2;itemCount--;}while(itemCount<0){xCoordinate/=2;itemCount++;}return xCoordinate;}
long double strtold(const char*stringData,char**endOffset){
    const char*startOffset=stringData;while(*stringData==' '||(*stringData>=9&&*stringData<=13))stringData++;int isNegative=0;if(*stringData=='-'||*stringData=='+')isNegative=*stringData++=='-';
    int backgroundValue=10;if(stringData[0]=='0'&&(stringData[1]=='x'||stringData[1]=='X')){backgroundValue=16;stringData+=2;}long double temporaryData=0,scale=1;int fractional=0,anyValue=0;
    for(;;){int characterCode=*stringData,destinationData=characterCode>='0'&&characterCode<='9'?characterCode-'0':characterCode>='a'&&characterCode<='f'?characterCode-'a'+10:characterCode>='A'&&characterCode<='F'?characterCode-'A'+10:99;
        if(characterCode=='.'&&!fractional){fractional=1;stringData++;continue;}if(destinationData>=backgroundValue)break;anyValue=1;stringData++;temporaryData=temporaryData*backgroundValue+destinationData;if(fractional)scale*=backgroundValue;
    }temporaryData/=scale;
    if((backgroundValue==10&&(*stringData=='e'||*stringData=='E'))||(backgroundValue==16&&(*stringData=='p'||*stringData=='P'))){const char*showValue=stringData++;int subtractValues=0;if(*stringData=='-'||*stringData=='+')subtractValues=*stringData++=='-';int itemCount=0,entryCount=0;while(*stringData>='0'&&*stringData<='9'){entryCount++;if(itemCount<20000)itemCount=itemCount*10+*stringData-'0';stringData++;}if(!entryCount)stringData=showValue;else{long double factor=backgroundValue==16?2:10;while(itemCount-->0&&itemCount<200000)temporaryData=subtractValues?temporaryData/factor:temporaryData*factor;}}
    if(endOffset)*endOffset=(char*)(anyValue?stringData:startOffset);return isNegative?-temporaryData:temporaryData;
}
double strtod(const char*stringData,char**auxiliaryEntry){return (double)strtold(stringData,auxiliaryEntry);}float strtof(const char*stringData,char**auxiliaryEntry){return (float)strtold(stringData,auxiliaryEntry);}
void qsort(void*backgroundValue,size_t itemCount,size_t size,int(*compare)(const void*,const void*)){
    unsigned char*dataPosition=backgroundValue;for(size_t ordinalIndex=1;ordinalIndex<itemCount;ordinalIndex++)for(size_t innerOrdinal=ordinalIndex;innerOrdinal&&compare(dataPosition+(innerOrdinal-1)*size,dataPosition+innerOrdinal*size)>0;innerOrdinal--)for(size_t thirdIndex=0;thirdIndex<size;thirdIndex++){unsigned char characterCode=dataPosition[(innerOrdinal-1)*size+thirdIndex];dataPosition[(innerOrdinal-1)*size+thirdIndex]=dataPosition[innerOrdinal*size+thirdIndex];dataPosition[innerOrdinal*size+thirdIndex]=characterCode;}
}
static struct {int usedCapacity,lookupIndex;size_t position;} opened[24];
static unsigned char output[32768];static size_t outputSize,outputPosition;static int outputOpen;
const unsigned char *cOutput(size_t *itemCount){*itemCount=outputSize;return output;}
int open(const char*name,int configurationBits,...){
    if(!strcmp(name,"/@cc-output")){if(outputOpen){error=16;return -1;}outputOpen=1;outputSize=outputPosition=0;return 100;}
    for(unsigned ordinalIndex=0;ordinalIndex<sizeof(compilerResources)/sizeof(compilerResources[0]);ordinalIndex++)if(!strcmp(name,compilerResources[ordinalIndex].name)){
        if(configurationBits&3){error=30;return -1;}for(int innerOrdinal=0;innerOrdinal<24;innerOrdinal++)if(!opened[innerOrdinal].usedCapacity){opened[innerOrdinal].usedCapacity=1;opened[innerOrdinal].lookupIndex=ordinalIndex;opened[innerOrdinal].position=0;return 128+innerOrdinal;}error=24;return -1;
    }
    intptr_t returnedValue=userInvoke(3,(uintptr_t)name,configurationBits,0,0,0,0);if(returnedValue<0){error=-returnedValue;return -1;}return returnedValue;
}
int close(int fileHandle){if(fileHandle==100){outputOpen=0;return 0;}if(fileHandle>=128&&fileHandle<152){opened[fileHandle-128].usedCapacity=0;return 0;}intptr_t returnedValue=userInvoke(4,fileHandle,0,0,0,0,0);if(returnedValue<0){error=-returnedValue;return -1;}return 0;}
long read(int fileHandle,void*data,size_t itemCount){
    if(fileHandle>=128&&fileHandle<152&&opened[fileHandle-128].usedCapacity){int ordinalIndex=fileHandle-128;const compilerResource*returnedValue=&compilerResources[opened[ordinalIndex].lookupIndex];size_t leftSide=returnedValue->size-opened[ordinalIndex].position;if(itemCount>leftSide)itemCount=leftSide;memcpy(data,returnedValue->data+opened[ordinalIndex].position,itemCount);opened[ordinalIndex].position+=itemCount;return itemCount;}
    intptr_t returnedValue=userInvoke(2,fileHandle,(uintptr_t)data,itemCount,0,0,0);if(returnedValue<0){error=-returnedValue;return -1;}return returnedValue;
}
long write(int fileHandle,const void*data,size_t itemCount){
    if(fileHandle==100){if(itemCount>sizeof(output)-outputPosition){error=28;return -1;}memcpy(output+outputPosition,data,itemCount);outputPosition+=itemCount;if(outputSize<outputPosition)outputSize=outputPosition;return itemCount;}
    intptr_t returnedValue=userInvoke(1,fileHandle,(uintptr_t)data,itemCount,0,0,0);if(returnedValue<0){error=-returnedValue;return -1;}return returnedValue;
}
long lseek(int fileHandle,long offsetValue,int seekOrigin){
    if(fileHandle==100){long dataPosition=offsetValue+(seekOrigin==0?0:seekOrigin==1?outputPosition:outputSize);if(dataPosition<0||(size_t)dataPosition>sizeof(output)){error=22;return -1;}outputPosition=dataPosition;return dataPosition;}
    if(fileHandle>=128&&fileHandle<152&&opened[fileHandle-128].usedCapacity){int ordinalIndex=fileHandle-128;long dataPosition=offsetValue+(seekOrigin==0?0:seekOrigin==1?opened[ordinalIndex].position:compilerResources[opened[ordinalIndex].lookupIndex].size);if(dataPosition<0||(size_t)dataPosition>compilerResources[opened[ordinalIndex].lookupIndex].size){error=22;return -1;}opened[ordinalIndex].position=dataPosition;return dataPosition;}
    intptr_t returnedValue=userInvoke(5,fileHandle,offsetValue,seekOrigin,0,0,0);if(returnedValue<0){error=-returnedValue;return -1;}return returnedValue;
}
int unlink(const char*name){intptr_t returnedValue=userInvoke(11,(uintptr_t)name,0,0,0,0,0);if(returnedValue<0){error=-returnedValue;return -1;}return returnedValue;}
char *realpath(const char*name,char*resultData){if(!resultData){resultData=malloc(strlen(name)+1);if(!resultData)return 0;}return strcpy(resultData,name);}
char *getcwd(char*dataPosition,size_t itemCount){if(itemCount<2){error=34;return 0;}dataPosition[0]='/';dataPosition[1]=0;return dataPosition;}
char *strerror(int auxiliaryEntry){(void)auxiliaryEntry;return "native compiler I/O error";}
time_t time(time_t*terminalEntry){time_t temporaryData=0;if(terminalEntry)*terminalEntry=temporaryData;return temporaryData;}
struct tm *localtime(const time_t*terminalEntry){(void)terminalEntry;static struct tm temporaryData={.tm_year=126,.tm_mon=0,.tm_mday=1};return &temporaryData;}
static FILE streams[18]={{1,0,1},{2,0,1}};FILE*stdout=&streams[0],*stderr=&streams[1];
FILE*fdopen(int fileHandle,const char*methodMode){(void)methodMode;for(unsigned ordinalIndex=2;ordinalIndex<18;ordinalIndex++)if(!streams[ordinalIndex].usedCapacity){streams[ordinalIndex].usedCapacity=1;streams[ordinalIndex].error=0;streams[ordinalIndex].fileHandle=fileHandle;return &streams[ordinalIndex];}error=24;return 0;}
int fflush(FILE*fileEntry){return fileEntry&&fileEntry->error?-1:0;}
int fclose(FILE*fileEntry){int returnedValue=close(fileEntry->fileHandle);if(fileEntry->error)returnedValue=-1;fileEntry->usedCapacity=0;return returnedValue;}
size_t fwrite(const void*dataPosition,size_t stringData,size_t itemCount,FILE*fileEntry){if(!stringData)return 0;if(itemCount>SIZE_MAX/stringData){fileEntry->error=1;return 0;}long returnedValue=write(fileEntry->fileHandle,dataPosition,stringData*itemCount);if(returnedValue<0){fileEntry->error=1;return 0;}return (size_t)returnedValue/stringData;}
int fputc(int characterCode,FILE*fileEntry){unsigned char secondValue=characterCode;return fwrite(&secondValue,1,1,fileEntry)==1?secondValue:EOF;}
int fputs(const char*stringData,FILE*fileEntry){return fwrite(stringData,1,strlen(stringData),fileEntry)==strlen(stringData)?0:EOF;}
static void putValue(char*resultData,size_t capacityMaximum,size_t*currentPosition,char characterCode){if(*currentPosition+1<capacityMaximum)resultData[*currentPosition]=characterCode;(*currentPosition)++;}
int vsnprintf(char*resultData,size_t capacityMaximum,const char*format,va_list variadicArguments){
    size_t currentPosition=0;while(*format){if(*format!='%'){putValue(resultData,capacityMaximum,&currentPosition,*format++);continue;}format++;
        int leftSide=0,zeroValue=0,fallbackValue=0;while(*format=='-'||*format=='0'||*format=='#'||*format=='+'||*format==' '){if(*format=='-')leftSide=1;if(*format=='0')zeroValue=1;if(*format=='#')fallbackValue=1;format++;}
        int widthValue=0,precisionValue=-1;if(*format=='*'){widthValue=va_arg(variadicArguments,int);format++;}else while(*format>='0'&&*format<='9')widthValue=widthValue*10+*format++-'0';
        if(*format=='.'){format++;precisionValue=0;if(*format=='*'){precisionValue=va_arg(variadicArguments,int);format++;}else while(*format>='0'&&*format<='9')precisionValue=precisionValue*10+*format++-'0';}
        int wideCharacter=0;while(*format=='l'||*format=='z'||*format=='t'||*format=='j'||*format=='h'){if(*format!='h')wideCharacter=1;format++;}
        char typeCategory=*format?*format++:0,bufferStorage[80];const char*stringData=bufferStorage;size_t itemCount=0;
        if(typeCategory=='s'){stringData=va_arg(variadicArguments,const char*);if(!stringData)stringData="(null)";itemCount=strlen(stringData);if(precisionValue>=0&&itemCount>(size_t)precisionValue)itemCount=precisionValue;}
        else if(typeCategory=='c'){bufferStorage[0]=va_arg(variadicArguments,int);itemCount=1;}
        else if(typeCategory=='%'){bufferStorage[0]='%';itemCount=1;}
        else if(typeCategory=='d'||typeCategory=='i'||typeCategory=='u'||typeCategory=='x'||typeCategory=='X'||typeCategory=='o'||typeCategory=='p'){
            unsigned long long value;int negative=0;
            if(typeCategory=='d'||typeCategory=='i'){long long temporaryData=wideCharacter?va_arg(variadicArguments,long long):va_arg(variadicArguments,int);negative=temporaryData<0;value=negative?0-(unsigned long long)temporaryData:temporaryData;}
            else value=typeCategory=='p'?(uintptr_t)va_arg(variadicArguments,void*):wideCharacter?va_arg(variadicArguments,unsigned long long):va_arg(variadicArguments,unsigned);
            unsigned backgroundValue=typeCategory=='x'||typeCategory=='X'||typeCategory=='p'?16:typeCategory=='o'?8:10;char digitCount[64];unsigned usedCapacity=0;
            do{digitCount[usedCapacity++]="0123456789abcdef"[value%backgroundValue];value/=backgroundValue;}while(value);
            if(negative)bufferStorage[itemCount++]='-';if(typeCategory=='p'||(fallbackValue&&backgroundValue==16)){bufferStorage[itemCount++]='0';bufferStorage[itemCount++]='x';}
            for(int fillValue=(int)usedCapacity;precisionValue>fillValue&&itemCount<sizeof(bufferStorage)-usedCapacity;fillValue++)bufferStorage[itemCount++]='0';
            if(zeroValue&&!leftSide&&precisionValue<0)while(widthValue>(int)(itemCount+usedCapacity)&&itemCount<sizeof(bufferStorage)-usedCapacity)bufferStorage[itemCount++]='0';
            while(usedCapacity)bufferStorage[itemCount++]=digitCount[--usedCapacity];
        }else{bufferStorage[0]='?';itemCount=1;}
        if(widthValue>4096)widthValue=4096;while(!leftSide&&widthValue>(int)itemCount){putValue(resultData,capacityMaximum,&currentPosition,' ');widthValue--;}
        for(size_t ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)putValue(resultData,capacityMaximum,&currentPosition,stringData[ordinalIndex]);while(leftSide&&widthValue>(int)itemCount){putValue(resultData,capacityMaximum,&currentPosition,' ');widthValue--;}
    }if(capacityMaximum)resultData[currentPosition<capacityMaximum?currentPosition:capacityMaximum-1]=0;return currentPosition;
}
int snprintf(char*resultData,size_t capacityMaximum,const char*fileEntry,...){va_list firstValue;va_start(firstValue,fileEntry);int returnedValue=vsnprintf(resultData,capacityMaximum,fileEntry,firstValue);va_end(firstValue);return returnedValue;}
int sprintf(char*resultData,const char*fileEntry,...){va_list firstValue;va_start(firstValue,fileEntry);int returnedValue=vsnprintf(resultData,SIZE_MAX,fileEntry,firstValue);va_end(firstValue);return returnedValue;}
int vfprintf(FILE*streamValue,const char*fileEntry,va_list firstValue){char secondValue[2048];int itemCount=vsnprintf(secondValue,sizeof(secondValue),fileEntry,firstValue);if(itemCount>2047)itemCount=2047;return fwrite(secondValue,1,itemCount,streamValue)==(size_t)itemCount?itemCount:-1;}
int fprintf(FILE*streamValue,const char*fileEntry,...){va_list firstValue;va_start(firstValue,fileEntry);int returnedValue=vfprintf(streamValue,fileEntry,firstValue);va_end(firstValue);return returnedValue;}
int printf(const char*fileEntry,...){va_list firstValue;va_start(firstValue,fileEntry);int returnedValue=vfprintf(stdout,fileEntry,firstValue);va_end(firstValue);return returnedValue;}
