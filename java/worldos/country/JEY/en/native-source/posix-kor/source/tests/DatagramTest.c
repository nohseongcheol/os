#include <FileABI.h>
#include <NetworkABI.h>
#include <string.h>
#include <stdio.h>

#define verify(condition) do { if (!(condition)) { puts("POSIX UDP CHECK FAILED: " #condition); return 1; } } while (0)
int main(int argumentsCount, char **argumentList) {
    verify(argumentsCount == 2);
    int portNumber = 0;
    for (int slotEntry = 0; argumentList[1][slotEntry]; slotEntry++) {
        verify(argumentList[1][slotEntry] >= '0' && argumentList[1][slotEntry] <= '9');
        portNumber = portNumber * 10 + argumentList[1][slotEntry] - '0';
        verify(portNumber <= 65535);
    }
    int endpointValue = createEndpoint(AF_INET, SOCK_DGRAM, 0);
    verify(endpointValue == 3);
    struct sockaddr_in localScope = {0}, peerValue = {0}, receivedAddress = {0};
    localScope.sin_family = AF_INET;
    socklen_t lengthValue = sizeof localScope;
    verify(readSocketAddress(endpointValue, (struct sockaddr *)&localScope, &lengthValue) == 0 && localScope.sin_port == 0);
    verify(bindAddress(endpointValue, (struct sockaddr *)&localScope, sizeof localScope) == 0);
    verify(readSocketAddress(endpointValue, (struct sockaddr *)&localScope, &lengthValue) == 0 && ntohs(localScope.sin_port) >= 49152);
    verify(bindAddress(endpointValue, (struct sockaddr *)&localScope, sizeof localScope) == -1 && errno == EINVAL);
    int secondOrdinal = socket(AF_INET, SOCK_DGRAM, 0);
    verify(bind(secondOrdinal, (struct sockaddr *)&localScope, sizeof localScope) == -1 && errno == EADDRINUSE);
    verify(close(secondOrdinal) == 0);
    secondOrdinal = dup(endpointValue);
    verify(close(endpointValue) == 0); endpointValue = secondOrdinal;
    peerValue.sin_family = AF_INET; peerValue.sin_port = networkShort(portNumber);
    verify(parseNetworkAddress(AF_INET, "10.0.2.2", &peerValue.sin_addr) == 1);
    struct timeval waitValue = {0, 200000};
    verify(changeNetworkSettings(endpointValue, SOL_SOCKET, SO_RCVTIMEO, &waitValue, sizeof waitValue) == 0);
    char data[32];
    verify(receiveDatagramData(endpointValue, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verify(sendDatagramData(endpointValue, "posix-udp", 9, 0, (struct sockaddr *)&peerValue, sizeof peerValue) == 9);
    lengthValue = sizeof receivedAddress;
    verify(recvfrom(endpointValue, (void *)0x00100000, 9, 0, NULL, NULL) == -1 && errno == EFAULT);
    verify(receiveDatagramData(endpointValue, data, sizeof data, 0, (struct sockaddr *)&receivedAddress, &lengthValue) == 9);
    verify(memcmp(data, "posix-udp", 9) == 0 && lengthValue == 16);
    verify(receivedAddress.sin_port == peerValue.sin_port && receivedAddress.sin_addr.s_addr == peerValue.sin_addr.s_addr);
    verify(sendto(endpointValue, "truncate", 8, 0, (struct sockaddr *)&peerValue, sizeof peerValue) == 8);
    verify(recvfrom(endpointValue, data, 3, 0, NULL, NULL) == 3 && memcmp(data, "tru", 3) == 0);
    verify(recvfrom(endpointValue, data, sizeof data, MSG_DONTWAIT, NULL, NULL) == -1 && errno == EAGAIN);
    verify(sendto(endpointValue, NULL, 0, 0, (struct sockaddr *)&peerValue, sizeof peerValue) == 0);
    verify(recvfrom(endpointValue, NULL, 0, 0, NULL, NULL) == 0);
    verify(recvfrom(endpointValue, data, sizeof data, 0, NULL, NULL) == -1 && errno == EAGAIN);
    verify(close(endpointValue) == 0);
    puts("POSIX UDP CHECK PASS");
    return 0;
}
