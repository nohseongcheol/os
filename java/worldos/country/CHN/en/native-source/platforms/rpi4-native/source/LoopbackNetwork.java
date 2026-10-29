// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Initial network layer: IPv4/UDP loopback within one kernel. External IP addresses return ENETUNREACH; this does not replace an Ethernet/IP packet driver. Eight endpoints, four datagrams per endpoint, 512 bytes per datagram. All calls are nonblocking. */
public final class LoopbackNetwork {
    static int[] useValue = new int[8];
    static int[] portValue = new int[8];
    static int[] address = new int[8];
    static int[] frontValue = new int[8];
    static int[] itemCount = new int[8];
    static int[] receivedPort = new int[8];
    static int[] lengthValue = new int[32];
    static int[] sentPort = new int[32];
    static int[] data = new int[32 * 512];
    static int[] forwardValue = new int[512];
    static int nextEndpoint = 49152;
    static int verify(int index) { return index >= 32 && index < 40 && useValue[index - 32] != 0 ? index - 32 : -1; }
    static boolean overlaps(int index) {
        for (int slotEntry = 0; slotEntry < 8; slotEntry++) if (useValue[slotEntry] != 0 && portValue[slotEntry] == index) return true;
        return false;
    }
    static int temporaryPort() {
        for (int attemptValue = 0; attemptValue < 16; attemptValue++) {
            int candidate = nextEndpoint++;
            if (nextEndpoint > 65535) nextEndpoint = 49152;
            if (!overlaps(candidate)) return candidate;
        }
        return -98;
    }
    public static int createEntry(int regionValue, int kindValue, int contractValue) {
        if (regionValue != 2) return -97;
        if (kindValue != 2 || (contractValue != 0 && contractValue != 17)) return -93;
        for (int slotEntry = 0; slotEntry < 8; slotEntry++) if (useValue[slotEntry] == 0) {
            useValue[slotEntry] = 1; portValue[slotEntry] = 0; address[slotEntry] = 0; frontValue[slotEntry] = 0; itemCount[slotEntry] = 0; receivedPort[slotEntry] = 0;
            return slotEntry + 32;
        }
        return -24;
    }
    public static int bindEndpoint(int index, int networkAddress, int endpointPortNumber) {
        int slotEntry = verify(index);
        if (slotEntry < 0) return -9;
        if (networkAddress != 0 && networkAddress != 0x7f000001) return -99;
        if (portValue[slotEntry] != 0 || endpointPortNumber < 0 || endpointPortNumber > 65535) return -22;
        if (endpointPortNumber == 0) endpointPortNumber = temporaryPort();
        if (endpointPortNumber < 0) return endpointPortNumber;
        if (overlaps(endpointPortNumber)) return -98;
        portValue[slotEntry] = endpointPortNumber; address[slotEntry] = networkAddress; return 0;
    }
    public static int putData(int index, int value) {
        if (index < 0 || index >= 512) return -22;
        forwardValue[index] = value & 255; return 0;
    }
    public static int readData(int index) { return index >= 0 && index < 512 ? forwardValue[index] : -22; }
    public static int send(int index, int networkAddress, int endpointPortNumber, int size) {
        int slotEntry = verify(index);
        if (slotEntry < 0) return -9;
        if (networkAddress != 0x7f000001) return -101;
        if (endpointPortNumber < 1 || endpointPortNumber > 65535) return -22;
        if (size < 0 || size > 512) return -90;
        if (portValue[slotEntry] == 0) {
            int result = bindEndpoint(index, 0x7f000001, 0);
            if (result < 0) return result;
        }
        int destinationValue = -1;
        for (int candidate = 0; candidate < 8; candidate++) if (useValue[candidate] != 0 && portValue[candidate] == endpointPortNumber) destinationValue = candidate;
        if (destinationValue < 0) return -111;
        if (itemCount[destinationValue] == 4) return -11;
        int positionIndex = destinationValue * 4 + (frontValue[destinationValue] + itemCount[destinationValue]) % 4;
        for (int byteValue = 0; byteValue < size; byteValue++) data[positionIndex * 512 + byteValue] = forwardValue[byteValue];
        lengthValue[positionIndex] = size; sentPort[positionIndex] = portValue[slotEntry]; itemCount[destinationValue]++;
        return size;
    }
    public static int receive(int index, int capacityValue) {
        int slotEntry = verify(index);
        if (slotEntry < 0) return -9;
        if (capacityValue < 0 || capacityValue > 512) return -22;
        if (itemCount[slotEntry] == 0) return -11;
        int positionIndex = slotEntry * 4 + frontValue[slotEntry];
        int size = lengthValue[positionIndex] < capacityValue ? lengthValue[positionIndex] : capacityValue;
        for (int byteValue = 0; byteValue < size; byteValue++) forwardValue[byteValue] = data[positionIndex * 512 + byteValue];
        receivedPort[slotEntry] = sentPort[positionIndex]; frontValue[slotEntry] = (frontValue[slotEntry] + 1) % 4; itemCount[slotEntry]--;
        return size;
    }
    public static int readEndpointPort(int index) { int slotEntry = verify(index); return slotEntry < 0 ? -9 : portValue[slotEntry]; }
    public static int readAddress(int index) { int slotEntry = verify(index); return slotEntry < 0 ? -9 : address[slotEntry]; }
    public static int senderEndpoint(int index) { int slotEntry = verify(index); return slotEntry < 0 ? -9 : receivedPort[slotEntry]; }
    public static int close(int index) {
        int slotEntry = verify(index); if (slotEntry < 0) return -9;
        useValue[slotEntry] = 0; itemCount[slotEntry] = 0; portValue[slotEntry] = 0; return 0;
    }
}
