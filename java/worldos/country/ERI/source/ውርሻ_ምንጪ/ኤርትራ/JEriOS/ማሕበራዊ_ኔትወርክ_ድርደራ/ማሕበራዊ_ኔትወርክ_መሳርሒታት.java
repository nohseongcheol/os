// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኤርትራ.JEriOS.ማሕበራዊ_ኔትወርክ_ድርደራ;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ባይት_ዋጋ 순서와 검사합 도구다. */
public final class ማሕበራዊ_ኔትወርክ_መሳርሒታት {
    private ማሕበራዊ_ኔትወርክ_መሳርሒታት() {
    }

    public static int 큰순서짧은정수(byte[] ሓበሬታ, int 위치) {
        범위확인(ሓበሬታ, 위치, 2);
        return ((ሓበሬታ[위치] & 0xff) << 8) | (ሓበሬታ[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ሓበሬታ, int 위치) {
        범위확인(ሓበሬታ, 위치, 4);
        return ((long) (ሓበሬታ[위치] & 0xff) << 24)
                | ((long) (ሓበሬታ[위치 + 1] & 0xff) << 16)
                | ((long) (ሓበሬታ[위치 + 2] & 0xff) << 8)
                | (ሓበሬታ[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ሓበሬታ, int ኣኺድ, int ንውሓት_ዋጋ) {
        범위확인(ሓበሬታ, ኣኺድ, ንውሓት_ዋጋ);
        long 합 = 0;
        int 끝 = ኣኺድ + ንውሓት_ዋጋ;
        int 위치 = ኣኺድ;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(ሓበሬታ, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (ሓበሬታ[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] ሓበሬታ) {
        return ሓበሬታ != null && ሓበሬታ.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ሓበሬታ) {
        if (!이더넷틀인가(ሓበሬታ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ሓበሬታ, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ሓበሬታ, int 위치) {
        if (ሓበሬታ == null || 위치 < 0 || ሓበሬታ.length - 위치 < 20) {
            return false;
        }
        int ሕታም_ዋጋ = (ሓበሬታ[위치] >>> 4) & 0xf;
        int ርእሲ_ንውሓት = (ሓበሬታ[위치] & 0xf) * 4;
        return ሕታም_ዋጋ == 4 && ርእሲ_ንውሓት >= 20 && ሓበሬታ.length - 위치 >= ርእሲ_ንውሓት;
    }

    private static void 범위확인(byte[] ሓበሬታ, int ኣኺድ, int ንውሓት_ዋጋ) {
        if (ሓበሬታ == null || ኣኺድ < 0 || ንውሓት_ዋጋ < 0 || ኣኺድ > ሓበሬታ.length - ንውሓት_ዋጋ) {
            throw new IllegalArgumentException("ማሕበራዊ_ኔትወርክ_ድርደራ ሓበሬታ 범위를 벗어났습니다.");
        }
    }
}

