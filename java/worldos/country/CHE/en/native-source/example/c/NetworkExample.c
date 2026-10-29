#include "ExampleABI.h"
#include <NetworkABI.h>
int main(int argumentCount,char **arguments) {
    if(argumentCount!=2)return Output("사용법: ./네트워크 UDP창구번호\n");
    unsigned portValue=0;for(int number=0;arguments[1][number];number++) {
        if(arguments[1][number]<'0'||arguments[1][number]>'9')return 2;
        portValue=portValue*10+arguments[1][number]-'0';if(portValue>65535)return 2;
    }
    if(!portValue)return 2;
    int endpoint=createEndpoint(InternetFamily,DatagramSocket,DatagramProtocol);if(endpoint<0)return 3;
    struct InternetSocketAddress address={0};address.addressFamily=InternetFamily;
    if(bindAddress(endpoint,(struct SocketAddress *)&address,sizeof(address))<0)return 4;
    address.portNumber=networkShort(portValue);address.InternetAddress.addressValue=networkInteger(0x0a000202);
    const char datagram[]="C UDP en";
    if(sendDatagramData(endpoint,datagram,sizeof(datagram)-1,0,(struct SocketAddress *)&address,sizeof(address))!=sizeof(datagram)-1)return 5;
    char reply[512];unsigned run=milliseconds();int receivedCount;
    do {
        receivedCount=receiveDatagramData(endpoint,reply,sizeof(reply),0,0,0);
        if(receivedCount<0&&errorNumber!=TryAgainError)return 6;
    } while(receivedCount<0&&(unsigned)(milliseconds()-run)<700);
    closeFile(endpoint);if(receivedCount!=sizeof(datagram)-1)return 7;
    for(int number=0;number<receivedCount;number++)if(datagram[number]!=reply[number])return 8;
    return Output("C 네트워크 verify: UDP en\n");
}
