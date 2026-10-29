/* kernelValue 전용 할당기와 passwordValue 난수 공급. User ELF의 libc와 별개이다. */
#include "cryptographySupport.h"
#include "../naming/machineLinkNames.h"
#include <string.h>
#include <bearssl_hash.h>
extern uintptr_t boardMillis(void);
typedef struct memoryBlock { size_t lengthValue; struct memoryBlock *nextItem; int useValue; } memoryBlock;
static unsigned char memoryArena[2*1024*1024] __attribute__((aligned(16)));
static memoryBlock *firstFragmentValue;
void *allocateRemote(size_t lengthValue) {
    if (!lengthValue || lengthValue>sizeof(memoryArena)-64) return 0;
    lengthValue=(lengthValue+15)&~(size_t)15;
    if(!firstFragmentValue){firstFragmentValue=(void*)memoryArena;firstFragmentValue->lengthValue=sizeof(memoryArena)-32;}
    for(memoryBlock *fragmentValue=firstFragmentValue;fragmentValue;fragmentValue=fragmentValue->nextItem)if(!fragmentValue->useValue&&fragmentValue->lengthValue>=lengthValue){
        if(fragmentValue->lengthValue>=lengthValue+64){memoryBlock *newFragment=(void*)((char*)fragmentValue+32+lengthValue);
            newFragment->lengthValue=fragmentValue->lengthValue-lengthValue-32;newFragment->nextItem=fragmentValue->nextItem;newFragment->useValue=0;fragmentValue->nextItem=newFragment;fragmentValue->lengthValue=lengthValue;}
        fragmentValue->useValue=1;return(char*)fragmentValue+32;
    }return 0;
}
void releaseRemote(void *address) {
    if(!address)return;memoryBlock *fragmentValue=(void*)((char*)address-32);
    volatile unsigned char *erasedValue=address;for(size_t ordinalIndex=0;ordinalIndex<fragmentValue->lengthValue;ordinalIndex++)erasedValue[ordinalIndex]=0;
    fragmentValue->useValue=0;
    for(fragmentValue=firstFragmentValue;fragmentValue&&fragmentValue->nextItem;){if(!fragmentValue->useValue&&!fragmentValue->nextItem->useValue){fragmentValue->lengthValue+=32+fragmentValue->nextItem->lengthValue;fragmentValue->nextItem=fragmentValue->nextItem->nextItem;}else fragmentValue=fragmentValue->nextItem;}
}
void *reallocateRemote(void *address,size_t lengthValue){
    if(!address)return allocateRemote(lengthValue);if(!lengthValue){releaseRemote(address);return 0;}
    memoryBlock *fragmentValue=(void*)((char*)address-32);void *newAddress=allocateRemote(lengthValue);
    if(newAddress){memcpy(newAddress,address,lengthValue<fragmentValue->lengthValue?lengthValue:fragmentValue->lengthValue);releaseRemote(address);}return newAddress;
}
int strcmp(const char *firstOperand,const char *secondOperand){while(*firstOperand&&*firstOperand==*secondOperand){firstOperand++;secondOperand++;}return(unsigned char)*firstOperand-(unsigned char)*secondOperand;}
char *strchr(const char *wordText,int characterValue){for(;;wordText++){if(*wordText==(char)characterValue)return(char*)wordText;if(!*wordText)return 0;}}
char *strstr(const char *wordText,const char *foundValue){size_t lengthValue=strlen(foundValue);for(;*wordText;wordText++)if(!strncmp(wordText,foundValue,lengthValue))return(char*)wordText;return lengthValue?0:(char*)wordText;}
char *strncpy(char *destinationValue,const char *original,size_t lengthValue){size_t ordinalIndex=0;for(;ordinalIndex<lengthValue&&original[ordinalIndex];ordinalIndex++)destinationValue[ordinalIndex]=original[ordinalIndex];for(;ordinalIndex<lengthValue;ordinalIndex++)destinationValue[ordinalIndex]=0;return destinationValue;}
char *strncat(char *destinationValue,const char *original,size_t lengthValue){char *ending=destinationValue+strlen(destinationValue);while(lengthValue--&&*original)*ending++=*original++;*ending=0;return destinationValue;}
int strncasecmp(const char *firstOperand,const char *secondOperand,size_t lengthValue){while(lengthValue--){unsigned firstCharacter=*firstOperand++,secondCharacter=*secondOperand++;if(firstCharacter>='A'&&firstCharacter<='Z')firstCharacter+=32;if(secondCharacter>='A'&&secondCharacter<='Z')secondCharacter+=32;if(firstCharacter!=secondCharacter)return(int)firstCharacter-(int)secondCharacter;if(!firstCharacter)break;}return 0;}
int strcasecmp(const char *firstOperand,const char *secondOperand){return strncasecmp(firstOperand,secondOperand,(size_t)-1);}
char *strtok_r(char *wordText,const char *delimiterValue,char **nextItem){if(!wordText)wordText=*nextItem;while(*wordText&&strchr(delimiterValue,*wordText))wordText++;if(!*wordText){*nextItem=wordText;return 0;}char *initialItem=wordText;while(*wordText&&!strchr(delimiterValue,*wordText))wordText++;if(*wordText)*wordText++=0;*nextItem=wordText;return initialItem;}
unsigned long strtoul(const char *wordText, char **ending, int baseValue) {
    const char *source=wordText;unsigned long value=0;int negativeValue=0,overflowValue=0;
    while(*wordText==' '||(*wordText>=9&&*wordText<=13))wordText++;
    if(*wordText=='-'||*wordText=='+')negativeValue=*wordText++=='-';
    if((baseValue==0||baseValue==16)&&wordText[0]=='0'&&(wordText[1]=='x'||wordText[1]=='X')&&
       ((wordText[2]>='0'&&wordText[2]<='9')||(wordText[2]>='a'&&wordText[2]<='f')||(wordText[2]>='A'&&wordText[2]<='F'))) {baseValue=16;wordText+=2;}
    if(!baseValue)baseValue=*wordText=='0'?8:10;
    if(baseValue<2||baseValue>36){if(ending)*ending=(char*)source;return 0;}
    const char *initialItem=wordText;
    for(;;wordText++) {
        unsigned characterValue=(unsigned char)*wordText;
        unsigned number=characterValue>='0'&&characterValue<='9'?characterValue-'0':characterValue>='a'&&characterValue<='z'?characterValue-'a'+10:characterValue>='A'&&characterValue<='Z'?characterValue-'A'+10:36;
        if(number>=(unsigned)baseValue)break;
        if(value>(~0ul-number)/(unsigned)baseValue)overflowValue=1;
        if(!overflowValue)value=value*(unsigned)baseValue+number;
    }
    if(ending)*ending=(char*)(wordText==initialItem?source:wordText);
    return overflowValue?~0ul:negativeValue?0ul-value:value;
}

/* RNG200: BCM2711 peripheral map, health errors cause fail-closed.
 * QEMU has no RNG200: the launcher supplies a fresh host CSPRNG seed at
 * reserved physical 0x01ff0000, outside both kernel BSS and EL0 arenas.
 * SHA256 key evolution supplies independent DRBG seeds; never a clock seed. */
static unsigned char mockSeed[32];
static int seedState;
void remoteSummary(const void *data, size_t lengthValue, unsigned char result[32]) {
    br_sha256_context contextValue;
    br_sha256_init(&contextValue); br_sha256_update(&contextValue, data, lengthValue); br_sha256_out(&contextValue, result);
    memset(&contextValue, 0, sizeof(contextValue));
}
#define randomRegisters(position) (*(volatile uint32_t*)(uintptr_t)(0xfe104000ul+(position)))
int remoteRandom(unsigned char *destinationValue,unsigned lengthValue){
    if(!seedState){volatile unsigned char *data=(void*)0x01ff0000ul;const char *markerValue="JKRENRG1";unsigned differenceValue=0;
        for(unsigned ordinalIndex=0;ordinalIndex<8;ordinalIndex++)differenceValue|=data[ordinalIndex]^(unsigned char)markerValue[ordinalIndex];
        if(!differenceValue){for(unsigned ordinalIndex=0;ordinalIndex<32;ordinalIndex++)mockSeed[ordinalIndex]=data[8+ordinalIndex];for(unsigned ordinalIndex=0;ordinalIndex<40;ordinalIndex++)data[ordinalIndex]=0;seedState=2;}
        else {seedState=1;randomRegisters(0)=(randomRegisters(0)&~0x1fffu)|1;}
    }
    if(seedState==2){while(lengthValue){unsigned char nextItem[32],inputValue[33];memcpy(inputValue,mockSeed,32);inputValue[32]=0;remoteSummary(inputValue,33,nextItem);
        inputValue[32]=1;remoteSummary(inputValue,33,mockSeed);memset(inputValue,0,33);
        unsigned number=lengthValue<32?lengthValue:32;memcpy(destinationValue,nextItem,number);memset(nextItem,0,32);destinationValue+=number;lengthValue-=number;}return 0;}
    uintptr_t limitValue=boardMillis()+1000;
    while(lengthValue){if((randomRegisters(0x18)&0x80000020u)||boardMillis()>limitValue)return -1;
        if(!(randomRegisters(0x24)&255))continue;uint32_t value=randomRegisters(0x20);
        for(unsigned ordinalIndex=0;ordinalIndex<4&&lengthValue;ordinalIndex++,lengthValue--){*destinationValue++=value&255;value>>=8;}}
    return 0;
}
