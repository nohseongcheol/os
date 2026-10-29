#include "NetworkABI.h"
static InternetSocketAddress address(unsigned portValue) {
    InternetSocketAddress value = {}; value.addressFamily = InternetFamily;
    value.portNumber = networkShort(portValue); value.InternetAddress.addressValue = networkInteger(loopbackAddress); return value;
}
extern "C" int startUserProgram(int) {
    int sendingEndpoint = createEndpoint(InternetFamily, DatagramSocket, 0);
    int receiverEndpoint = createEndpoint(InternetFamily, DatagramSocket, DatagramProtocol);
    if (sendingEndpoint < 0 || receiverEndpoint < 0) return 1;
    InternetSocketAddress arrivalValue = address(7777), departureValue = address(7778), sentAddress = {};
    socketAddressLengthType addressLength = sizeof(sentAddress);
    if (bindAddress(receiverEndpoint, (SocketAddress *)&arrivalValue, sizeof(arrivalValue))) return 2;
    if (bindAddress(sendingEndpoint, (SocketAddress *)&arrivalValue, sizeof(arrivalValue)) != -1 || errorNumber != 98) return 3;
    if (bindAddress(sendingEndpoint, (SocketAddress *)&departureValue, sizeof(departureValue))) return 4;
    static const char contentValue[] = "한글 UDP loopback 😀";
    char receivedValue[64] = {};
    if (sendDatagramData(sendingEndpoint, contentValue, sizeof(contentValue), 0, (SocketAddress *)&arrivalValue, sizeof(arrivalValue)) != sizeof(contentValue)) return 5;
    if (receiveDatagramData(receiverEndpoint, (void *)contentValue, sizeof(contentValue), 0, 0, 0) != -1 || errorNumber != 14) return 6;
    if (receiveDatagramData(receiverEndpoint, receivedValue, sizeof(receivedValue), 0, (SocketAddress *)&sentAddress, &addressLength) != sizeof(contentValue)) return 7;
    if (addressLength != sizeof(sentAddress) || deviceOrderShort(sentAddress.portNumber) != 7778 || deviceOrderInteger(sentAddress.InternetAddress.addressValue) != loopbackAddress) return 8;
    for (unsigned ordinalIndex = 0; ordinalIndex < sizeof(contentValue); ordinalIndex++) if (receivedValue[ordinalIndex] != contentValue[ordinalIndex]) return 9;
    if (receiveDatagramData(receiverEndpoint, receivedValue, sizeof(receivedValue), 0, 0, 0) != -1 || errorNumber != 11) return 10;
    if (sendDatagramData(receiverEndpoint, receivedValue, sizeof(contentValue), 0, (SocketAddress *)&sentAddress, sizeof(sentAddress)) != sizeof(contentValue)) return 11;
    if (receiveDatagramData(sendingEndpoint, receivedValue, 4, 0, 0, 0) != 4) return 12;
    if (receiveDatagramData(sendingEndpoint, receivedValue, 4, 0, 0, 0) != -1 || errorNumber != 11) return 13;
    for (int ordinalIndex = 0; ordinalIndex < 4; ordinalIndex++) if (sendDatagramData(sendingEndpoint, contentValue, sizeof(contentValue), 0, (SocketAddress *)&arrivalValue, sizeof(arrivalValue)) != sizeof(contentValue)) return 14;
    if (sendDatagramData(sendingEndpoint, contentValue, sizeof(contentValue), 0, (SocketAddress *)&arrivalValue, sizeof(arrivalValue)) != -1 || errorNumber != 11) return 15;
    for (int ordinalIndex = 0; ordinalIndex < 4; ordinalIndex++) if (receiveDatagramData(receiverEndpoint, receivedValue, sizeof(receivedValue), 0, 0, 0) != sizeof(contentValue)) return 16;
    if (sendDatagramData(sendingEndpoint, 0, 0, 0, (SocketAddress *)&arrivalValue, sizeof(arrivalValue)) != 0 ||
        receiveDatagramData(receiverEndpoint, 0, 0, 0, 0, 0) != 0) return 21;
    arrivalValue.InternetAddress.addressValue = networkInteger(0x08080808);
    if (sendDatagramData(sendingEndpoint, contentValue, sizeof(contentValue), 0, (SocketAddress *)&arrivalValue, sizeof(arrivalValue)) != -1 || errorNumber != 101) return 17;
    if (createEndpoint(InternetFamily, StreamNetwork, DatagramProtocol) != -1 || errorNumber != 93) return 18;
    addressLength = sizeof(sentAddress);
    if (readSocketAddress(receiverEndpoint, (SocketAddress *)&sentAddress, &addressLength) || deviceOrderShort(sentAddress.portNumber) != 7777) return 19;
    if (closeFile(receiverEndpoint) || closeFile(receiverEndpoint) != -1 || errorNumber != 9) return 20;
    // 보내는곳은 열어 둔다: exitProgram 시 프로세스별 socket 정리를 검사한다.
    static const char isComplete[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    writeFileData(1, isComplete, sizeof(isComplete) - 1);
    return 0;
}
