// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.nätverk_Stack;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_värde 순서와 kontrollsumma 도구다. */
public final class nätverk_Verktyg {
    private nätverk_Verktyg() {
    }

    public static int 큰순서짧은정수(byte[] data, int position) {
        check_område(data, position, 2);
        return ((data[position] & 0xff) << 8) | (data[position + 1] & 0xff);
    }

    public static long big_endian_heltal(byte[] data, int position) {
        check_område(data, position, 4);
        return ((long) (data[position] & 0xff) << 24)
                | ((long) (data[position + 1] & 0xff) << 16)
                | ((long) (data[position + 2] & 0xff) << 8)
                | (data[position + 3] & 0xffL);
    }

    public static int nät_kontrollsumma(byte[] data, int Kör, int längd_värde) {
        check_område(data, Kör, längd_värde);
        long SUM_värde = 0;
        int 끝 = Kör + längd_värde;
        int position = Kör;
        while (position + 1 < 끝) {
            SUM_värde += 큰순서짧은정수(data, position);
            position += 2;
        }
        if (position < 끝) {
            SUM_värde += (data[position] & 0xff) << 8;
        }
        while ((SUM_värde >>> 16) != 0) {
            SUM_värde = (SUM_värde & 0xffff) + (SUM_värde >>> 16);
        }
        return (int) (~SUM_värde) & 0xffff;
    }

    public static boolean informationsteknik_Ethernet_ram(byte[] data) {
        return data != null && data.length >= 14;
    }

    public static int Ethernet_VERSALER_protokoll(byte[] data) {
        if (!informationsteknik_Ethernet_ram(data)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(data, 12);
    }

    public static boolean informationsteknik_FPV_4_protokoll(byte[] data, int position) {
        if (data == null || position < 0 || data.length - position < 20) {
            return false;
        }
        int version_värde = (data[position] >>> 4) & 0xf;
        int huvud_längd = (data[position] & 0xf) * 4;
        return version_värde == 4 && huvud_längd >= 20 && data.length - position >= huvud_längd;
    }

    private static void check_område(byte[] data, int Kör, int längd_värde) {
        if (data == null || Kör < 0 || längd_värde < 0 || Kör > data.length - längd_värde) {
            throw new IllegalArgumentException("nätverk_Stack data 범위를 벗어났습니다.");
        }
    }
}

