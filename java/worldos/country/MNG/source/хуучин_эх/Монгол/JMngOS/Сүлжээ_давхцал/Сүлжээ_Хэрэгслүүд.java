// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол.JMngOS.Сүлжээ_давхцал;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 байт_утга 순서와 검사합 도구다. */
public final class Сүлжээ_Хэрэгслүүд {
    private Сүлжээ_Хэрэгслүүд() {
    }

    public static int 큰순서짧은정수(byte[] өгөгдөл, int 위치) {
        범위확인(өгөгдөл, 위치, 2);
        return ((өгөгдөл[위치] & 0xff) << 8) | (өгөгдөл[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] өгөгдөл, int 위치) {
        범위확인(өгөгдөл, 위치, 4);
        return ((long) (өгөгдөл[위치] & 0xff) << 24)
                | ((long) (өгөгдөл[위치 + 1] & 0xff) << 16)
                | ((long) (өгөгдөл[위치 + 2] & 0xff) << 8)
                | (өгөгдөл[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] өгөгдөл, int Ажиллуулах, int урт_утга) {
        범위확인(өгөгдөл, Ажиллуулах, урт_утга);
        long 합 = 0;
        int 끝 = Ажиллуулах + урт_утга;
        int 위치 = Ажиллуулах;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(өгөгдөл, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (өгөгдөл[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] өгөгдөл) {
        return өгөгдөл != null && өгөгдөл.length >= 14;
    }

    public static int 이더넷상위규약(byte[] өгөгдөл) {
        if (!이더넷틀인가(өгөгдөл)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(өгөгдөл, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] өгөгдөл, int 위치) {
        if (өгөгдөл == null || 위치 < 0 || өгөгдөл.length - 위치 < 20) {
            return false;
        }
        int хувилбар_утга = (өгөгдөл[위치] >>> 4) & 0xf;
        int Толгой_урт = (өгөгдөл[위치] & 0xf) * 4;
        return хувилбар_утга == 4 && Толгой_урт >= 20 && өгөгдөл.length - 위치 >= Толгой_урт;
    }

    private static void 범위확인(byte[] өгөгдөл, int Ажиллуулах, int урт_утга) {
        if (өгөгдөл == null || Ажиллуулах < 0 || урт_утга < 0 || Ажиллуулах > өгөгдөл.length - урт_утга) {
            throw new IllegalArgumentException("Сүлжээ_давхцал өгөгдөл 범위를 벗어났습니다.");
        }
    }
}

