#include <NetworkABI.h>
#include <errno.h>
#include "CallBoundary.h"

int socket(int addressScheme, int networkKind, int contractNumber) {
    return invocationResult(jkoros_syscall(41, addressScheme, networkKind, contractNumber, 0, 0));
}
int bind(int fileDescriptor, const struct sockaddr *address, socklen_t addressLength) {
    return invocationResult(jkoros_syscall(42, fileDescriptor, (int)address, addressLength, 0, 0));
}
ssize_t sendto(int fileDescriptor, const void *data, size_t byteCount, int settings,
               const struct sockaddr *address, socklen_t addressLength) {
    int request[2] = {(int)address, addressLength};
    return invocationResult(jkoros_syscall(43, fileDescriptor, (int)data, byteCount, settings, (int)request));
}
ssize_t recvfrom(int fileDescriptor, void *data, size_t byteCount, int settings,
                 struct sockaddr *address, socklen_t *addressLength) {
    int request[2] = {(int)address, (int)addressLength};
    return invocationResult(jkoros_syscall(44, fileDescriptor, (int)data, byteCount, settings, (int)request));
}
int getsockname(int fileDescriptor, struct sockaddr *address, socklen_t *addressLength) {
    return invocationResult(jkoros_syscall(45, fileDescriptor, (int)address, (int)addressLength, 0, 0));
}
int setsockopt(int fileDescriptor, int layerValue, int settingsName, const void *value, socklen_t valueLength) {
    if (layerValue != SOL_SOCKET || settingsName != SO_RCVTIMEO) { errno = ENOPROTOOPT; return -1; }
    if (!value) { errno = EFAULT; return -1; }
    if (valueLength != sizeof(struct timeval)) { errno = EINVAL; return -1; }
    const struct timeval *timeValue = value;
    if (timeValue->tv_sec < 0 || timeValue->tv_sec > 2 || timeValue->tv_usec < 0 || timeValue->tv_usec >= 1000000) {
        errno = EINVAL; return -1;
    }
    int milliseconds = timeValue->tv_sec * 1000 + (timeValue->tv_usec + 999) / 1000;
    return invocationResult(jkoros_syscall(46, fileDescriptor, milliseconds, 0, 0, 0));
}
uint16_t htons(uint16_t value) { return (value << 8) | (value >> 8); }
uint16_t ntohs(uint16_t value) { return htons(value); }
uint32_t htonl(uint32_t value) {
    return (value << 24) | ((value << 8) & 0xff0000U) | ((value >> 8) & 0xff00U) | (value >> 24);
}
uint32_t ntohl(uint32_t value) { return htonl(value); }
int inet_pton(int addressScheme, const char *stringValue, void *address) {
    if (addressScheme != AF_INET) { errno = EAFNOSUPPORT; return -1; }
    if (!stringValue || !address) { errno = EFAULT; return -1; }
    unsigned char temporaryValue[4];
    for (int slotEntry = 0; slotEntry < 4; slotEntry++) {
        int value = 0, digits = 0;
        const char *run = stringValue;
        while (*stringValue >= '0' && *stringValue <= '9') {
            if (++digits > 3) return 0;
            value = value * 10 + *stringValue++ - '0';
        }
        if (!digits || value > 255 || (digits > 1 && *run == '0')) return 0;
        temporaryValue[slotEntry] = value;
        if (slotEntry < 3) { if (*stringValue++ != '.') return 0; }
        else if (*stringValue) return 0;
    }
    for (int slotEntry = 0; slotEntry < 4; slotEntry++) ((unsigned char *)address)[slotEntry] = temporaryValue[slotEntry];
    return 1;
}
const char *inet_ntop(int addressScheme, const void *address, char *stringValue, socklen_t capacityValue) {
    if (addressScheme != AF_INET) { errno = EAFNOSUPPORT; return 0; }
    if (!address || !stringValue) { errno = EFAULT; return 0; }
    const unsigned char *number = address;
    char temporaryValue[16]; unsigned int lengthValue = 0;
    for (int slotEntry = 0; slotEntry < 4; slotEntry++) {
        unsigned int value = number[slotEntry];
        if (value >= 100) temporaryValue[lengthValue++] = '0' + value / 100;
        if (value >= 10) temporaryValue[lengthValue++] = '0' + value / 10 % 10;
        temporaryValue[lengthValue++] = '0' + value % 10;
        if (slotEntry < 3) temporaryValue[lengthValue++] = '.';
    }
    temporaryValue[lengthValue++] = 0;
    if (capacityValue < lengthValue) { errno = ENOSPC; return 0; }
    for (unsigned int slotEntry = 0; slotEntry < lengthValue; slotEntry++) stringValue[slotEntry] = temporaryValue[slotEntry];
    return stringValue;
}
