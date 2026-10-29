#include "../naming/machineLinkNames.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "networkStack.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../remoteValue/remoteValue.h"
#include "wiredNetwork.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define machineRegister(firstValue) (*(volatile uint32_t *)(uintptr_t)(firstValue))
#define auxiliaryDevice 0xfe215000ul
extern uintptr_t boardMillis(void);
static struct netif connectionDevice;
static int isPrepared, polling;
static int useWiredNetwork;
static unsigned receiveUsage, receiveEscape, receiveError;
static unsigned char receiveDataBuffer[1600];
static unsigned char transmitData[32768];
static unsigned txHead, txCount;
static uint32_t receivedDatagramCount, sentDatagramCount, receivedByteCount, sentByteCount, droppedDatagramCount;
typedef struct {
    int typeCategory, receivePort, isPending, connected, fileEnd, error;
    struct tcp_pcb *connectionControl;
    struct udp_pcb *datagramControl;
    unsigned frontEntry, entryCount;
    unsigned char data[4096];
    unsigned lengths[4], ports[4], peerEndpointNumber;
    uint32_t addresses[4], peerAddress;
} socketEndpoint;
static socketEndpoint socketEndpoints[32];
u32_t sys_now(void) { return (u32_t)boardMillis(); }
static int errorNumber(err_t auxiliaryEntry) {
    return auxiliaryEntry == ERR_MEM || auxiliaryEntry == ERR_BUF || auxiliaryEntry == ERR_WOULDBLOCK ? -11 : auxiliaryEntry == ERR_USE ? -98 :
        auxiliaryEntry == ERR_RTE ? -101 : auxiliaryEntry == ERR_RST ? -104 : auxiliaryEntry == ERR_CONN ? -107 : auxiliaryEntry == ERR_TIMEOUT ? -110 : -5;
}
static socketEndpoint *getValue(int fileHandle) { return fileHandle >= 0 && fileHandle < 32 && socketEndpoints[fileHandle].typeCategory ? &socketEndpoints[fileHandle] : 0; }
static int reserve(int typeCategory) {
    for (int ordinalIndex = 0; ordinalIndex < 32; ++ordinalIndex) if (!socketEndpoints[ordinalIndex].typeCategory) {
        memset(&socketEndpoints[ordinalIndex], 0, sizeof(socketEndpoint)); socketEndpoints[ordinalIndex].typeCategory = typeCategory; socketEndpoints[ordinalIndex].isPending = -1; return ordinalIndex;
    }
    return -24;
}
static void emitValue(unsigned characterCode) { transmitData[(txHead + txCount++) % sizeof(transmitData)] = characterCode; }
static err_t output(struct netif *itemCount, struct pbuf *dataPosition, const ip4_addr_t *address) {
    (void)itemCount; (void)address;
    if (dataPosition->tot_len > 1500 || txCount + 2 * dataPosition->tot_len + 2 > sizeof(transmitData)) return ERR_MEM;
    emitValue(192);
    for (struct pbuf *nextOffset = dataPosition; nextOffset; nextOffset = nextOffset->next) for (unsigned ordinalIndex = 0; ordinalIndex < nextOffset->len; ordinalIndex++) {
        unsigned characterCode = ((unsigned char *)nextOffset->payload)[ordinalIndex];
        if (characterCode == 192 || characterCode == 219) { emitValue(219); emitValue(characterCode == 192 ? 220 : 221); } else emitValue(characterCode);
    }
    emitValue(192); sentDatagramCount++; sentByteCount += dataPosition->tot_len; return ERR_OK;
}
static err_t prepareRuntime(struct netif *itemCount) { itemCount->name[0] = 's'; itemCount->name[1] = 'l'; itemCount->mtu = 1500; itemCount->output = output; return ERR_OK; }
void prepareNetwork(void) {
    if (isPrepared) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    machineRegister(auxiliaryDevice + 4) |= 1; machineRegister(auxiliaryDevice + 0x60) = 0; machineRegister(auxiliaryDevice + 0x44) = 0;
    machineRegister(auxiliaryDevice + 0x48) = 0xc6; machineRegister(auxiliaryDevice + 0x4c) = 3; machineRegister(auxiliaryDevice + 0x68) = 270; machineRegister(auxiliaryDevice + 0x60) = 3;
    lwip_init();
    ip4_addr_t InternetAddress, bitMask, gatewayAddress;
    useWiredNetwork=hasWiredDevice();
    ip4_addr_set_u32(&InternetAddress, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitMask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gatewayAddress, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&connectionDevice, &InternetAddress, &bitMask, &gatewayAddress, 0, useWiredNetwork?prepareWiredNetwork:prepareRuntime, useWiredNetwork?ethernet_input:ip4_input))return;
    netif_set_default(&connectionDevice); netif_set_up(&connectionDevice);if(!useWiredNetwork)netif_set_link_up(&connectionDevice); isPrepared = 1;
    prepareRemote();
}
static err_t hasReceived(void *additionalArguments, struct tcp_pcb *transmissionControlBlock, struct pbuf *dataPosition, err_t error) {
    socketEndpoint *stringData = additionalArguments; (void)transmissionControlBlock; (void)error;
    if (!dataPosition) { stringData->fileEnd = 1; return ERR_OK; }
    if (dataPosition->tot_len > sizeof(stringData->data) - stringData->entryCount) return ERR_MEM;
    unsigned currentPosition = (stringData->frontEntry + stringData->entryCount) % sizeof(stringData->data);
    for (struct pbuf *nextOffset = dataPosition; nextOffset; nextOffset = nextOffset->next) for (unsigned ordinalIndex = 0; ordinalIndex < nextOffset->len; ordinalIndex++) {
        stringData->data[currentPosition] = ((unsigned char *)nextOffset->payload)[ordinalIndex]; currentPosition = (currentPosition + 1) % sizeof(stringData->data);
    }
    stringData->entryCount += dataPosition->tot_len; pbuf_free(dataPosition); return ERR_OK;
}
static void hasFailed(void *additionalArguments, err_t error) { socketEndpoint *stringData = additionalArguments; stringData->connectionControl = 0; stringData->error = errorNumber(error); }
static void callbacks(socketEndpoint *stringData) { tcp_arg(stringData->connectionControl, stringData); tcp_recv(stringData->connectionControl, hasReceived); tcp_err(stringData->connectionControl, hasFailed); }
static err_t connected(void *additionalArguments, struct tcp_pcb *transmissionControlBlock, err_t error) {
    socketEndpoint *stringData = additionalArguments; (void)transmissionControlBlock; if (error) stringData->error = errorNumber(error); else stringData->connected = 1; return ERR_OK;
}
static err_t accepted(void *additionalArguments, struct tcp_pcb *transmissionControlBlock, err_t error) {
    socketEndpoint *parent = additionalArguments; if (error) return error;
    int fileHandle = reserve(1); if (fileHandle < 0) return ERR_MEM;
    socketEndpoint *stringData = &socketEndpoints[fileHandle]; stringData->connectionControl = transmissionControlBlock; stringData->connected = 1; stringData->isPending = (int)(parent - socketEndpoints);
    stringData->peerAddress = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmissionControlBlock->remote_ip))); stringData->peerEndpointNumber = transmissionControlBlock->remote_port;
    callbacks(stringData); return ERR_OK;
}
static void datagram(void *additionalArguments, struct udp_pcb *transmissionControlBlock, struct pbuf *dataPosition, const ip_addr_t *address, u16_t portNumber) {
    socketEndpoint *stringData = additionalArguments; (void)transmissionControlBlock;
    if (stringData->entryCount < 4 && dataPosition->tot_len <= 512) {
        unsigned positionIndex = (stringData->frontEntry + stringData->entryCount) % 4;
        pbuf_copy_partial(dataPosition, stringData->data + positionIndex * 512, dataPosition->tot_len, 0);
        stringData->lengths[positionIndex] = dataPosition->tot_len; stringData->ports[positionIndex] = portNumber;
        stringData->addresses[positionIndex] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(address))); stringData->entryCount++;
    }
    pbuf_free(dataPosition);
}
int createSocketEndpoint(int typeCategory) {
    if (!isPrepared) return -100;
    if (typeCategory != 1 && typeCategory != 2) return -93;
    int fileHandle = reserve(typeCategory); if (fileHandle < 0) return fileHandle;
    socketEndpoint *stringData = &socketEndpoints[fileHandle];
    if (typeCategory == 1) { stringData->connectionControl = tcp_new(); if (stringData->connectionControl) callbacks(stringData); }
    else { stringData->datagramControl = udp_new(); if (stringData->datagramControl) udp_recv(stringData->datagramControl, datagram, stringData); }
    if (!stringData->connectionControl && !stringData->datagramControl) { stringData->typeCategory = 0; return -12; } return fileHandle;
}
int netBind(int fileHandle, uint32_t address, unsigned portNumber) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData) return -9;
    if (portNumber > 65535 || (address && address != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&connectionDevice))) && address != 0x7f000001)) return -99;
    ip_addr_t InternetAddress; ip_addr_set_ip4_u32(&InternetAddress, lwip_htonl(address));
    err_t auxiliaryEntry = stringData->typeCategory == 1 ? tcp_bind(stringData->connectionControl, &InternetAddress, portNumber) : udp_bind(stringData->datagramControl, &InternetAddress, portNumber); return auxiliaryEntry ? errorNumber(auxiliaryEntry) : 0;
}
void reuseSocketAddress(int fileHandle) { socketEndpoint *stringData = getValue(fileHandle); if (stringData && stringData->connectionControl) ip_set_option(stringData->connectionControl, SOF_REUSEADDR); }
int netListen(int fileHandle) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || stringData->typeCategory != 1) return -9;
    if (stringData->receivePort) return 0;
    err_t auxiliaryEntry; struct tcp_pcb *transmissionControlBlock = tcp_listen_with_backlog_and_err(stringData->connectionControl, 4, &auxiliaryEntry);
    if (!transmissionControlBlock) return errorNumber(auxiliaryEntry); stringData->connectionControl = transmissionControlBlock; stringData->receivePort = 1; tcp_arg(transmissionControlBlock, stringData); tcp_accept(transmissionControlBlock, accepted); return 0;
}
int netConnect(int fileHandle, uint32_t address, unsigned portNumber) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || stringData->typeCategory != 1) return -9;
    if (stringData->error) return stringData->error;
    if (stringData->connected) return 0;
    if (stringData->peerEndpointNumber) return -115;
    if (!portNumber || portNumber > 65535 || !address) return -22;
    ip_addr_t InternetAddress; ip_addr_set_ip4_u32(&InternetAddress, lwip_htonl(address));
    stringData->peerAddress = address; stringData->peerEndpointNumber = portNumber;
    err_t auxiliaryEntry = tcp_connect(stringData->connectionControl, &InternetAddress, portNumber, connected); return auxiliaryEntry ? errorNumber(auxiliaryEntry) : -115;
}
int netAccept(int fileHandle) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || !stringData->receivePort) return -22;
    for (int ordinalIndex = 0; ordinalIndex < 32; ordinalIndex++) if (socketEndpoints[ordinalIndex].typeCategory == 1 && socketEndpoints[ordinalIndex].isPending == fileHandle) { socketEndpoints[ordinalIndex].isPending = -1; return ordinalIndex; }
    return -11;
}
int netRead(int fileHandle, void *data, unsigned itemCount) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || stringData->typeCategory != 1) return -9;
    if (!itemCount) return 0; if (!stringData->entryCount) return stringData->error ? stringData->error : stringData->fileEnd ? 0 : -11;
    if (itemCount > stringData->entryCount) itemCount = stringData->entryCount;
    for (unsigned ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) { ((unsigned char *)data)[ordinalIndex] = stringData->data[stringData->frontEntry]; stringData->frontEntry = (stringData->frontEntry + 1) % sizeof(stringData->data); }
    stringData->entryCount -= itemCount; if (stringData->connectionControl) tcp_recved(stringData->connectionControl, itemCount); return itemCount;
}
int netWrite(int fileHandle, const void *data, unsigned itemCount) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || stringData->typeCategory != 1) return -9;
    if (stringData->error) return stringData->error; if (!stringData->connectionControl || !stringData->connected) return -107;
    if (!itemCount) return 0; if (itemCount > tcp_sndbuf(stringData->connectionControl)) itemCount = tcp_sndbuf(stringData->connectionControl);
    if (!itemCount) return -11; if (itemCount > 1024) itemCount = 1024;
    err_t auxiliaryEntry = tcp_write(stringData->connectionControl, data, itemCount, TCP_WRITE_FLAG_COPY); if (auxiliaryEntry) return errorNumber(auxiliaryEntry);
    tcp_output(stringData->connectionControl); return itemCount;
}
int sendDatagram(int fileHandle, const void *data, unsigned itemCount, uint32_t address, unsigned portNumber) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || stringData->typeCategory != 2) return -9;
    if (itemCount > 512) return -90; if (!portNumber || portNumber > 65535) return -22;
    struct pbuf *dataPosition = pbuf_alloc(PBUF_TRANSPORT, itemCount, PBUF_RAM); if (!dataPosition) return -11;
    pbuf_take(dataPosition, data, itemCount); ip_addr_t InternetAddress; ip_addr_set_ip4_u32(&InternetAddress, lwip_htonl(address));
    err_t auxiliaryEntry = udp_sendto(stringData->datagramControl, dataPosition, &InternetAddress, portNumber); pbuf_free(dataPosition); return auxiliaryEntry ? errorNumber(auxiliaryEntry) : (int)itemCount;
}
int receiveDatagram(int fileHandle, void *data, unsigned itemCount) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData || stringData->typeCategory != 2) return -9;
    if (!stringData->entryCount) return -11; unsigned currentPosition = stringData->frontEntry;
    if (itemCount > stringData->lengths[currentPosition]) itemCount = stringData->lengths[currentPosition]; memcpy(data, stringData->data + currentPosition * 512, itemCount);
    stringData->peerEndpointNumber = stringData->ports[currentPosition]; stringData->peerAddress = stringData->addresses[currentPosition]; stringData->frontEntry = (currentPosition + 1) % 4; stringData->entryCount--; return itemCount;
}
unsigned networkPortNumber(int fileHandle) { socketEndpoint *stringData = getValue(fileHandle); return !stringData ? 0 : stringData->connectionControl ? stringData->connectionControl->local_port : stringData->datagramControl ? stringData->datagramControl->local_port : 0; }
unsigned peerPortNumber(int fileHandle) { socketEndpoint *stringData = getValue(fileHandle); return stringData ? stringData->peerEndpointNumber : 0; }
uint32_t netPeerAddress(int fileHandle) { socketEndpoint *stringData = getValue(fileHandle); return stringData ? stringData->peerAddress : 0; }
void closeNetwork(int fileHandle) {
    socketEndpoint *stringData = getValue(fileHandle); if (!stringData) return;
    if (stringData->receivePort) for (int ordinalIndex = 0; ordinalIndex < 32; ++ordinalIndex) if (socketEndpoints[ordinalIndex].typeCategory && socketEndpoints[ordinalIndex].isPending == fileHandle) closeNetwork(ordinalIndex);
    if (stringData->connectionControl) {
        tcp_arg(stringData->connectionControl, 0); if (stringData->receivePort) tcp_accept(stringData->connectionControl, 0); else { tcp_recv(stringData->connectionControl, 0); tcp_err(stringData->connectionControl, 0); }
        if (tcp_close(stringData->connectionControl) != ERR_OK) tcp_abort(stringData->connectionControl);
    }
    if (stringData->datagramControl) udp_remove(stringData->datagramControl); stringData->typeCategory = 0;
}
void inspectNetwork(void) {
    if (!isPrepared || polling) return; polling = 1;
    if(useWiredNetwork)inspectWiredNetwork(&connectionDevice);
    for (unsigned budget = 0; !useWiredNetwork && budget < 4096 && (machineRegister(auxiliaryDevice + 0x54) & 1); budget++) {
        unsigned characterCode = machineRegister(auxiliaryDevice + 0x40) & 255;
        if (characterCode == 192) {
            if (receiveUsage && !receiveError && !receiveEscape) {
                struct pbuf *dataPosition = pbuf_alloc(PBUF_RAW, receiveUsage, PBUF_POOL);
                if (dataPosition) { receivedDatagramCount++; receivedByteCount += receiveUsage; pbuf_take(dataPosition, receiveDataBuffer, receiveUsage); if (connectionDevice.input(dataPosition, &connectionDevice) != ERR_OK) { droppedDatagramCount++; pbuf_free(dataPosition); } }
                else droppedDatagramCount++;
            }
            else if (receiveUsage) droppedDatagramCount++;
            receiveUsage = receiveError = receiveEscape = 0;
        } else if (characterCode == 219 && !receiveEscape) receiveEscape = 1;
        else {
            if (receiveEscape) { if (characterCode != 220 && characterCode != 221) receiveError = 1; characterCode = characterCode == 220 ? 192 : 219; receiveEscape = 0; }
            if (receiveUsage < sizeof(receiveDataBuffer)) receiveDataBuffer[receiveUsage++] = characterCode; else receiveError = 1;
        }
    }
    netif_poll(&connectionDevice); sys_check_timeouts(); inspectFileTransfer(); inspectRemote();
    for (unsigned budget = 0; budget < 4096 && txCount && (machineRegister(auxiliaryDevice + 0x54) & 0x20); budget++) {
        machineRegister(auxiliaryDevice + 0x40) = transmitData[txHead]; txHead = (txHead + 1) % sizeof(transmitData); txCount--;
    }
    polling = 0;
}

/* settings·조회는 lwIP의 actualData 인터페이스와 endPoint 표를 사용한다. */
uint32_t readNetworkStatus(unsigned entryValue, unsigned index) {
    if(entryValue==20)return useWiredNetwork;
    if(entryValue==21)return isPrepared&&netif_is_link_up(&connectionDevice);
    if(entryValue==22)return useWiredNetwork?wiredNetworkStatistics(5):0;
    if (!isPrepared) return 0;
    if(useWiredNetwork&&entryValue>=4&&entryValue<=8)return wiredNetworkStatistics(entryValue-4);
    if (entryValue == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&connectionDevice)));
    if (entryValue == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&connectionDevice)));
    if (entryValue == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&connectionDevice)));
    if (entryValue == 3) return netif_is_up(&connectionDevice) != 0;
    if (entryValue == 4) return receivedDatagramCount;
    if (entryValue == 5) return sentDatagramCount;
    if (entryValue == 6) return receivedByteCount;
    if (entryValue == 7) return sentByteCount;
    if (entryValue == 8) return droppedDatagramCount;
    if (entryValue == 9) return txCount;
    if (index >= 32) return 0;
    socketEndpoint *endPoint = &socketEndpoints[index];
    if (entryValue == 10) return endPoint->typeCategory;
    if (!endPoint->typeCategory) return 0;
    if (entryValue == 11) return networkPortNumber(index);
    if (entryValue == 12) return endPoint->peerAddress;
    if (entryValue == 13) return endPoint->peerEndpointNumber;
    if (entryValue == 14) return endPoint->receivePort ? 1 : endPoint->fileEnd ? 3 : endPoint->error ? 4 : endPoint->connected ? 2 : 0;
    if (entryValue == 15) return endPoint->entryCount;
    if (entryValue == 16) {
        const ip_addr_t *address = endPoint->typeCategory == 1 && endPoint->connectionControl ? &endPoint->connectionControl->local_ip :
            endPoint->typeCategory == 2 && endPoint->datagramControl ? &endPoint->datagramControl->local_ip : 0;
        return address ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(address))) : 0;
    }
    return 0;
}

int configureNetwork(unsigned action, uint32_t address, uint32_t maskValue, uint32_t gatewayValue) {
    if (!isPrepared) return -100;
    if (action == 1) { netif_set_up(&connectionDevice); return 0; }
    if (action == 2) { netif_set_down(&connectionDevice); return 0; }
    if (action != 0) return -22;
    /* 유니캐스트 IPv4, denseSwitchCases maskValue, 같은 망의 선택적 defaultValue gatewayValue. */
    uint32_t invertedMask = ~maskValue;
    if (!maskValue || (invertedMask & (invertedMask + 1)) || !address || (address >> 24) == 127 ||
        (address >> 24) == 0 || (address >> 28) >= 14 ||
        (invertedMask > 1 && (!(address & invertedMask) || (address & invertedMask) == invertedMask)) ||
        (gatewayValue && ((gatewayValue & maskValue) != (address & maskValue) || gatewayValue == address || (gatewayValue >> 28) >= 14 ||
         (invertedMask > 1 && (!(gatewayValue & invertedMask) || (gatewayValue & invertedMask) == invertedMask))))) return -22;
    /* 기존 연결을 address 변경으로 몰래 끊지 않는다. */
    for (unsigned index = 0; index < 32; index++) if (socketEndpoints[index].typeCategory &&
        !(socketEndpoints[index].receivePort && socketEndpoints[index].connectionControl && ip_addr_isany(&socketEndpoints[index].connectionControl->local_ip))) return -16;
    if(useWiredNetwork)dhcp_stop(&connectionDevice);
    ip4_addr_t newAddress, newMask, newGatewayValue;
    ip4_addr_set_u32(&newAddress, lwip_htonl(address)); ip4_addr_set_u32(&newMask, lwip_htonl(maskValue)); ip4_addr_set_u32(&newGatewayValue, lwip_htonl(gatewayValue));
    netif_set_addr(&connectionDevice, &newAddress, &newMask, &newGatewayValue);
    return 0;
}

static struct raw_pcb *responseEndpoint;
static uint32_t testAddress, testTime, responseTime;
static unsigned testSequence, testIdentifier, responseSequence;
static int responseState;
static u8_t hasResponse(void *arguments, struct raw_pcb *endPoint, struct pbuf *data, const ip_addr_t *address) {
    (void)arguments; (void)endPoint;
    unsigned char headValue[20], reply[16];
    if (responseState != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(address))) != testAddress || pbuf_copy_partial(data, headValue, 20, 0) != 20) return 0;
    unsigned headerSize = (headValue[0] & 15) * 4;
    if ((headValue[0] >> 4) != 4 || headerSize < 20 || data->tot_len < headerSize + 16 ||
        pbuf_copy_partial(data, reply, 16, headerSize) != 16 || reply[0] || reply[1] ||
        (((unsigned)reply[4] << 8) | reply[5]) != testIdentifier ||
        (((unsigned)reply[6] << 8) | reply[7]) != testSequence ||
        reply[8] != 'J' || reply[9] != 'K' || reply[10] != 'O' || reply[11] != 'S' ||
        (((uint32_t)reply[12] << 24) | ((uint32_t)reply[13] << 16) | ((uint32_t)reply[14] << 8) | reply[15]) != testTime) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, headerSize)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, headerSize); return 0; }
    responseTime = (uint32_t)boardMillis() - testTime; responseSequence = headValue[8]; responseState = 0;
    pbuf_free(data); return 1;
}
int startResponseTest(uint32_t address, unsigned orderValue) {
    if (!isPrepared || !netif_is_up(&connectionDevice)) return -100;
    if (!address || (address >> 28) >= 14 || address == 0xffffffffu) return -22;
    if (!responseEndpoint) { responseEndpoint = raw_new(IP_PROTO_ICMP); if (!responseEndpoint) return -12; raw_recv(responseEndpoint, hasResponse, 0); }
    testAddress = address; testSequence = orderValue & 65535; testIdentifier = (testIdentifier + 1) & 65535;
    testTime = boardMillis(); responseState = -11; responseTime = responseSequence = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = testIdentifier >> 8; data[5] = testIdentifier; data[6] = testSequence >> 8; data[7] = testSequence;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=testTime >> 24; data[13]=testTime >> 16; data[14]=testTime >> 8; data[15]=testTime;
    for (unsigned positionIndex = 16; positionIndex < sizeof(data); positionIndex++) data[positionIndex] = positionIndex;
    uint16_t verificationChecksum = inet_chksum(data, sizeof(data)); memcpy(data + 2, &verificationChecksum, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, data, sizeof(data)); ip_addr_t destinationEndpoint; ip_addr_set_ip4_u32(&destinationEndpoint, lwip_htonl(address));
    err_t processedValue = raw_sendto(responseEndpoint, datagram, &destinationEndpoint); pbuf_free(datagram);
    if (processedValue) responseState = errorNumber(processedValue);
    return processedValue ? responseState : 0;
}
int readResponseTest(unsigned entryValue) {
    inspectNetwork();
    return entryValue == 0 ? responseState : entryValue == 1 ? (int)responseTime : entryValue == 2 ? (int)responseSequence : -22;
}
