// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.Urusobemiyoboro_Ikirundo;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bayiti_agaciro 순서와 검사합 도구다. */
public final class Urusobemiyoboro_Ibikoresho {
    private Urusobemiyoboro_Ibikoresho() {
    }

    public static int 큰순서짧은정수(byte[] amakurushingiro, int 위치) {
        범위확인(amakurushingiro, 위치, 2);
        return ((amakurushingiro[위치] & 0xff) << 8) | (amakurushingiro[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] amakurushingiro, int 위치) {
        범위확인(amakurushingiro, 위치, 4);
        return ((long) (amakurushingiro[위치] & 0xff) << 24)
                | ((long) (amakurushingiro[위치 + 1] & 0xff) << 16)
                | ((long) (amakurushingiro[위치 + 2] & 0xff) << 8)
                | (amakurushingiro[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] amakurushingiro, int ihuriro, int uburebure_agaciro) {
        범위확인(amakurushingiro, ihuriro, uburebure_agaciro);
        long 합 = 0;
        int 끝 = ihuriro + uburebure_agaciro;
        int 위치 = ihuriro;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(amakurushingiro, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (amakurushingiro[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] amakurushingiro) {
        return amakurushingiro != null && amakurushingiro.length >= 14;
    }

    public static int 이더넷상위규약(byte[] amakurushingiro) {
        if (!이더넷틀인가(amakurushingiro)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(amakurushingiro, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] amakurushingiro, int 위치) {
        if (amakurushingiro == null || 위치 < 0 || amakurushingiro.length - 위치 < 20) {
            return false;
        }
        int verisiyo_agaciro = (amakurushingiro[위치] >>> 4) & 0xf;
        int Umutwengaruka_uburebure = (amakurushingiro[위치] & 0xf) * 4;
        return verisiyo_agaciro == 4 && Umutwengaruka_uburebure >= 20 && amakurushingiro.length - 위치 >= Umutwengaruka_uburebure;
    }

    private static void 범위확인(byte[] amakurushingiro, int ihuriro, int uburebure_agaciro) {
        if (amakurushingiro == null || ihuriro < 0 || uburebure_agaciro < 0 || ihuriro > amakurushingiro.length - uburebure_agaciro) {
            throw new IllegalArgumentException("Urusobemiyoboro_Ikirundo amakurushingiro 범위를 벗어났습니다.");
        }
    }
}

