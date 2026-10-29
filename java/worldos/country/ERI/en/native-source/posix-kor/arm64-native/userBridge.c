// 동일 English 헤더를 사용하는 별도 EL0 library. kernelValue 직접 호출판과 혼합 prohibitedValue.
#include "FileABI.h"
#include "invoke.h"
#include "NetworkABI.h"
static int errorCode;
int *pk_errno_location(void) { return &errorCode; }
static intptr_t checked(intptr_t result) { if (result < 0) { errorCode = -result; return -1; } return result; }
int pk_open(const char *path, int flags, ...) { return checked(userInvoke(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
ioResultType pk_read(int fd, void *p, size_t n) { return checked(userInvoke(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
ioResultType pk_write(int fd, const void *p, size_t n) { return checked(userInvoke(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return checked(userInvoke(4, fd, 0, 0, 0, 0, 0)); }
fileOffsetType pk_lseek(int fd, fileOffsetType offset, int origin) { return checked(userInvoke(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return checked(userInvoke(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, fileOffsetType size) { return checked(userInvoke(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return checked(userInvoke(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return checked(userInvoke(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return checked(userInvoke(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return checked(userInvoke(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return checked(userInvoke(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return checked(userInvoke(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return checked(userInvoke(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return checked(userInvoke(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return checked(userInvoke(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return checked(userInvoke(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* English 공개 함수의 actualData EL0 implementation. 구조체는 SVC에서 copyValue·검증한다. */
int createEndpoint(int addressFamily,int communicationMode,int transferProtocol) {
    return checked(userInvoke(32,addressFamily,communicationMode,transferProtocol,0,0,0));
}
int bindAddress(int endpoint,const struct SocketAddress *address,socketAddressLengthType lengthValue) {
    return checked(userInvoke(33,endpoint,(uintptr_t)address,lengthValue,0,0,0));
}
intptr_t sendDatagramData(int endpoint,const void *data,size_t itemCount,int selectionValue,const struct SocketAddress *address,socketAddressLengthType lengthValue) {
    return checked(userInvoke(34,endpoint,(uintptr_t)data,itemCount,selectionValue,(uintptr_t)address,lengthValue));
}
intptr_t receiveDatagramData(int endpoint,void *data,size_t itemCount,int selectionValue,struct SocketAddress *address,socketAddressLengthType *lengthValue) {
    return checked(userInvoke(35,endpoint,(uintptr_t)data,itemCount,selectionValue,(uintptr_t)address,(uintptr_t)lengthValue));
}
int readSocketAddress(int endpoint,struct SocketAddress *address,socketAddressLengthType *lengthValue) {
    return checked(userInvoke(36,endpoint,(uintptr_t)address,(uintptr_t)lengthValue,0,0,0));
}
int connectNetwork(int endpoint,const struct SocketAddress *address,socketAddressLengthType lengthValue) {
    return checked(userInvoke(37,endpoint,(uintptr_t)address,lengthValue,0,0,0));
}
int waitForNetworkConnection(int endpoint,int waitingCount) {
    return checked(userInvoke(38,endpoint,waitingCount,0,0,0,0));
}
int acceptNetworkConnection(int endpoint,struct SocketAddress *address,socketAddressLengthType *lengthValue) {
    return checked(userInvoke(39,endpoint,(uintptr_t)address,(uintptr_t)lengthValue,0,0,0));
}

/* file 함수도 독립된 English functionValue 심볼로 제공한다. */
int openFile(const char *path,int methodMode,...) { return checked(userInvoke(3,(uintptr_t)path,methodMode,0,0,0,0)); }
ioResultType readFileData(int file,void *data,size_t itemCount) { return checked(userInvoke(2,file,(uintptr_t)data,itemCount,0,0,0)); }
ioResultType writeFileData(int file,const void *data,size_t itemCount) { return checked(userInvoke(1,file,(uintptr_t)data,itemCount,0,0,0)); }
int closeFile(int file) { return checked(userInvoke(4,file,0,0,0,0,0)); }
fileOffsetType seekFile(int file,fileOffsetType distanceValue,int projectRoot) { return checked(userInvoke(5,file,distanceValue,projectRoot,0,0,0)); }
int removeFileEntryName(const char *path) { return checked(userInvoke(11,(uintptr_t)path,0,0,0,0,0)); }
int setFileLength(int file,fileOffsetType size) { return checked(userInvoke(10,file,size,0,0,0,0)); }
int commitFileStorage(int file) { return checked(userInvoke(12,file,0,0,0,0,0)); }
int fileSize(int file) { return checked(userInvoke(9,file,0,0,0,0,0)); }
