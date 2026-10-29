// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.통신망;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 byte_ᏧᎬᏩᎶᏗᏯ 순서와 검사합 도구다. */
public final class 통신망도구 {
    private 통신망도구() {
    }

    public static int 큰순서짧은정수(byte[] ᎦᏟᏌᏅᎯ, int 위치) {
        범위확인(ᎦᏟᏌᏅᎯ, 위치, 2);
        return ((ᎦᏟᏌᏅᎯ[위치] & 0xff) << 8) | (ᎦᏟᏌᏅᎯ[위치 + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ᎦᏟᏌᏅᎯ, int 위치) {
        범위확인(ᎦᏟᏌᏅᎯ, 위치, 4);
        return ((long) (ᎦᏟᏌᏅᎯ[위치] & 0xff) << 24)
                | ((long) (ᎦᏟᏌᏅᎯ[위치 + 1] & 0xff) << 16)
                | ((long) (ᎦᏟᏌᏅᎯ[위치 + 2] & 0xff) << 8)
                | (ᎦᏟᏌᏅᎯ[위치 + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] ᎦᏟᏌᏅᎯ, int ᎠᎢᏎᏍᏗ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
        범위확인(ᎦᏟᏌᏅᎯ, ᎠᎢᏎᏍᏗ, ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ);
        long 합 = 0;
        int 끝 = ᎠᎢᏎᏍᏗ + ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ;
        int 위치 = ᎠᎢᏎᏍᏗ;
        while (위치 + 1 < 끝) {
            합 += 큰순서짧은정수(ᎦᏟᏌᏅᎯ, 위치);
            위치 += 2;
        }
        if (위치 < 끝) {
            합 += (ᎦᏟᏌᏅᎯ[위치] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] ᎦᏟᏌᏅᎯ) {
        return ᎦᏟᏌᏅᎯ != null && ᎦᏟᏌᏅᎯ.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ᎦᏟᏌᏅᎯ) {
        if (!이더넷틀인가(ᎦᏟᏌᏅᎯ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ᎦᏟᏌᏅᎯ, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ᎦᏟᏌᏅᎯ, int 위치) {
        if (ᎦᏟᏌᏅᎯ == null || 위치 < 0 || ᎦᏟᏌᏅᎯ.length - 위치 < 20) {
            return false;
        }
        int ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ = (ᎦᏟᏌᏅᎯ[위치] >>> 4) & 0xf;
        int ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ = (ᎦᏟᏌᏅᎯ[위치] & 0xf) * 4;
        return ᏄᏓᎴᏒᎢ_ᏧᎬᏩᎶᏗᏯ == 4 && ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ >= 20 && ᎦᏟᏌᏅᎯ.length - 위치 >= ᎦᎸᎳᏗ_ᎪᏪᎵ_ᏱᎦᏅᎯᏓ;
    }

    private static void 범위확인(byte[] ᎦᏟᏌᏅᎯ, int ᎠᎢᏎᏍᏗ, int ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
        if (ᎦᏟᏌᏅᎯ == null || ᎠᎢᏎᏍᏗ < 0 || ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ < 0 || ᎠᎢᏎᏍᏗ > ᎦᏟᏌᏅᎯ.length - ᏱᎦᏅᎯᏓ_ᏧᎬᏩᎶᏗᏯ) {
            throw new IllegalArgumentException("통신망 ᎦᏟᏌᏅᎯ 범위를 벗어났습니다.");
        }
    }
}

