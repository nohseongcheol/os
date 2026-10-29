#include "../naming/machineLinkNames.h"
/* Read-only ZIP/JAR class path in EL0; no host extraction or code execution. */
#include "invoke.h"
#include "Bundle.h"
#include "uzlib.h"
static unsigned char archive[16384], unpacked[16385];
static unsigned size, central, entriesList;
static char entryClass[256];
static unsigned readTwoBytes(unsigned currentPosition) { return archive[currentPosition] | archive[currentPosition+1] << 8; }
static uint32_t readFourBytes(unsigned currentPosition) { return readTwoBytes(currentPosition) | (uint32_t)readTwoBytes(currentPosition+2) << 16; }
static int clip(unsigned currentPosition, unsigned itemCount, unsigned capacityLimit) { return currentPosition <= capacityLimit && itemCount <= capacityLimit-currentPosition; }
static size_t lengthValue(const char *stringData) { size_t itemCount=0; while(stringData[itemCount]) itemCount++; return itemCount; }
static int equalText(const unsigned char *firstValue, const unsigned char *secondValue, unsigned itemCount) { for(unsigned ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)if(firstValue[ordinalIndex]!=secondValue[ordinalIndex])return 0;return 1; }
static int fileEnd(void *unused) { (void)unused; return -1; }
static int attributeData(const char *line,unsigned usedCapacity,int *entryPointExists) {
    if(usedCapacity>=12 && equalText((const unsigned char*)line,(const unsigned char*)"Class-Path: ",12))return -95;
    if(usedCapacity>=12 && equalText((const unsigned char*)line,(const unsigned char*)"Main-Class: ",12)) {
        unsigned value=usedCapacity-12;if(*entryPointExists||!value||value>=sizeof(entryClass))return -8;
        for(unsigned ordinalIndex=0;ordinalIndex<value;ordinalIndex++){unsigned char characterCode=line[12+ordinalIndex];if(characterCode<=32||characterCode=='/'||characterCode=='\\')return -8;entryClass[ordinalIndex]=characterCode;}
        entryClass[value]=0;*entryPointExists=1;
    }
    return 0;
}
static int member(unsigned currentPosition, unsigned char *resultData, unsigned capacityMaximum) {
    unsigned methodEntry=readTwoBytes(currentPosition+10), configurationBits=readTwoBytes(currentPosition+8), compressed=readFourBytes(currentPosition+20), releaseSize=readFourBytes(currentPosition+24), local=readFourBytes(currentPosition+42);
    unsigned name=readTwoBytes(currentPosition+28);
    if(releaseSize>capacityMaximum || releaseSize>16384 || (methodEntry!=0 && methodEntry!=8) || (configurationBits&~0x80e))return -8;
    if(!clip(local,30,central) || readFourBytes(local)!=0x04034b50 || readTwoBytes(local+8)!=methodEntry || readTwoBytes(local+6)!=configurationBits || readTwoBytes(local+26)!=name)return -8;
    unsigned startOffset=local+30, additionalRegion=readTwoBytes(local+28);
    if(!clip(startOffset,name,central) || !equalText(archive+startOffset,archive+currentPosition+46,name))return -8;
    startOffset+=name;if(!clip(startOffset,additionalRegion,central))return -8;startOffset+=additionalRegion;
    if(!clip(startOffset,compressed,central))return -8;
    if(!(configurationBits&8) && (readFourBytes(local+14)!=readFourBytes(currentPosition+16) || readFourBytes(local+18)!=compressed || readFourBytes(local+22)!=releaseSize))return -8;
    if(methodEntry==0) { if(compressed!=releaseSize)return -8; for(unsigned ordinalIndex=0;ordinalIndex<releaseSize;ordinalIndex++)resultData[ordinalIndex]=archive[startOffset+ordinalIndex]; }
    else {
        uzlib_uncomp_t destinationData={0};uzlib_uncompress_init(&destinationData,0,0);
        destinationData.source=archive+startOffset;destinationData.source_limit=destinationData.source+compressed;destinationData.source_read_cb=fileEnd;
        /* One extra output byte lets inflate consume/check the end marker. */
        destinationData.dest_start=destinationData.dest=unpacked;destinationData.dest_limit=unpacked+releaseSize+1;
        int returnedValue=uzlib_uncompress(&destinationData);
        if(returnedValue!=UZLIB_DONE || destinationData.eof || destinationData.dest!=unpacked+releaseSize || destinationData.source!=destinationData.source_limit)return -8;
        for(unsigned ordinalIndex=0;ordinalIndex<releaseSize;ordinalIndex++)resultData[ordinalIndex]=unpacked[ordinalIndex];
    }
    if((uzlib_crc32(resultData,releaseSize,0xffffffffu)^0xffffffffu)!=readFourBytes(currentPosition+16))return -8;
    return releaseSize;
}
int jarRead(const char *name, unsigned char *resultData, unsigned bufferCapacity) {
    if(!entriesList)return -2;unsigned itemCount=lengthValue(name),currentPosition=central;
    for(unsigned ordinalIndex=0;ordinalIndex<entriesList;ordinalIndex++) {
        unsigned namelen=readTwoBytes(currentPosition+28);
        if(namelen==itemCount && equalText(archive+currentPosition+46,(const unsigned char*)name,itemCount))return member(currentPosition,resultData,bufferCapacity);
        currentPosition+=46+namelen+readTwoBytes(currentPosition+30)+readTwoBytes(currentPosition+32);
    }
    return -2;
}
const char *jarMain(void) { return entryClass; }
int jarOpen(const char *fileEntryName) {
    entriesList=0;entryClass[0]=0;
    intptr_t fileHandle=userInvoke(3,(uintptr_t)fileEntryName,0,0,0,0,0);if(fileHandle<0)return fileHandle;
    intptr_t itemCount=userInvoke(9,fileHandle,0,0,0,0,0);
    if(itemCount<22 || itemCount>(intptr_t)sizeof(archive)) { userInvoke(4,fileHandle,0,0,0,0,0);return -8; }
    intptr_t receivedCount=userInvoke(2,fileHandle,(uintptr_t)archive,itemCount,0,0,0);userInvoke(4,fileHandle,0,0,0,0,0);
    if(receivedCount!=itemCount)return -5;size=itemCount;
    unsigned endOffset=size-22;
    for(;;) { if(readFourBytes(endOffset)==0x06054b50 && endOffset+22+readTwoBytes(endOffset+20)==size)break; if(!endOffset)return -8;endOffset--; }
    unsigned entryCount=readTwoBytes(endOffset+10);central=readFourBytes(endOffset+16);
    if(readTwoBytes(endOffset+4)||readTwoBytes(endOffset+6)||readTwoBytes(endOffset+8)!=entryCount||!entryCount||entryCount>256||!clip(central,readFourBytes(endOffset+12),endOffset)||central+readFourBytes(endOffset+12)!=endOffset)return -8;
    unsigned currentPosition=central;
    for(unsigned ordinalIndex=0;ordinalIndex<entryCount;ordinalIndex++) {
        if(!clip(currentPosition,46,endOffset)||readFourBytes(currentPosition)!=0x02014b50||readTwoBytes(currentPosition+34))return -8;
        unsigned namelen=readTwoBytes(currentPosition+28),nextItem=46+namelen+readTwoBytes(currentPosition+30)+readTwoBytes(currentPosition+32);
        if(!namelen||namelen>511||!clip(currentPosition,nextItem,endOffset)||readFourBytes(currentPosition+24)>16384)return -8;
        for(unsigned innerOrdinal=0;innerOrdinal<namelen;innerOrdinal++)if(!archive[currentPosition+46+innerOrdinal])return -8;
        unsigned otherEntry=central;
        for(unsigned innerOrdinal=0;innerOrdinal<ordinalIndex;innerOrdinal++){unsigned lengthData=readTwoBytes(otherEntry+28);if(lengthData==namelen&&equalText(archive+otherEntry+46,archive+currentPosition+46,lengthData))return -8;otherEntry+=46+lengthData+readTwoBytes(otherEntry+30)+readTwoBytes(otherEntry+32);}
        currentPosition+=nextItem;
    }
    if(currentPosition!=endOffset)return -8;entriesList=entryCount;
    unsigned char bundleManifest[4096];int groupSize=jarRead("META-INF/MANIFEST.MF",bundleManifest,sizeof(bundleManifest)-1);if(groupSize<0){entriesList=0;return -8;}
    bundleManifest[groupSize]=0;
    char logical[512];unsigned usedCapacity=0,indexValue=0;int entryPointExists=0;
    while(indexValue<(unsigned)groupSize) {
        unsigned run=indexValue;while(indexValue<(unsigned)groupSize && bundleManifest[indexValue]!='\n')indexValue++;
        unsigned lengthData=indexValue-run;if(indexValue<(unsigned)groupSize)indexValue++;if(lengthData && bundleManifest[run+lengthData-1]=='\r')lengthData--;
        if(usedCapacity && lengthData && bundleManifest[run]==' ') {run++;lengthData--;}
        else {
            int result=attributeData(logical,usedCapacity,&entryPointExists);if(result)return result;
            usedCapacity=0;if(!lengthData)break;
        }
        if(lengthData>sizeof(logical)-usedCapacity)return -8;
        for(unsigned ordinalIndex=0;ordinalIndex<lengthData;ordinalIndex++)logical[usedCapacity++]=bundleManifest[run+ordinalIndex];
    }
    /* The last attribute may be followed by only one newline. */
    int result=attributeData(logical,usedCapacity,&entryPointExists);if(result)return result;
    return entryPointExists?0:-8;
}
