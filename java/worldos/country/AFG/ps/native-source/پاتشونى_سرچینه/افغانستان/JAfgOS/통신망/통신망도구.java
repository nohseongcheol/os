// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package افغانستان.JAfgOS.통신망;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بايټ_ارزښت 순서와 검사합 도구다. */
public final class 통신망도구 {
    private 통신망도구() {
    }

    public static int 큰순서짧은정수(byte[] اومتوک, int ځای) {
        범위확인(اومتوک, ځای, 2);
        return ((اومتوک[ځای] & 0xff) << 8) | (اومتوک[ځای + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] اومتوک, int ځای) {
        범위확인(اومتوک, ځای, 4);
        return ((long) (اومتوک[ځای] & 0xff) << 24)
                | ((long) (اومتوک[ځای + 1] & 0xff) << 16)
                | ((long) (اومتوک[ځای + 2] & 0xff) << 8)
                | (اومتوک[ځای + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] اومتوک, int ځغلول, int اوږدوالى_ارزښت) {
        범위확인(اومتوک, ځغلول, اوږدوالى_ارزښت);
        long 합 = 0;
        int 끝 = ځغلول + اوږدوالى_ارزښت;
        int ځای = ځغلول;
        while (ځای + 1 < 끝) {
            합 += 큰순서짧은정수(اومتوک, ځای);
            ځای += 2;
        }
        if (ځای < 끝) {
            합 += (اومتوک[ځای] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] اومتوک) {
        return اومتوک != null && اومتوک.length >= 14;
    }

    public static int 이더넷상위규약(byte[] اومتوک) {
        if (!이더넷틀인가(اومتوک)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(اومتوک, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] اومتوک, int ځای) {
        if (اومتوک == null || ځای < 0 || اومتوک.length - ځای < 20) {
            return false;
        }
        int 판 = (اومتوک[ځای] >>> 4) & 0xf;
        int سرۍ_اوږدوالى = (اومتوک[ځای] & 0xf) * 4;
        return 판 == 4 && سرۍ_اوږدوالى >= 20 && اومتوک.length - ځای >= سرۍ_اوږدوالى;
    }

    private static void 범위확인(byte[] اومتوک, int ځغلول, int اوږدوالى_ارزښت) {
        if (اومتوک == null || ځغلول < 0 || اوږدوالى_ارزښت < 0 || ځغلول > اومتوک.length - اوږدوالى_ارزښت) {
            throw new IllegalArgumentException("통신망 اومتوک 범위를 벗어났습니다.");
        }
    }
}

