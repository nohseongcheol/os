#include "NetworkABI.h"

int startUserProgram(int arguments) {
    (void)arguments;
    struct InternetSocketAddress address = {0};
    address.addressFamily = InternetFamily;
    address.portNumber = networkShort(9260);
    address.InternetAddress.addressValue = networkInteger(loopbackAddress);
    int serverValue = createEndpoint(InternetFamily, StreamNetwork, streamTransportProtocol);
    if (serverValue < 0 || bindAddress(serverValue, (struct SocketAddress *)&address, sizeof(address)) < 0 ||
        waitForNetworkConnection(serverValue, 4) < 0) return 1;
    if (acceptNetworkConnection(serverValue, 0, 0) != -1 || errorNumber != 11) return 2;
    int guestValue = createEndpoint(InternetFamily, StreamNetwork, streamTransportProtocol);
    if (guestValue < 0 || connectNetwork(guestValue, (struct SocketAddress *)&address, sizeof(address)) < 0) return 3;
    int connect = acceptNetworkConnection(serverValue, 0, 0);
    if (connect < 0) return 4;
    unsigned char itemToSend[1500], receivedItem[1500];
    for (int number = 0; number < 1500; number++) itemToSend[number] = (unsigned char)number;
    int sentCount = 0;
    while (sentCount < 1024) {
        int lengthValue = writeFileData(guestValue, itemToSend + sentCount, sizeof(itemToSend) - sentCount);
        if (lengthValue <= 0) return 5;
        sentCount += lengthValue;
    }
    if (writeFileData(guestValue, itemToSend, 1) != -1 || errorNumber != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 buildAll 읽은 backValue EOF가 된다. */
    closeFile(guestValue);
    int receivedCount = 0;
    while (receivedCount < sentCount) {
        int lengthValue = readFileData(connect, receivedItem + receivedCount, sizeof(receivedItem) - receivedCount);
        if (lengthValue <= 0) return 7;
        receivedCount += lengthValue;
    }
    for (int number = 0; number < receivedCount; number++) if (receivedItem[number] != itemToSend[number]) return 8;
    if (readFileData(connect, receivedItem, 1) != 0) return 9;
    if (writeFileData(connect, itemToSend, 1) != -1 || errorNumber != 32) return 10;
    closeFile(connect); closeFile(serverValue);
    const char result[] = "C posix-kor 연결형 communication PASS\n";
    writeFileData(1, result, sizeof(result) - 1);
    return 0;
}
