// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Mooritani.JMrtOS.mbaal_Tegalo;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 okte_xëyma 순서와 검사합 도구다. */
public final class mbaal_Jumtukaay_yi {
    private mbaal_Jumtukaay_yi() {
    }

    public static int 큰순서짧은정수(byte[] mbir, int 위치) {
        범위확인(mbir, 위치, 2);
        return ((mbir[위치] & 0xff) << 8) | (mbir[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] mbir, int 위치) {
        범위확인(mbir, 위치, 4);
        return ((long) (mbir[위치] & 0xff) << 24)
                | ((long) (mbir[위치 + 1] & 0xff) << 16)
                | ((long) (mbir[위치 + 2] & 0xff) << 8)
                | (mbir[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] mbir, int daw, int diir_xëyma) {
        범위확인(mbir, daw, diir_xëyma);
        long 합 = 0;
        int 끝 = daw + diir_xëyma;
        int 위치 = daw;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(mbir, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (mbir[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] mbir) {
        return mbir != null && mbir.length >= 14;
    }

    public static int 이더넷상위규약(byte[] mbir) {
        if (!이더넷틀인가(mbir)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(mbir, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] mbir, int 위치) {
        if (mbir == null || 위치 < 0 || mbir.length - 위치 < 20) {
            return false;
        }
        int taalif_xëyma = (mbir[위치] >>> 4) & 0xf;
        int Tur_diir = (mbir[위치] & 0xf) * 4;
        return taalif_xëyma == 4 && Tur_diir >= 20 && mbir.length - 위치 >= Tur_diir;
    }

    private static void 범위확인(byte[] mbir, int daw, int diir_xëyma) {
        if (mbir == null || daw < 0 || diir_xëyma < 0 || daw > mbir.length - diir_xëyma) {
            throw new IllegalArgumentException("mbaal_Tegalo mbir 범위를 벗어났습니다.");
        }
    }
}

