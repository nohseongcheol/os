// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** Calls the real Java protocol handler in a JVM to check bounds and malformed input quickly. */
public final class PacketTest {
    static int repetitionCount = 0;
    static void verify(boolean value) { if (!value) throw new AssertionError("case " + repetitionCount); repetitionCount++; }
    static int checksum(int[] value, int run, int lengthValue, int initialState) {
        int sumValue = initialState;
        for (int index = 0; index < lengthValue; index++) sumValue += value[run + index] << ((index & 1) == 0 ? 8 : 0);
        sumValue = (sumValue & 65535) + (sumValue >>> 16);
        sumValue = (sumValue & 65535) + (sumValue >>> 16);
        return ~sumValue & 65535;
    }
    static void prepare(int lengthValue) {
        networkStack.cleanProcess();
        verify(networkStack.open(5000) == 3);
        int[] frameIndex = networkStack.inputFrame;
        Arrays.fill(frameIndex, 0);
        for (int index = 0; index < 6; index++) frameIndex[index] = NetworkDeviceDriver.deviceAddress[index];
        networkStack.put16(frameIndex, 12, 0x0800);
        frameIndex[14] = 0x45; frameIndex[22] = 64; frameIndex[23] = 17;
        networkStack.put16(frameIndex, 16, 28 + lengthValue);
        networkStack.put32(frameIndex, 26, 0x0a000202); networkStack.put32(frameIndex, 30, networkStack.ownAddress);
        networkStack.put16(frameIndex, 34, 4321); networkStack.put16(frameIndex, 36, 5000); networkStack.put16(frameIndex, 38, lengthValue + 8);
        for (int index = 0; index < lengthValue; index++) frameIndex[42 + index] = index & 255;
        setChecksum(lengthValue);
    }
    static void setChecksum(int lengthValue) {
        int[] frameIndex = networkStack.inputFrame;
        networkStack.put16(frameIndex, 24, 0); networkStack.put16(frameIndex, 40, 0);
        networkStack.put16(frameIndex, 24, checksum(frameIndex, 14, 20, 0));
        int initialState = networkStack.pseudoHeaderChecksum(networkStack.integer32(frameIndex, 26), networkStack.ownAddress, lengthValue + 8);
        int sumValue = checksum(frameIndex, 34, lengthValue + 8, initialState);
        networkStack.put16(frameIndex, 40, sumValue == 0 ? 65535 : sumValue);
    }
    static void rejectValue(int lengthValue) { networkStack.processFrame(lengthValue); verify(networkStack.receivedLength[0] == -1); }
    public static void main(String[] arguments) {
        for (int lengthValue : new int[]{0, 1, 2, 7, 1023, 1024}) {
            prepare(lengthValue); networkStack.processFrame(lengthValue + 42);
            verify(networkStack.receivedLength[0] == lengthValue);
            verify(networkStack.receivedAddress[0] == 0x0a000202 && networkStack.receivedPortNumber[0] == 4321);
            for (int index = 0; index < lengthValue; index++) verify(networkStack.receivedData[index] == (index & 255));
        }
        for (int lengthValue = 0; lengthValue < 42; lengthValue++) { prepare(0); rejectValue(lengthValue); }
        prepare(1025); rejectValue(1067);
        prepare(2); networkStack.inputFrame[24] ^= 1; rejectValue(44);
        prepare(2); networkStack.inputFrame[42] ^= 1; rejectValue(44);
        prepare(2); networkStack.put16(networkStack.inputFrame, 38, 7); rejectValue(44);
        prepare(2); networkStack.put16(networkStack.inputFrame, 38, 65535); rejectValue(44);
        prepare(2); networkStack.inputFrame[14] = 0x4f; rejectValue(44);
        prepare(2); networkStack.inputFrame[14] = 0x44; rejectValue(44);
        prepare(2); networkStack.inputFrame[20] = 0x20; setChecksum(2); rejectValue(44);
        prepare(2); networkStack.inputFrame[21] = 1; setChecksum(2); rejectValue(44);
        prepare(2); networkStack.inputFrame[33] = 99; setChecksum(2); rejectValue(44);
        prepare(2); networkStack.inputFrame[0] ^= 1; rejectValue(44);
        prepare(2); networkStack.inputFrame[23] = 6; setChecksum(2); rejectValue(44);
        prepare(2); networkStack.put16(networkStack.inputFrame, 40, 0); networkStack.processFrame(44); verify(networkStack.receivedLength[0] == 2);
        int[] result = new int[4];
        verify(networkStack.receive(3, result, 1, 0) == -90);
        verify(networkStack.receive(3, result, 4, 0) == -11);
        prepare(2); networkStack.processFrame(44); int discardValue = networkStack.discardedCount;
        networkStack.processFrame(44); verify(networkStack.discardedCount == discardValue + 1);
        networkStack.cleanProcess(); verify(networkStack.open(5000) == 3);
        verify(networkStack.open(5000) == -98); verify(networkStack.open(0) == 4);
        verify(networkStack.open(0) == 5); verify(networkStack.open(0) == 6); verify(networkStack.open(0) == -24);
        verify(networkStack.close(4) == 0); verify(networkStack.close(4) == -9);
        networkStack.foundAddress = networkStack.gatewayValue;
        verify(networkStack.send(3, networkStack.gatewayValue, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] hasSent = NetworkDeviceDriver.recentValue;
        verify(checksum(hasSent, 14, 20, 0) == 0);
        verify(checksum(hasSent, 34, 11, networkStack.pseudoHeaderChecksum(networkStack.ownAddress, networkStack.gatewayValue, 11)) == 0);
        verify(hasSent[42] == 1 && hasSent[44] == 3);
        System.out.println("PACKET TEST PASS: " + repetitionCount + " assertions");
    }
}
