// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.Inethiwekhi_fumba;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ibhayithi_ixabiso 순서와 검사합 도구다. */
public final class Inethiwekhi_Izixhobo {
    private Inethiwekhi_Izixhobo() {
    }

    public static int 큰순서짧은정수(byte[] iingcombolo, int 위치) {
        범위확인(iingcombolo, 위치, 2);
        return ((iingcombolo[위치] & 0xff) << 8) | (iingcombolo[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] iingcombolo, int 위치) {
        범위확인(iingcombolo, 위치, 4);
        return ((long) (iingcombolo[위치] & 0xff) << 24)
                | ((long) (iingcombolo[위치 + 1] & 0xff) << 16)
                | ((long) (iingcombolo[위치 + 2] & 0xff) << 8)
                | (iingcombolo[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] iingcombolo, int Phumeza, int ubude_ixabiso) {
        범위확인(iingcombolo, Phumeza, ubude_ixabiso);
        long 합 = 0;
        int 끝 = Phumeza + ubude_ixabiso;
        int 위치 = Phumeza;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(iingcombolo, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (iingcombolo[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] iingcombolo) {
        return iingcombolo != null && iingcombolo.length >= 14;
    }

    public static int 이더넷상위규약(byte[] iingcombolo) {
        if (!이더넷틀인가(iingcombolo)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(iingcombolo, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] iingcombolo, int 위치) {
        if (iingcombolo == null || 위치 < 0 || iingcombolo.length - 위치 < 20) {
            return false;
        }
        int inguqulelo_ixabiso = (iingcombolo[위치] >>> 4) & 0xf;
        int Iheda_ubude = (iingcombolo[위치] & 0xf) * 4;
        return inguqulelo_ixabiso == 4 && Iheda_ubude >= 20 && iingcombolo.length - 위치 >= Iheda_ubude;
    }

    private static void 범위확인(byte[] iingcombolo, int Phumeza, int ubude_ixabiso) {
        if (iingcombolo == null || Phumeza < 0 || ubude_ixabiso < 0 || Phumeza > iingcombolo.length - ubude_ixabiso) {
            throw new IllegalArgumentException("Inethiwekhi_fumba iingcombolo 범위를 벗어났습니다.");
        }
    }
}

