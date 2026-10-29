#include "../naming/machineLinkNames.h"
/* Static Java 8 bytecode -> C -> TinyCC ARM64 code, entirely inside EL0.
 * This is not a complete JVM. Unsupported instructions/APIs stop compilation.
 */
#include "invoke.h"
#include "Bundle.h"
#include "stdio.h"
#include <stdarg.h>
#include <string.h>
#include <stdint.h>
static unsigned char data[16384];static unsigned lengthValue,currentPosition;static int isInvalid;
static unsigned tagsList[512],firstValue[512],secondValue[512],constantPool,currentClass;
static char text[65536];static unsigned textSize;
typedef struct {unsigned configurationBits,name,descriptorData,instructionSequence,size,localVariables,stackStorage;} methodEntry;
static methodEntry declaredMethods[64];static unsigned declaredMethodCount;
static unsigned fieldName[64],fieldDescriptor[64],fieldConstant[64],declaredFieldCount;
static unsigned takeValue(unsigned itemCount){if(currentPosition>lengthValue||itemCount>lengthValue-currentPosition){isInvalid=1;return 0;}unsigned dataPosition=currentPosition;currentPosition+=itemCount;return dataPosition;}
static unsigned byteData(void){unsigned dataPosition=takeValue(1);return isInvalid?0:data[dataPosition];}
static unsigned halfValue(void){unsigned xCoordinate=byteData();return xCoordinate<<8|byteData();}
static uint32_t isFull(void){uint32_t xCoordinate=halfValue();return xCoordinate<<16|halfValue();}
static int unicodeValue(unsigned ordinalIndex,const char*stringData){return ordinalIndex>0&&ordinalIndex<constantPool&&tagsList[ordinalIndex]==1&&strlen(stringData)==secondValue[ordinalIndex]&&!memcmp(data+firstValue[ordinalIndex],stringData,secondValue[ordinalIndex]);}
static int equalText(unsigned xCoordinate,unsigned yCoordinate){return xCoordinate>0&&xCoordinate<constantPool&&yCoordinate>0&&yCoordinate<constantPool&&tagsList[xCoordinate]==1&&tagsList[yCoordinate]==1&&secondValue[xCoordinate]==secondValue[yCoordinate]&&!memcmp(data+firstValue[xCoordinate],data+firstValue[yCoordinate],secondValue[xCoordinate]);}
static void emitValue(const char*fileEntry,...){if(isInvalid)return;va_list argumentArray;va_start(argumentArray,fileEntry);int itemCount=vsnprintf(text+textSize,sizeof(text)-textSize,fileEntry,argumentArray);va_end(argumentArray);if(itemCount<0||(unsigned)itemCount>=sizeof(text)-textSize){isInvalid=1;return;}textSize+=itemCount;}
static int descriptorEntry(unsigned identifierValue,int*result){
    if(identifierValue<1||identifierValue>=constantPool||tagsList[identifierValue]!=1)return -1;unsigned dataPosition=firstValue[identifierValue],endOffset=dataPosition+secondValue[identifierValue];if(dataPosition>=endOffset||data[dataPosition++]!='(')return -1;int entryCount=0;
    while(dataPosition<endOffset&&data[dataPosition]!=')'){
        unsigned characterCode=data[dataPosition++];while(characterCode=='['&&dataPosition<endOffset)characterCode=data[dataPosition++];
        if(characterCode=='L'){while(dataPosition<endOffset&&data[dataPosition]!=';')dataPosition++;if(dataPosition==endOffset)return -1;dataPosition++;}
        else if(characterCode!='I'&&characterCode!='Z'&&characterCode!='B'&&characterCode!='C'&&characterCode!='S')return -1;
        if(++entryCount>16)return -1;
    }
    if(dataPosition+1>=endOffset||data[dataPosition++]!=')')return -1;*result=data[dataPosition]=='V'?0:1;
    if(data[dataPosition]=='J'||data[dataPosition]=='D'||data[dataPosition]=='F')return -1;return entryCount;
}
static void attributes(void){unsigned itemCount=halfValue();for(unsigned ordinalIndex=0;ordinalIndex<itemCount&&!isInvalid;ordinalIndex++){halfValue();unsigned size=isFull();takeValue(size);}}
static int parseInput(void){
    if(isFull()!=0xcafebabe)return -1;unsigned minorVersion=halfValue(),versionNumber=halfValue();if(minorVersion||versionNumber<45||versionNumber>52)return -1;
    constantPool=halfValue();if(constantPool<1||constantPool>512)return -1;
    for(unsigned ordinalIndex=1;ordinalIndex<constantPool&&!isInvalid;ordinalIndex++){
        tagsList[ordinalIndex]=byteData();switch(tagsList[ordinalIndex]){
        case 1:secondValue[ordinalIndex]=halfValue();firstValue[ordinalIndex]=takeValue(secondValue[ordinalIndex]);break;case 3:case 4:firstValue[ordinalIndex]=isFull();break;
        case 5:case 6:takeValue(8);if(++ordinalIndex>=constantPool)return -1;break;
        case 7:case 8:case 16:firstValue[ordinalIndex]=halfValue();break;
        case 9:case 10:case 11:case 12:case 18:firstValue[ordinalIndex]=halfValue();secondValue[ordinalIndex]=halfValue();break;
        case 15:firstValue[ordinalIndex]=byteData();secondValue[ordinalIndex]=halfValue();break;default:return -1;
        }
    }
    halfValue();currentClass=halfValue();halfValue();if(currentClass<1||currentClass>=constantPool||tagsList[currentClass]!=7||firstValue[currentClass]<1||firstValue[currentClass]>=constantPool||tagsList[firstValue[currentClass]]!=1)return -1;unsigned interfaces=halfValue();takeValue(interfaces*2);
    declaredFieldCount=halfValue();if(declaredFieldCount>64)return -1;
    for(unsigned ordinalIndex=0;ordinalIndex<declaredFieldCount&&!isInvalid;ordinalIndex++){
        unsigned configurationBits=halfValue();fieldName[ordinalIndex]=halfValue();fieldDescriptor[ordinalIndex]=halfValue();
        if(!(configurationBits&8))return -1;
        unsigned entryCount=halfValue();for(unsigned innerOrdinal=0;innerOrdinal<entryCount&&!isInvalid;innerOrdinal++){
            unsigned name=halfValue(),size=isFull();
            if(unicodeValue(name,"ConstantValue")){if(size!=2)return -1;fieldConstant[ordinalIndex]=halfValue();}
            else takeValue(size);
        }
    }
    declaredMethodCount=halfValue();if(declaredMethodCount>64)return -1;
    for(unsigned ordinalIndex=0;ordinalIndex<declaredMethodCount&&!isInvalid;ordinalIndex++){
        methodEntry*groupSize=declaredMethods+ordinalIndex;groupSize->configurationBits=halfValue();groupSize->name=halfValue();groupSize->descriptorData=halfValue();unsigned entryCount=halfValue();
        for(unsigned innerOrdinal=0;innerOrdinal<entryCount&&!isInvalid;innerOrdinal++){
            unsigned name=halfValue(),size=isFull(),run=currentPosition;
            if(size>lengthValue-currentPosition)return -1;
            if(unicodeValue(name,"Code")){
                groupSize->stackStorage=halfValue();groupSize->localVariables=halfValue();groupSize->size=isFull();groupSize->instructionSequence=takeValue(groupSize->size);
                if(groupSize->stackStorage>128||groupSize->localVariables>128||groupSize->size>8192||halfValue())return -1;attributes();
            }else takeValue(size);
            if(currentPosition!=run+size)return -1;
        }
        if(!unicodeValue(groupSize->name,"<init>")&&(!(groupSize->configurationBits&8)||(groupSize->configurationBits&(0x100|0x20))||!groupSize->size))return -1;
    }
    attributes();return isInvalid||currentPosition!=lengthValue?-1:0;
}
static void constantValue(unsigned identifierValue){
    if(!identifierValue||identifierValue>=constantPool){isInvalid=1;return;}
    if(tagsList[identifierValue]==3)emitValue("P(%uU);",firstValue[identifierValue]);
    else if(tagsList[identifierValue]==8)emitValue("P((W)k%u);",identifierValue);else isInvalid=1;
}
static void invoke(unsigned identifierValue,int virtualCall){
    if(identifierValue<1||identifierValue>=constantPool||(tagsList[identifierValue]!=10&&tagsList[identifierValue]!=11)||firstValue[identifierValue]<1||firstValue[identifierValue]>=constantPool||tagsList[firstValue[identifierValue]]!=7||secondValue[identifierValue]<1||secondValue[identifierValue]>=constantPool||tagsList[secondValue[identifierValue]]!=12){isInvalid=1;return;}
    unsigned ownerObject=firstValue[firstValue[identifierValue]],name=firstValue[secondValue[identifierValue]],descriptorData=secondValue[secondValue[identifierValue]];int result=0,itemCount=descriptorEntry(descriptorData,&result);if(itemCount<0){isInvalid=1;return;}
    for(int ordinalIndex=itemCount;ordinalIndex>0;ordinalIndex--)emitValue("x[%d]=Q();",ordinalIndex-1);if(virtualCall)emitValue("Q();");
    if(!virtualCall&&equalText(ownerObject,firstValue[currentClass])){
        unsigned groupSize=0;for(;groupSize<declaredMethodCount;groupSize++)if(equalText(name,declaredMethods[groupSize].name)&&equalText(descriptorData,declaredMethods[groupSize].descriptorData))break;
        if(groupSize==declaredMethodCount||!(declaredMethods[groupSize].configurationBits&8)){isInvalid=1;return;}
        if(result)emitValue("P(");emitValue("m%u(",groupSize);for(int ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)emitValue(ordinalIndex?",x[%d]":"x[%d]",ordinalIndex);emitValue(result?"));":" );");return;
    }
    if((virtualCall&&unicodeValue(ownerObject,"java/io/PrintStream")&& (unicodeValue(name,"print")||unicodeValue(name,"println")))||(!virtualCall&&unicodeValue(ownerObject,"English/Native/Output"))){
        if(unicodeValue(descriptorData,"(I)V")&&(unicodeValue(name,"print")||unicodeValue(name,"println")||unicodeValue(name,"writeNumber"))){emitValue("jprint(x[0],1,%d);",unicodeValue(name,"print")?0:1);return;}
        if(unicodeValue(descriptorData,"(Ljava/lang/String;)V")&&(unicodeValue(name,"print")||unicodeValue(name,"println")||unicodeValue(name,"write")||unicodeValue(name,"writeLine"))){emitValue("jprint(x[0],0,%d);",unicodeValue(name,"print")||unicodeValue(name,"write")?0:1);return;}
        if(unicodeValue(descriptorData,"()V")&&unicodeValue(name,"println")){emitValue("jprint((W)\"\",0,1);");return;}
    }
    if(!virtualCall&&unicodeValue(ownerObject,"English/Native/file")){
        if(unicodeValue(name,"write")&&unicodeValue(descriptorData,"(Ljava/lang/String;Ljava/lang/String;)V")){emitValue("jfwrite(x[0],x[1]);");return;}
        if(unicodeValue(name,"read")&&unicodeValue(descriptorData,"(Ljava/lang/String;)Ljava/lang/String;")){emitValue("P(jfread(x[0]));");return;}
    }
    isInvalid=1;
}
static void compileMethod(unsigned lookupIndex){
    methodEntry*groupSize=declaredMethods+lookupIndex;if(unicodeValue(groupSize->name,"<init>"))return;int result,itemCount=descriptorEntry(groupSize->descriptorData,&result);if(itemCount<0){isInvalid=1;return;}
    emitValue("static W m%u(",lookupIndex);for(int ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)emitValue(ordinalIndex?",W a%d":"W a%d",ordinalIndex);if(!itemCount)emitValue("void");
    if((unsigned)itemCount>groupSize->localVariables){isInvalid=1;return;}
    emitValue("){W v[%u]={0},s[128],x[16];int sp=0;W q,r;\n",groupSize->localVariables?groupSize->localVariables:1);for(int ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)emitValue("v[%d]=a%d;",ordinalIndex,ordinalIndex);
    unsigned saved=lengthValue;lengthValue=groupSize->instructionSequence+groupSize->size;currentPosition=groupSize->instructionSequence;
    while(currentPosition<lengthValue&&!isInvalid){unsigned commandPosition=currentPosition-groupSize->instructionSequence,operationValue=byteData();emitValue("L%u:;",commandPosition);
        if(operationValue==0){}
        else if(operationValue==1)emitValue("P(0);");
        else if(operationValue>=2&&operationValue<=8)emitValue("P(%uU);",operationValue-3);
        else if(operationValue==16){int value=(int8_t)byteData();emitValue("P(%uU);",(unsigned)value);}
        else if(operationValue==17){int value=(int16_t)halfValue();emitValue("P(%uU);",(unsigned)value);}
        else if(operationValue==18||operationValue==19)constantValue(operationValue==18?byteData():halfValue());
        else if(operationValue==21||operationValue==25){unsigned ordinalIndex=byteData();if(ordinalIndex>=groupSize->localVariables)isInvalid=1;emitValue("P(v[%u]);",ordinalIndex);}
        else if((operationValue>=26&&operationValue<=29)||(operationValue>=42&&operationValue<=45)){unsigned ordinalIndex=operationValue>=42?operationValue-42:operationValue-26;if(ordinalIndex>=groupSize->localVariables)isInvalid=1;emitValue("P(v[%u]);",ordinalIndex);}
        else if(operationValue==54||operationValue==58){unsigned ordinalIndex=byteData();if(ordinalIndex>=groupSize->localVariables)isInvalid=1;emitValue("v[%u]=Q();",ordinalIndex);}
        else if((operationValue>=59&&operationValue<=62)||(operationValue>=75&&operationValue<=78)){unsigned ordinalIndex=operationValue>=75?operationValue-75:operationValue-59;if(ordinalIndex>=groupSize->localVariables)isInvalid=1;emitValue("v[%u]=Q();",ordinalIndex);}
        else if(operationValue==46||operationValue==50||operationValue==51||operationValue==52||operationValue==53)emitValue("q=Q();r=Q();P(*jindex(r,(int)q));");
        else if(operationValue==79||operationValue==83||operationValue==84||operationValue==85||operationValue==86)emitValue("q=Q();r=Q();*jindex(Q(),(int)r)=%s;",operationValue==84?"(unsigned)(signed char)q":operationValue==85?"(unsigned short)q":operationValue==86?"(unsigned)(short)q":"q");
        else if(operationValue==87)emitValue("Q();");
        else if(operationValue==89)emitValue("q=Q();P(q);P(q);");
        else if(operationValue==90)emitValue("q=Q();r=Q();P(q);P(r);P(q);");
        else if(operationValue==95)emitValue("q=Q();r=Q();P(q);P(r);");
        else if(operationValue==96||operationValue==100||operationValue==104||operationValue==120||operationValue==124||operationValue==126||operationValue==128||operationValue==130){const char*encodingValue=operationValue==96?"+":operationValue==100?"-":operationValue==104?"*":operationValue==120?"<<":operationValue==124?">>":operationValue==126?"&":operationValue==128?"|":"^";emitValue("q=Q();r=Q();P((unsigned)r%s(unsigned)q%s);",encodingValue,operationValue==120||operationValue==124?"%32":"");}
        else if(operationValue==108||operationValue==112)emitValue("q=Q();r=Q();P((unsigned)jdivide((int)r,(int)q,%d));",operationValue==112);
        else if(operationValue==116)emitValue("P(0U-(unsigned)Q());");
        else if(operationValue==122)emitValue("q=Q();r=Q();P((unsigned)((int)r>>((unsigned)q&31)));");
        else if(operationValue==132){unsigned ordinalIndex=byteData();int differenceValue=(int8_t)byteData();if(ordinalIndex>=groupSize->localVariables)isInvalid=1;emitValue("v[%u]=(unsigned)v[%u]+%uU;",ordinalIndex,ordinalIndex,(unsigned)differenceValue);}
        else if(operationValue>=145&&operationValue<=147)emitValue("P((unsigned)(%s)Q());",operationValue==145?"signed char":operationValue==146?"unsigned short":"short");
        else if(operationValue>=153&&operationValue<=166){int targetValue=(int)commandPosition+(int16_t)halfValue();const char*comparisonValue[]={"==","!=","<",">=",">","<="};if(targetValue<0||targetValue>=(int)groupSize->size){isInvalid=1;break;}if(operationValue<159)emitValue("if((int)Q()%s0)goto L%d;",comparisonValue[operationValue-153],targetValue);else if(operationValue<165)emitValue("q=Q();r=Q();if((int)r%s(int)q)goto L%d;",comparisonValue[operationValue-159],targetValue);else emitValue("q=Q();r=Q();if(r%sq)goto L%d;",operationValue==165?"==":"!=",targetValue);}
        else if(operationValue==167){int targetValue=(int)commandPosition+(int16_t)halfValue();if(targetValue<0||targetValue>=(int)groupSize->size)isInvalid=1;emitValue("goto L%d;",targetValue);}
        else if(operationValue==172||operationValue==176)emitValue("return Q();");else if(operationValue==177)emitValue("return 0;");
        else if(operationValue==178||operationValue==179){unsigned identifierValue=halfValue();if(identifierValue<1||identifierValue>=constantPool||tagsList[identifierValue]!=9||firstValue[identifierValue]>=constantPool||secondValue[identifierValue]>=constantPool||tagsList[firstValue[identifierValue]]!=7||tagsList[secondValue[identifierValue]]!=12){isInvalid=1;break;}unsigned ownerObject=firstValue[firstValue[identifierValue]],name=firstValue[secondValue[identifierValue]],descriptorData=secondValue[secondValue[identifierValue]];
            if(operationValue==178&&unicodeValue(ownerObject,"java/lang/System")&&unicodeValue(name,"out")&&unicodeValue(descriptorData,"Ljava/io/PrintStream;"))emitValue("P(1);");
            else {unsigned fileEntry=0;while(fileEntry<declaredFieldCount&&(!equalText(name,fieldName[fileEntry])||!equalText(descriptorData,fieldDescriptor[fileEntry])))fileEntry++;if(!equalText(ownerObject,firstValue[currentClass])||fileEntry==declaredFieldCount){isInvalid=1;break;}emitValue(operationValue==178?"P(fields[%u]);":"fields[%u]=Q();",fileEntry);}}
        else if(operationValue==182||operationValue==184)invoke(halfValue(),operationValue==182);
        else if(operationValue==188){unsigned typeCategory=byteData();if(typeCategory!=4&&typeCategory!=5&&typeCategory!=8&&typeCategory!=9&&typeCategory!=10)isInvalid=1;emitValue("P(jarray((int)Q()));");}
        else if(operationValue==190)emitValue("P(jlength(Q()));");
        else if(operationValue==198||operationValue==199){int targetValue=(int)commandPosition+(int16_t)halfValue();if(targetValue<0||targetValue>=(int)groupSize->size)isInvalid=1;emitValue("if(Q()%s0)goto L%d;",operationValue==198?"==":"!=",targetValue);}
        else isInvalid=1;
        if(isInvalid)printf("jaot: method %u bytecode %u at %u unsupported or malformed\n",lookupIndex,operationValue,commandPosition);
        emitValue("\n");
    }
    lengthValue=saved;emitValue("jfail();return 0;}\n");
}
static unsigned stringUnit(unsigned *dataPosition,unsigned endOffset){
    if(*dataPosition>=endOffset){isInvalid=1;return 0;}unsigned characterCode=data[(*dataPosition)++];
    if(characterCode<128)return characterCode;
    unsigned itemCount=characterCode>=0xc0&&characterCode<=0xdf?1:characterCode>=0xe0&&characterCode<=0xef?2:3;
    if(itemCount==3||itemCount>endOffset-*dataPosition){isInvalid=1;return 0;}unsigned value=characterCode&((1u<<(6-itemCount))-1);
    for(unsigned ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++){unsigned nextItem=data[(*dataPosition)++];if((nextItem&0xc0)!=0x80)isInvalid=1;value=value<<6|(nextItem&63);}
    if((itemCount==1&&value<128&&value!=0)||(itemCount==2&&value<2048))isInvalid=1;return value;
}
static void stringConstant(unsigned identifierValue){
    unsigned unsignedValue=firstValue[identifierValue];if(unsignedValue<1||unsignedValue>=constantPool||tagsList[unsignedValue]!=1){isInvalid=1;return;}emitValue("static const unsigned char k%u[]={",identifierValue);
    unsigned dataPosition=firstValue[unsignedValue],endOffset=dataPosition+secondValue[unsignedValue];
    while(dataPosition<endOffset&&!isInvalid){unsigned characterCode=stringUnit(&dataPosition,endOffset);
        if(characterCode>=0xd800&&characterCode<=0xdbff){unsigned lowPart=stringUnit(&dataPosition,endOffset);if(lowPart<0xdc00||lowPart>0xdfff){isInvalid=1;break;}characterCode=0x10000+((characterCode-0xd800)<<10)+lowPart-0xdc00;}
        else if(characterCode>=0xdc00&&characterCode<=0xdfff){isInvalid=1;break;}
        if(!characterCode){printf("jaot: embedded NUL string needs JVM mode\n");isInvalid=1;break;}
        if(characterCode<128)emitValue("%u,",characterCode);
        else{unsigned itemCount=characterCode<2048?2:characterCode<65536?3:4;emitValue("%u,",(itemCount==2?0xc0:itemCount==3?0xe0:0xf0)|(characterCode>>(6*(itemCount-1))));for(unsigned ordinalIndex=itemCount-1;ordinalIndex;ordinalIndex--)emitValue("%u,",0x80|((characterCode>>(6*(ordinalIndex-1)))&63));}
    }emitValue("0};\n");
}
const char *jaotSource(const char*name){
    size_t itemCount=strlen(name);
    if(itemCount>4&&!strcmp(name+itemCount-4,".jar")){
        if(jarOpen(name)<0){printf("jaot: invalid JAR/Main-Class\n");return 0;}char path[256];const char*entryMethod=jarMain();itemCount=strlen(entryMethod);if(itemCount+6>=sizeof(path))return 0;
        for(unsigned ordinalIndex=0;ordinalIndex<itemCount;ordinalIndex++)path[ordinalIndex]=entryMethod[ordinalIndex]=='.'?'/':entryMethod[ordinalIndex];strcpy(path+itemCount,".class");int entryCount=jarRead(path,data,sizeof(data));if(entryCount<0)return 0;lengthValue=entryCount;
    }else{intptr_t fileHandle=userInvoke(3,(uintptr_t)name,0,0,0,0,0);if(fileHandle<0)return 0;intptr_t entryCount=userInvoke(9,fileHandle,0,0,0,0,0);if(entryCount<0||entryCount>sizeof(data)){userInvoke(4,fileHandle,0,0,0,0,0);return 0;}intptr_t receivedCount=userInvoke(2,fileHandle,(uintptr_t)data,entryCount,0,0,0);userInvoke(4,fileHandle,0,0,0,0,0);if(receivedCount!=entryCount)return 0;lengthValue=entryCount;}
    if(parseInput()<0){printf("jaot: requires static Java 8 int/reference subset without exceptions\n");return 0;}
    emitValue("typedef unsigned long W; extern void jfail(void);extern void jpush(W*,int*,W);extern W jpop(W*,int*);extern W jarray(int);extern W*jindex(W,int);extern int jlength(W),jdivide(int,int,int);extern void jprint(W,int,int);extern W jfread(W),jfwrite(W,W);static W fields[64];\n#define P(x) jpush(s,&sp,(W)(x))\n#define Q() jpop(s,&sp)\n");
    for(unsigned ordinalIndex=1;ordinalIndex<constantPool&&!isInvalid;ordinalIndex++)if(tagsList[ordinalIndex]==8)stringConstant(ordinalIndex);
    if(isInvalid)return 0;
    int entryPoint=-1,initialValue=-1;
    for(unsigned ordinalIndex=0;ordinalIndex<declaredMethodCount;ordinalIndex++)if(!unicodeValue(declaredMethods[ordinalIndex].name,"<init>")){
        int result,entryCount=descriptorEntry(declaredMethods[ordinalIndex].descriptorData,&result);if(entryCount<0)return 0;emitValue("static W m%u(",ordinalIndex);for(int innerOrdinal=0;innerOrdinal<entryCount;innerOrdinal++)emitValue(innerOrdinal?",W":"W");if(!entryCount)emitValue("void");emitValue(");\n");
        if(unicodeValue(declaredMethods[ordinalIndex].name,"main")&&unicodeValue(declaredMethods[ordinalIndex].descriptorData,"([Ljava/lang/String;)V")&&(declaredMethods[ordinalIndex].configurationBits&9)==9)entryPoint=ordinalIndex;
        if(unicodeValue(declaredMethods[ordinalIndex].name,"<clinit>"))initialValue=ordinalIndex;
    }
    if(entryPoint<0)return 0;for(unsigned ordinalIndex=0;ordinalIndex<declaredMethodCount&&!isInvalid;ordinalIndex++)compileMethod(ordinalIndex);
    emitValue("int main(int argc,char**argv){W a[9]={0};a[0]=argc>0?argc-1:0;for(int i=1;i<argc&&i<9;i++)a[i]=(W)argv[i];");
    for(unsigned ordinalIndex=0;ordinalIndex<declaredFieldCount;ordinalIndex++)if(fieldConstant[ordinalIndex]){
        unsigned characterCode=fieldConstant[ordinalIndex];if(characterCode>=constantPool)return 0;
        if(tagsList[characterCode]==3)emitValue("fields[%u]=%uU;",ordinalIndex,firstValue[characterCode]);else if(tagsList[characterCode]==8)emitValue("fields[%u]=(W)k%u;",ordinalIndex,characterCode);else return 0;
    }
    if(initialValue>=0)emitValue("m%d();",initialValue);emitValue("m%d((W)a);return 0;}\n",entryPoint);
    return isInvalid?0:text;
}
