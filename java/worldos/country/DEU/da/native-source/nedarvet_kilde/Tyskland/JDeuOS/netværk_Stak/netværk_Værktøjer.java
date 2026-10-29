// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tyskland.JDeuOS.netværk_Stak;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_VÆRDI 순서와 kontrolsum 도구다. */
public final class netværk_Værktøjer {
    private netværk_Værktøjer() {
    }

    public static int 큰순서짧은정수(byte[] data, int Placering) {
        check_område(data, Placering, 2);
        return ((data[Placering] & 0xff) << 8) | (data[Placering + 1] & 0xff);
    }

    public static long big_endian_heltal(byte[] data, int Placering) {
        check_område(data, Placering, 4);
        return ((long) (data[Placering] & 0xff) << 24)
                | ((long) (data[Placering + 1] & 0xff) << 16)
                | ((long) (data[Placering + 2] & 0xff) << 8)
                | (data[Placering + 3] & 0xffL);
    }

    public static int net_kontrolsum(byte[] data, int Kør_2, int varighed_VÆRDI) {
        check_område(data, Kør_2, varighed_VÆRDI);
        long SUM_VÆRDI = 0;
        int 끝 = Kør_2 + varighed_VÆRDI;
        int Placering = Kør_2;
        while (Placering + 1 < 끝) {
            SUM_VÆRDI += 큰순서짧은정수(data, Placering);
            Placering += 2;
        }
        if (Placering < 끝) {
            SUM_VÆRDI += (data[Placering] & 0xff) << 8;
        }
        while ((SUM_VÆRDI >>> 16) != 0) {
            SUM_VÆRDI = (SUM_VÆRDI & 0xffff) + (SUM_VÆRDI >>> 16);
        }
        return (int) (~SUM_VÆRDI) & 0xffff;
    }

    public static boolean it_Ethernet_ramme(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_STORE_BOGSTAVER_protokol(byte[] data) {
        if (!it_Ethernet_ramme(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean it_IPV_4_protokol(byte[] data, int Placering) {
        if (data == null || Placering < 0 || data.length - Placering < 20) {
            return false;
        }
        int version_VÆRDI = (data[Placering] >>> 4) & 0xf;
        int Header_varighed = (data[Placering] & 0xf) * 4;
        return version_VÆRDI == 4 && Header_varighed >= 20 && data.length - Placering >= Header_varighed;
    }

    private static void check_område(byte[] data, int Kør_2, int varighed_VÆRDI) {
        if (data == null || Kør_2 < 0 || varighed_VÆRDI < 0 || Kør_2 > data.length - varighed_VÆRDI) {
            throw new IllegalArgumentException("netværk_Stak data 범위를 벗어났습니다.");
        }
    }
}

