// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Connection-oriented byte streams inside the kernel: a loopback socket layer, not an Ethernet/TCP packet stack. */
public final class StreamNetwork {
    static int[] stateValue = new int[16], portValue = new int[16], pairedValue = new int[16], peerPort = new int[16], waitValue = new int[16], isBound = new int[16];
    static int[] frontValue = new int[16], number = new int[16], data = new int[16 * 1024];
    static int nextItem = 50000;
    static int verify(int openedFileNumber) { return openedFileNumber >= 40 && openedFileNumber < 56 && stateValue[openedFileNumber - 40] != 0 ? openedFileNumber - 40 : -1; }
    static boolean isInUse(int portNumber) { for (int loopIndex = 0; loopIndex < 16; loopIndex++) if (stateValue[loopIndex] != 0 && isBound[loopIndex] != 0 && portValue[loopIndex] == portNumber) return true; return false; }
    public static int createEntry() {
        for (int loopIndex = 0; loopIndex < 16; loopIndex++) if (stateValue[loopIndex] == 0) { stateValue[loopIndex] = 1; peerPort[loopIndex] = portValue[loopIndex] = frontValue[loopIndex] = number[loopIndex] = waitValue[loopIndex] = isBound[loopIndex] = 0; pairedValue[loopIndex] = -1; return loopIndex + 40; }
        return -24;
    }
    public static int bindEndpoint(int openedFileNumber, int SocketAddress, int portNumber) {
        int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9;
        if (SocketAddress != 0 && SocketAddress != 0x7f000001) return -99;
        if (stateValue[loopIndex] != 1 || portNumber < 0 || portNumber > 65535) return -22;
        if (portNumber == 0) { do { portNumber = nextItem++; if (nextItem > 65535) nextItem = 50000; } while (isInUse(portNumber)); }
        if (isInUse(portNumber)) return -98; portValue[loopIndex] = portNumber; isBound[loopIndex] = 1; stateValue[loopIndex] = 2; return 0;
    }
    public static int listenEndpoint(int openedFileNumber, int backlog) { int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9; if (stateValue[loopIndex] != 2 || backlog < 1) return -22; stateValue[loopIndex] = 3; return 0; }
    public static int connect(int openedFileNumber, int SocketAddress, int portNumber) {
        int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9; if (SocketAddress != 0x7f000001) return -101;
        if (portNumber < 1 || portNumber > 65535 || stateValue[loopIndex] > 2) return -22;
        int receivePage = -1; for (int innerPosition = 0; innerPosition < 16; innerPosition++) if (stateValue[innerPosition] == 3 && portValue[innerPosition] == portNumber) receivePage = innerPosition;
        if (receivePage < 0) return -111;
        int isQueued = 0; for (int innerPosition = 0; innerPosition < 16; innerPosition++) if (waitValue[innerPosition] == receivePage + 1) isQueued++;
        if (isQueued >= 4) return -11;
        if (stateValue[loopIndex] == 1) { int processedValue = bindEndpoint(openedFileNumber, 0x7f000001, 0); if (processedValue < 0) return processedValue; }
        int other = createEntry(); if (other < 0) return other; other -= 40;
        stateValue[loopIndex] = stateValue[other] = 4; pairedValue[loopIndex] = other; pairedValue[other] = loopIndex; portValue[other] = portNumber; peerPort[loopIndex] = portNumber; peerPort[other] = portValue[loopIndex]; waitValue[other] = receivePage + 1; return 0;
    }
    public static int acceptConnection(int openedFileNumber) { int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9; if (stateValue[loopIndex] != 3) return -22; for (int innerPosition = 0; innerPosition < 16; innerPosition++) if (stateValue[innerPosition] != 0 && waitValue[innerPosition] == loopIndex + 1) { waitValue[innerPosition] = 0; return innerPosition + 40; } return -11; }
    public static int write(int openedFileNumber, int entryCount) {
        int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9; if (stateValue[loopIndex] != 4) return -107;
        if (entryCount < 0 || entryCount > 512) return -22; if (entryCount == 0) return 0;
        int innerPosition = pairedValue[loopIndex]; if (innerPosition < 0) return -32; int totalCount = 1024 - number[innerPosition]; if (totalCount == 0) return -11; if (totalCount > entryCount) totalCount = entryCount;
        for (int comparisonPosition = 0; comparisonPosition < totalCount; comparisonPosition++) data[innerPosition * 1024 + (frontValue[innerPosition] + number[innerPosition] + comparisonPosition) % 1024] = LoopbackNetwork.forwardValue[comparisonPosition]; number[innerPosition] += totalCount; return totalCount;
    }
    public static int read(int openedFileNumber, int entryCount) {
        int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9; if (stateValue[loopIndex] != 4) return -107; if (entryCount < 0 || entryCount > 512) return -22;
        if (entryCount == 0) return 0; if (number[loopIndex] == 0) return pairedValue[loopIndex] < 0 ? 0 : -11; if (entryCount > number[loopIndex]) entryCount = number[loopIndex];
        for (int comparisonPosition = 0; comparisonPosition < entryCount; comparisonPosition++) LoopbackNetwork.forwardValue[comparisonPosition] = data[loopIndex * 1024 + (frontValue[loopIndex] + comparisonPosition) % 1024]; frontValue[loopIndex] = (frontValue[loopIndex] + entryCount) % 1024; number[loopIndex] -= entryCount; return entryCount;
    }
    public static int readEndpointPort(int openedFileNumber) { int loopIndex = verify(openedFileNumber); return loopIndex < 0 ? -9 : portValue[loopIndex]; }
    public static int readPeerPort(int openedFileNumber) { int loopIndex = verify(openedFileNumber); return loopIndex < 0 ? -9 : peerPort[loopIndex]; }
    public static int close(int openedFileNumber) {
        int loopIndex = verify(openedFileNumber); if (loopIndex < 0) return -9;
        if (stateValue[loopIndex] == 3) for (int innerPosition = 0; innerPosition < 16; innerPosition++) if (waitValue[innerPosition] == loopIndex + 1) { if (pairedValue[innerPosition] >= 0) pairedValue[pairedValue[innerPosition]] = -1; stateValue[innerPosition] = waitValue[innerPosition] = isBound[innerPosition] = 0; }
        if (pairedValue[loopIndex] >= 0) pairedValue[pairedValue[loopIndex]] = -1; stateValue[loopIndex] = isBound[loopIndex] = number[loopIndex] = waitValue[loopIndex] = 0; return 0;
    }
}
