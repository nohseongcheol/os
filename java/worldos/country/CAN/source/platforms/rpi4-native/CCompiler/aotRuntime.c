#include "../naming/machineLinkNames.h"
/* Small native runtime for jaot's explicitly checked static Java subset. */
#include "invoke.h"
#include "FileABI.h"
typedef unsigned long machineWord;
static machineWord heapStorage[8192];static unsigned usedCapacity;
void jfail(void){const char text[]="AOT runtime error\n";writeFileData(2,text,sizeof(text)-1);userInvoke(6,1,0,0,0,0,0);for(;;){}}
void jpush(machineWord *stackStorage,int *depthValue,machineWord value){if(*depthValue<0||*depthValue>=128)jfail();stackStorage[(*depthValue)++]=value;}
machineWord javaPopValue(machineWord *stackStorage,int *depthValue){if(*depthValue<=0||*depthValue>128)jfail();return stackStorage[--*depthValue];}
machineWord jarray(int itemCount){if(itemCount<0||(unsigned)itemCount+1>8192-usedCapacity)jfail();machineWord*dataPosition=heapStorage+usedCapacity;usedCapacity+=itemCount+1;dataPosition[0]=itemCount;return (machineWord)dataPosition;}
machineWord *jindex(machineWord objectReference,int itemCount){machineWord*dataPosition=(machineWord*)objectReference;if(!dataPosition||itemCount<0||(machineWord)itemCount>=dataPosition[0])jfail();return dataPosition+itemCount+1;}
int jlength(machineWord objectReference){if(!objectReference)jfail();return *(machineWord*)objectReference;}
int jdivide(int xCoordinate,int yCoordinate,int remainderValue){if(!yCoordinate)jfail();if(xCoordinate==(-2147483647-1)&&yCoordinate==-1)return remainderValue?0:xCoordinate;return remainderValue?xCoordinate%yCoordinate:xCoordinate/yCoordinate;}
static unsigned lengthValue(const char*stringData){unsigned itemCount=0;if(!stringData)jfail();while(stringData[itemCount])itemCount++;return itemCount;}
void jprint(machineWord dataPosition,int numericValue,int newline){
    if(numericValue){char secondValue[16];unsigned itemCount=0;int value=(int)dataPosition;unsigned unsignedValue=value<0?0-(unsigned)value:value;do{secondValue[itemCount++]='0'+unsignedValue%10;unsignedValue/=10;}while(unsignedValue);if(value<0)secondValue[itemCount++]='-';while(itemCount)writeFileData(1,secondValue+--itemCount,1);}
    else{const char*stringData=dataPosition?(const char*)dataPosition:"null";writeFileData(1,stringData,lengthValue(stringData));}if(newline)writeFileData(1,"\n",1);
}
machineWord jfwrite(machineWord path,machineWord value){const char*stringData=(const char*)value;unsigned itemCount=lengthValue(stringData);int fileHandle=openFile((const char*)path,writeOnlyValue|CreateIfMissing|TruncateContents,0600);if(fileHandle<0)jfail();int returnedValue=writeFileData(fileHandle,stringData,itemCount);closeFile(fileHandle);if(returnedValue!=(int)itemCount)jfail();return 0;}
machineWord jfread(machineWord path){int fileHandle=openFile((const char*)path,readOnlyValue,0);if(fileHandle<0)jfail();int itemCount=fileSize(fileHandle);if(itemCount<0||itemCount>16384||(unsigned)(itemCount+8)/8>8192-usedCapacity)jfail();char*dataPosition=(char*)(heapStorage+usedCapacity);usedCapacity+=(itemCount+8)/8;int returnedValue=readFileData(fileHandle,dataPosition,itemCount);closeFile(fileHandle);if(returnedValue!=itemCount)jfail();dataPosition[itemCount]=0;return (machineWord)dataPosition;}
