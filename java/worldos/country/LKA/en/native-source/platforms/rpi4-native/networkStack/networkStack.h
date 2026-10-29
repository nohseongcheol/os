#ifndef nativeNetworkHeader
#define nativeNetworkHeader
#include <stdint.h>
#include <stddef.h>
void prepareNetwork(void);
void inspectNetwork(void);
int createSocketEndpoint(int typeCategory);
int netBind(int fileHandle, uint32_t address, unsigned portNumber);
int netListen(int fileHandle);
void reuseSocketAddress(int fileHandle);
int netConnect(int fileHandle, uint32_t address, unsigned portNumber);
int netAccept(int fileHandle);
int netRead(int fileHandle, void *data, unsigned itemCount);
int netWrite(int fileHandle, const void *data, unsigned itemCount);
int sendDatagram(int fileHandle, const void *data, unsigned itemCount, uint32_t address, unsigned portNumber);
int receiveDatagram(int fileHandle, void *data, unsigned itemCount);
unsigned networkPortNumber(int fileHandle);
unsigned peerPortNumber(int fileHandle);
uint32_t netPeerAddress(int fileHandle);
void closeNetwork(int fileHandle);
int fileTransferControl(int action);
void inspectFileTransfer(void);
uint32_t readNetworkStatus(unsigned entryValue, unsigned index);
int configureNetwork(unsigned action, uint32_t address, uint32_t maskValue, uint32_t gatewayValue);
int startResponseTest(uint32_t address, unsigned orderValue);
int readResponseTest(unsigned entryValue);
#endif
