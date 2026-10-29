// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.Líonra_Cruach;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 beart_VALUE 순서와 suim_seiceála 도구다. */
public final class Líonra_Uirlisí {
    private Líonra_Uirlisí() {
    }

    public static int 큰순서짧은정수(byte[] sonraí, int suíomh) {
        범위확인(sonraí, suíomh, 2);
        return ((sonraí[suíomh] & 0xff) << 8) | (sonraí[suíomh + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] sonraí, int suíomh) {
        범위확인(sonraí, suíomh, 4);
        return ((long) (sonraí[suíomh] & 0xff) << 24)
                | ((long) (sonraí[suíomh + 1] & 0xff) << 16)
                | ((long) (sonraí[suíomh + 2] & 0xff) << 8)
                | (sonraí[suíomh + 3] & 0xffL);
    }

    public static int néal_suim_seiceála(byte[] sonraí, int Rith_2, int fad_VALUE) {
        범위확인(sonraí, Rith_2, fad_VALUE);
        long SUM_VALUE = 0;
        int 끝 = Rith_2 + fad_VALUE;
        int suíomh = Rith_2;
        while (suíomh + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(sonraí, suíomh);
            suíomh += 2;
        }
        if (suíomh < 끝) {
            SUM_VALUE += (sonraí[suíomh] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean teicneolaíocht_faisnéise_Ethernet_fráma(byte[] sonraí) {
        return sonraí != null && sonraí.length >= 14;
    }

    public static int Ethernet_UPPER_prótacal(byte[] sonraí) {
        if (!teicneolaíocht_faisnéise_Ethernet_fráma(sonraí)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(sonraí, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] sonraí, int suíomh) {
        if (sonraí == null || suíomh < 0 || sonraí.length - suíomh < 20) {
            return false;
        }
        int leagan_VALUE = (sonraí[suíomh] >>> 4) & 0xf;
        int Ceanntásc_fad = (sonraí[suíomh] & 0xf) * 4;
        return leagan_VALUE == 4 && Ceanntásc_fad >= 20 && sonraí.length - suíomh >= Ceanntásc_fad;
    }

    private static void 범위확인(byte[] sonraí, int Rith_2, int fad_VALUE) {
        if (sonraí == null || Rith_2 < 0 || fad_VALUE < 0 || Rith_2 > sonraí.length - fad_VALUE) {
            throw new IllegalArgumentException("Líonra_Cruach sonraí 범위를 벗어났습니다.");
        }
    }
}

