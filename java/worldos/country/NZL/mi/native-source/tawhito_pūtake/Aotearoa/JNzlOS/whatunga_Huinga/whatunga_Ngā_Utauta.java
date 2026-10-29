// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.whatunga_Huinga;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 paita_uara 순서와 검사합 도구다. */
public final class whatunga_Ngā_Utauta {
    private whatunga_Ngā_Utauta() {
    }

    public static int 큰순서짧은정수(byte[] raraunga, int tūranga) {
        범위확인(raraunga, tūranga, 2);
        return ((raraunga[tūranga] & 0xff) << 8) | (raraunga[tūranga + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] raraunga, int tūranga) {
        범위확인(raraunga, tūranga, 4);
        return ((long) (raraunga[tūranga] & 0xff) << 24)
                | ((long) (raraunga[tūranga + 1] & 0xff) << 16)
                | ((long) (raraunga[tūranga + 2] & 0xff) << 8)
                | (raraunga[tūranga + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] raraunga, int whakahaere, int roa_uara) {
        범위확인(raraunga, whakahaere, roa_uara);
        long SUM_uara = 0;
        int 끝 = whakahaere + roa_uara;
        int tūranga = whakahaere;
        while (tūranga + 1 < 끝) {
            SUM_uara += 큰순서짧은정수(raraunga, tūranga);
            tūranga += 2;
        }
        if (tūranga < 끝) {
            SUM_uara += (raraunga[tūranga] & 0xff) << 8;
        }
        while ((SUM_uara >>> 16) != 0) {
            SUM_uara = (SUM_uara & 0xffff) + (SUM_uara >>> 16);
        }
        return (int) (~SUM_uara) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] raraunga) {
        return raraunga != null && raraunga.length >= 14;
    }

    public static int Itarangi_UPPER_kawa(byte[] raraunga) {
        if (!이더넷틀인가(raraunga)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(raraunga, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] raraunga, int tūranga) {
        if (raraunga == null || tūranga < 0 || raraunga.length - tūranga < 20) {
            return false;
        }
        int putanga_uara = (raraunga[tūranga] >>> 4) & 0xf;
        int Pane_roa = (raraunga[tūranga] & 0xf) * 4;
        return putanga_uara == 4 && Pane_roa >= 20 && raraunga.length - tūranga >= Pane_roa;
    }

    private static void 범위확인(byte[] raraunga, int whakahaere, int roa_uara) {
        if (raraunga == null || whakahaere < 0 || roa_uara < 0 || whakahaere > raraunga.length - roa_uara) {
            throw new IllegalArgumentException("whatunga_Huinga raraunga 범위를 벗어났습니다.");
        }
    }
}

