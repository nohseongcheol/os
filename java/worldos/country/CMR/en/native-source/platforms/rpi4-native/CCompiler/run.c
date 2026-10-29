#include "../naming/machineLinkNames.h"
#include "invoke.h"
#include "libtcc.h"
#include "stdio.h"
#include <string.h>
#include <stdint.h>
extern const unsigned char *cOutput(size_t *);
extern const char *jaotSource(const char *);
typedef struct { unsigned char identifierValue[16];uint16_t typeCategory,machineType;uint32_t versionNumber;uint64_t entryPoint,programHeaderOffset,sectionHeaderOffset;uint32_t configurationBits;uint16_t size,programHeaderSize,programHeaderCount,sectionHeaderSize,sectionHeaderCount,sectionNameTable; } headerValue;
typedef struct {uint32_t typeCategory,configurationBits;uint64_t offsetValue,address,physicalAddress,filesz,memsz,alignBoundary;} segmentValue;
static unsigned char image[16384];
static int publishEntry(const char *name){
    size_t itemCount;const unsigned char*originalData=cOutput(&itemCount);if(itemCount<sizeof(headerValue))return -1;
    headerValue executableHeader;memcpy(&executableHeader,originalData,sizeof(executableHeader));
    if(executableHeader.typeCategory!=2||executableHeader.machineType!=183||executableHeader.programHeaderSize!=sizeof(segmentValue)||!executableHeader.programHeaderCount||executableHeader.programHeaderCount>16||executableHeader.programHeaderOffset>itemCount||executableHeader.programHeaderCount*sizeof(segmentValue)>itemCount-executableHeader.programHeaderOffset)return -1;
    executableHeader.programHeaderOffset=sizeof(executableHeader);executableHeader.sectionHeaderOffset=executableHeader.sectionHeaderCount=executableHeader.sectionHeaderSize=executableHeader.sectionNameTable=0;memcpy(image,&executableHeader,sizeof(executableHeader));
    size_t auxiliaryInformation=sizeof(executableHeader)+executableHeader.programHeaderCount*sizeof(segmentValue),nextItem=4096;unsigned char pageList[3072]={0};int validEntryPoint=0;
    for(unsigned ordinalIndex=0;ordinalIndex<executableHeader.programHeaderCount;ordinalIndex++){
        segmentValue dataPosition;headerValue original;memcpy(&original,originalData,sizeof(original));memcpy(&dataPosition,originalData+original.programHeaderOffset+ordinalIndex*sizeof(dataPosition),sizeof(dataPosition));
        if(dataPosition.offsetValue>itemCount||dataPosition.filesz>itemCount-dataPosition.offsetValue||dataPosition.filesz>dataPosition.memsz)return -1;
        if(dataPosition.typeCategory==1){
            if((dataPosition.configurationBits&~7u)||!(dataPosition.configurationBits&4)||(dataPosition.configurationBits&3)==3||dataPosition.address<0x02000000||dataPosition.address>0x02c00000||dataPosition.memsz>0x02c00000-dataPosition.address)return -1;
            if((dataPosition.configurationBits&1)&&executableHeader.entryPoint>=dataPosition.address&&executableHeader.entryPoint-dataPosition.address<dataPosition.filesz&&!(executableHeader.entryPoint&3))validEntryPoint=1;
            size_t precedingValue=dataPosition.address&4095,byteValues=dataPosition.filesz?precedingValue+dataPosition.filesz:0;
            if(nextItem>sizeof(image)||byteValues>sizeof(image)-nextItem){printf("cc: ELF load data needs %u bytes; file limit is %u\n",(unsigned)(nextItem+byteValues),(unsigned)sizeof(image));return -1;}
            if(byteValues)memcpy(image+nextItem+precedingValue,originalData+dataPosition.offsetValue,dataPosition.filesz);
            dataPosition.address-=precedingValue;dataPosition.physicalAddress=dataPosition.address;dataPosition.memsz+=precedingValue;dataPosition.filesz=byteValues;dataPosition.offsetValue=nextItem;dataPosition.alignBoundary=4096;
            for(uint64_t pageValue=dataPosition.address;pageValue<dataPosition.address+dataPosition.memsz;pageValue+=4096){unsigned lookupIndex=(pageValue-0x02000000)/4096;if(lookupIndex>=sizeof(pageList)||pageList[lookupIndex]){printf("cc: ELF load segments overlap or leave user memory\n");return -1;}pageList[lookupIndex]=1;}
            nextItem+=(byteValues+4095)&~(size_t)4095;
        }else if(dataPosition.typeCategory==4){if(dataPosition.filesz>4096-auxiliaryInformation)return -1;memcpy(image+auxiliaryInformation,originalData+dataPosition.offsetValue,dataPosition.filesz);dataPosition.offsetValue=auxiliaryInformation;auxiliaryInformation+=dataPosition.filesz;}
        else if(dataPosition.typeCategory!=0&&dataPosition.typeCategory!=6&&dataPosition.typeCategory!=0x6474e551)return -1;
        memcpy(image+executableHeader.programHeaderOffset+ordinalIndex*sizeof(dataPosition),&dataPosition,sizeof(dataPosition));
    }
    if(!validEntryPoint)return -1;
    intptr_t fileHandle=userInvoke(3,(uintptr_t)name,577,0600,0,0,0);if(fileHandle<0){printf("cc: cannot create output file, error %d\n",(int)fileHandle);return -1;}
    intptr_t written=userInvoke(1,fileHandle,(uintptr_t)image,nextItem,0,0,0);userInvoke(4,fileHandle,0,0,0,0,0);return written==(intptr_t)nextItem?0:-1;
}
int startUserProgram(int methodMode){
    char input[256],selectedEntry[256],output[256]="a.elf";
    int argumentsCount=userInvoke(15,UINTPTR_MAX,0,0,0,0,0);
    if(argumentsCount!=1&&argumentsCount!=3){printf(methodMode?"Usage: jaot FILE.class|FILE.jar [-o FILE.elf]\n":"Usage: cc FILE.c [-o FILE.elf] (TinyCC/native ABI)\n");return 2;}
    if(userInvoke(15,0,(uintptr_t)input,sizeof(input),0,0,0)<0)return 2;
    if(argumentsCount==1&&(!strcmp(input,"--version")||!strcmp(input,"-version"))){printf(methodMode?"jkoros jaot 0.1: static Java subset -> native ARM64 ELF\n":"jkoros TinyCC ARM64: freestanding C, native ABI v1\n");return 0;}
    if(argumentsCount==3){userInvoke(15,1,(uintptr_t)selectedEntry,sizeof(selectedEntry),0,0,0);if(strcmp(selectedEntry,"-o")||userInvoke(15,2,(uintptr_t)output,sizeof(output),0,0,0)<0)return 2;}
    if(!strcmp(input,output)){printf("cc: input and output must differ\n");return 2;}
    TCCState*stringData=tcc_new();if(!stringData)return 1;
    tcc_undefine_symbol(stringData,"__linux__");tcc_undefine_symbol(stringData,"__linux");tcc_undefine_symbol(stringData,"linux");
    tcc_undefine_symbol(stringData,"__unix__");tcc_undefine_symbol(stringData,"__unix");tcc_undefine_symbol(stringData,"unix");
    tcc_undefine_symbol(stringData,"__STDC_HOSTED__");tcc_define_symbol(stringData,"__STDC_HOSTED__","0");tcc_define_symbol(stringData,"__JKOROS__","1");
    tcc_set_options(stringData,"-nostdlib -nostdinc -static -Wl,-Ttext=0x02000000,-section-alignment=0x1000");
    tcc_add_include_path(stringData,"/sdk/include");
    int returnedValue=tcc_set_output_type(stringData,TCC_OUTPUT_EXE);
    if(!returnedValue){if(methodMode){const char*originalData=jaotSource(input);returnedValue=originalData?tcc_compile_string(stringData,originalData):-1;}else returnedValue=tcc_add_file(stringData,input);}
    if(!returnedValue)returnedValue=tcc_add_file(stringData,"/sdk/lib/start.o");
    if(!returnedValue)returnedValue=tcc_add_file(stringData,"/sdk/lib/crt.o");
    if(!returnedValue&&methodMode)returnedValue=tcc_add_file(stringData,"/sdk/lib/aot-runtime.o");
    if(!returnedValue)returnedValue=tcc_add_file(stringData,"/sdk/lib/libposix-kor-user.a");
    if(!returnedValue)returnedValue=tcc_output_file(stringData,"/@cc-output");
    if(!returnedValue)returnedValue=publishEntry(output);
    tcc_delete(stringData);
    if(returnedValue){printf("cc: failed; output requires native ABI and <=16384 bytes\n");return 1;}
    printf(methodMode?"AOT compiled native ARM64 ELF: %s\n":"Compiled native ARM64 ELF: %s\n",output);return 0;
}
