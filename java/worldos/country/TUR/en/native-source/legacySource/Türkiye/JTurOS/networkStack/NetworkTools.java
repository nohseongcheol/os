// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiye.JTurOS.networkStack;

/** Byte-order and checksum helpers shared by Ethernet/ARP/IPv4/ICMP/UDP layers. */
public final class NetworkTools {
    private NetworkTools() {
    }

    public static int bigEndianShort(byte[] data, int position) {
        checkRange(data, position, 2);
        return ((data[position] & 0xff) << 8) | (data[position + 1] & 0xff);
    }

    public static long bigEndianInteger(byte[] data, int position) {
        checkRange(data, position, 4);
        return ((long) (data[position] & 0xff) << 24)
                | ((long) (data[position + 1] & 0xff) << 16)
                | ((long) (data[position + 2] & 0xff) << 8)
                | (data[position + 3] & 0xffL);
    }

    public static int internetChecksum(byte[] data, int run, int lengthValue) {
        checkRange(data, run, lengthValue);
        long sumValue = 0;
        int ending = run + lengthValue;
        int position = run;
        while (position + 1 < ending) {
            sumValue += bigEndianShort(data, position);
            position += 2;
        }
        if (position < ending) {
            sumValue += (data[position] & 0xff) << 8;
        }
        while ((sumValue >>> 16) != 0) {
            sumValue = (sumValue & 0xffff) + (sumValue >>> 16);
        }
        return (int) (~sumValue) & 0xffff;
    }

    public static boolean isEthernetFrame(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int ethernetUpperProtocol(byte[] data) {
        if (!isEthernetFrame(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return bigEndianShort(data, 12);
    }

    public static boolean isIpv4Protocol(byte[] data, int position) {
        if (data == null || position < 0 || data.length - position < 20) {
            return false;
        }
        int versionValue = (data[position] >>> 4) & 0xf;
        int headerLength = (data[position] & 0xf) * 4;
        return versionValue == 4 && headerLength >= 20 && data.length - position >= headerLength;
    }

    private static void checkRange(byte[] data, int run, int lengthValue) {
        if (data == null || run < 0 || lengthValue < 0 || run > data.length - lengthValue) {
            throw new IllegalArgumentException("networkStack data 범위를 벗어났습니다.");
        }
    }
}

