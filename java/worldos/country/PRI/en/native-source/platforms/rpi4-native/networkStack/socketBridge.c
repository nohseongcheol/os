#include "../naming/machineLinkNames.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "networkStack.h"
extern int32_t jloopnetSocket(int32_t,int32_t,int32_t), jloopnetBind(int32_t,int32_t,int32_t);
extern int32_t jloopnetSend(int32_t,int32_t,int32_t,int32_t), jloopnetRecv(int32_t,int32_t);
extern int32_t jloopnetPort(int32_t), jloopnetAddress(int32_t), jloopnetPeer(int32_t), jloopnetClose(int32_t);
extern int32_t jnetPut(int32_t,int32_t),jnetGet(int32_t);
extern int32_t jloopstreamCreate(void),jloopstreamBind(int32_t,int32_t,int32_t),jloopstreamListen(int32_t,int32_t);
extern int32_t jloopstreamConnect(int32_t,int32_t,int32_t),jloopstreamAccept(int32_t),jloopstreamRead(int32_t,int32_t),jloopstreamWrite(int32_t,int32_t);
extern int32_t jloopstreamPort(int32_t),jloopstreamPeer(int32_t),jloopstreamClose(int32_t);
static int external[24];
static int anyAddress[24], dualListener[24], udpExternalPeer[8], boundAddress[8];
static int externalNumber(int fileHandle) { return fileHandle>=32 && fileHandle<56 ? external[fileHandle-32]-1 : -1; }
static int pasteText(int fileHandle,int typeCategory) {
    if(fileHandle<32||fileHandle>=56)return -9;int previousItem=externalNumber(fileHandle);if(previousItem>=0)return previousItem;
    int itemCount=createSocketEndpoint(typeCategory);if(itemCount>=0)external[fileHandle-32]=itemCount+1;return itemCount;
}
int32_t jnetSocket(int32_t firstValue,int32_t secondValue,int32_t characterCode){return jloopnetSocket(firstValue,secondValue,characterCode);}
int32_t jnetBind(int32_t fileHandle,int32_t InternetAddress,int32_t portNumber){
    if(InternetAddress==0x7f000001)return jloopnetBind(fileHandle,InternetAddress,portNumber);
    if(InternetAddress!=0&&InternetAddress!=readNetworkStatus(0,0))return -99;
    int returnedValue=jloopnetBind(fileHandle,0,portNumber);if(returnedValue<0)return returnedValue;
    int itemCount=pasteText(fileHandle,2);if(itemCount<0)return itemCount;returnedValue=netBind(itemCount,readNetworkStatus(0,0),jloopnetPort(fileHandle));if(!returnedValue)boundAddress[fileHandle-32]=InternetAddress;return returnedValue;
}
int32_t jnetSend(int32_t fileHandle,int32_t InternetAddress,int32_t portNumber,int32_t size){
    if(InternetAddress==0x7f000001)return jloopnetSend(fileHandle,InternetAddress,portNumber,size);
    if(size<0||size>512)return -90;if(portNumber<1||portNumber>65535)return -22;
    if(jloopnetPort(fileHandle)<0)return -9;
    if(jloopnetAddress(fileHandle)==0x7f000001)return -101;
    int itemCount=externalNumber(fileHandle);if(itemCount<0){int returnedValue=0;if(jloopnetPort(fileHandle)==0)returnedValue=jloopnetBind(fileHandle,0,0);if(returnedValue<0)return returnedValue;itemCount=pasteText(fileHandle,2);if(itemCount<0)return itemCount;returnedValue=netBind(itemCount,readNetworkStatus(0,0),jloopnetPort(fileHandle));if(returnedValue<0)return returnedValue;}
    unsigned char data[512];for(int ordinalIndex=0;ordinalIndex<size;ordinalIndex++)data[ordinalIndex]=jnetGet(ordinalIndex);return sendDatagram(itemCount,data,size,InternetAddress,portNumber);
}
int32_t jnetRecv(int32_t fileHandle,int32_t size){
    int itemCount=externalNumber(fileHandle);if(itemCount<0)return jloopnetRecv(fileHandle,size);if(size<0||size>512)return -22;
    int local=jloopnetRecv(fileHandle,size);if(local!=-11){udpExternalPeer[fileHandle-32]=0;return local;}
    unsigned char data[512];int returnedValue=receiveDatagram(itemCount,data,size);if(returnedValue>=0)udpExternalPeer[fileHandle-32]=1;for(int ordinalIndex=0;ordinalIndex<returnedValue;ordinalIndex++)jnetPut(ordinalIndex,data[ordinalIndex]);return returnedValue;
}
int32_t jnetPort(int32_t fileHandle){int itemCount=externalNumber(fileHandle);return itemCount<0?jloopnetPort(fileHandle):(int32_t)networkPortNumber(itemCount);}
int32_t jnetAddress(int32_t fileHandle){return externalNumber(fileHandle)<0?jloopnetAddress(fileHandle):boundAddress[fileHandle-32];}
int32_t jnetPeer(int32_t fileHandle){int itemCount=externalNumber(fileHandle);return itemCount<0||!udpExternalPeer[fileHandle-32]?jloopnetPeer(fileHandle):(int32_t)peerPortNumber(itemCount);}
int32_t jnetRemote(int32_t fileHandle){int itemCount=externalNumber(fileHandle);return itemCount<0||!udpExternalPeer[fileHandle-32]?0x7f000001:(int32_t)netPeerAddress(itemCount);}
int32_t jnetClose(int32_t fileHandle){int itemCount=externalNumber(fileHandle);if(itemCount>=0){closeNetwork(itemCount);external[fileHandle-32]=0;}if(fileHandle>=32&&fileHandle<40)udpExternalPeer[fileHandle-32]=boundAddress[fileHandle-32]=0;return jloopnetClose(fileHandle);}
int32_t jstreamCreate(void){return jloopstreamCreate();}
int32_t jstreamBind(int32_t fileHandle,int32_t InternetAddress,int32_t portNumber){
    if(InternetAddress==0||InternetAddress==0x7f000001){int returnedValue=jloopstreamBind(fileHandle,InternetAddress,portNumber);if(!returnedValue)anyAddress[fileHandle-32]=InternetAddress==0;return returnedValue;}
    if(InternetAddress!=readNetworkStatus(0,0))return -99;int returnedValue=jloopstreamBind(fileHandle,0,portNumber);if(returnedValue<0)return returnedValue;
    int itemCount=pasteText(fileHandle,1);return itemCount<0?itemCount:netBind(itemCount,InternetAddress,jloopstreamPort(fileHandle));
}
int32_t jstreamListen(int32_t fileHandle,int32_t backlog){
    int itemCount=externalNumber(fileHandle);if(itemCount<0){int returnedValue=jloopstreamListen(fileHandle,backlog);if(returnedValue<0||!anyAddress[fileHandle-32])return returnedValue;
        itemCount=pasteText(fileHandle,1);if(itemCount<0)return itemCount;returnedValue=netBind(itemCount,readNetworkStatus(0,0),jloopstreamPort(fileHandle));if(returnedValue<0)return returnedValue;dualListener[fileHandle-32]=1;
    }return backlog<1?-22:netListen(itemCount);
}
int32_t jstreamConnect(int32_t fileHandle,int32_t InternetAddress,int32_t portNumber){
    if(InternetAddress==0x7f000001 && externalNumber(fileHandle)<0)return jloopstreamConnect(fileHandle,InternetAddress,portNumber);
    if(jloopstreamPort(fileHandle)<0)return -9;int itemCount=pasteText(fileHandle,1);return itemCount<0?itemCount:netConnect(itemCount,InternetAddress,portNumber);
}
int32_t jstreamAccept(int32_t fileHandle){
    int itemCount=externalNumber(fileHandle);if(itemCount<0)return jloopstreamAccept(fileHandle);
    if(dualListener[fileHandle-32]){int local=jloopstreamAccept(fileHandle);if(local!=-11)return local;}
    int peerValue=netAccept(itemCount);if(peerValue<0)return peerValue;
    int targetValue=jloopstreamCreate();if(targetValue<0){closeNetwork(peerValue);return targetValue;}external[targetValue-32]=peerValue+1;return targetValue;
}
int32_t jstreamRead(int32_t fileHandle,int32_t size){
    int itemCount=externalNumber(fileHandle);if(itemCount<0)return jloopstreamRead(fileHandle,size);if(size<0||size>512)return -22;
    unsigned char data[512];int returnedValue=netRead(itemCount,data,size);for(int ordinalIndex=0;ordinalIndex<returnedValue;ordinalIndex++)jnetPut(ordinalIndex,data[ordinalIndex]);return returnedValue;
}
int32_t jstreamWrite(int32_t fileHandle,int32_t size){
    int itemCount=externalNumber(fileHandle);if(itemCount<0)return jloopstreamWrite(fileHandle,size);if(size<0||size>512)return -22;
    unsigned char data[512];for(int ordinalIndex=0;ordinalIndex<size;ordinalIndex++)data[ordinalIndex]=jnetGet(ordinalIndex);return netWrite(itemCount,data,size);
}
int32_t jstreamPort(int32_t fileHandle){int itemCount=externalNumber(fileHandle);return itemCount<0?jloopstreamPort(fileHandle):(int32_t)networkPortNumber(itemCount);}
int32_t jstreamPeer(int32_t fileHandle){int itemCount=externalNumber(fileHandle);return itemCount<0?jloopstreamPeer(fileHandle):(int32_t)peerPortNumber(itemCount);}
int32_t jstreamAddress(int32_t fileHandle){return externalNumber(fileHandle)<0?0x7f000001:dualListener[fileHandle-32]?0:readNetworkStatus(0,0);}
int32_t jstreamClose(int32_t fileHandle){int itemCount=externalNumber(fileHandle);if(itemCount>=0){closeNetwork(itemCount);external[fileHandle-32]=0;}if(fileHandle>=40&&fileHandle<56)anyAddress[fileHandle-32]=dualListener[fileHandle-32]=0;return jloopstreamClose(fileHandle);}
