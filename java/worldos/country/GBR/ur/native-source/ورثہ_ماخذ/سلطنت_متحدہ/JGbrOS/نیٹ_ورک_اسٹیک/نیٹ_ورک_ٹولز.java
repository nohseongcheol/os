// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package سلطنت_متحدہ.JGbrOS.نیٹ_ورک_اسٹیک;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بائٹ_قدر 순서와 میزان_کی_جانچ_کرنا 도구다. */
public final class نیٹ_ورک_ٹولز {
    private نیٹ_ورک_ٹولز() {
    }

    public static int 큰순서짧은정수(byte[] کوائف, int مقام) {
        범위확인(کوائف, مقام, 2);
        return ((کوائف[مقام] & 0xff) << 8) | (کوائف[مقام + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] کوائف, int مقام) {
        범위확인(کوائف, مقام, 4);
        return ((long) (کوائف[مقام] & 0xff) << 24)
                | ((long) (کوائف[مقام + 1] & 0xff) << 16)
                | ((long) (کوائف[مقام + 2] & 0xff) << 8)
                | (کوائف[مقام + 3] & 0xffL);
    }

    public static int بادل_میزان_کی_جانچ_کرنا(byte[] کوائف, int چلائیں, int لمبا_ئی_قدر) {
        범위확인(کوائف, چلائیں, لمبا_ئی_قدر);
        long 합 = 0;
        int 끝 = چلائیں + لمبا_ئی_قدر;
        int مقام = چلائیں;
        while (مقام + 1 < 끝) {
            합 += 큰순서짧은정수(کوائف, مقام);
            مقام += 2;
        }
        if (مقام < 끝) {
            합 += (کوائف[مقام] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean معلومات_ٹیکنالوجی_ایتھرنیٹ_فریم(byte[] کوائف) {
        return کوائف != null && کوائف.length >= 14;
    }

    public static int 이더넷상위규약(byte[] کوائف) {
        if (!معلومات_ٹیکنالوجی_ایتھرنیٹ_فریم(کوائف)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(کوائف, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] کوائف, int مقام) {
        if (کوائف == null || مقام < 0 || کوائف.length - مقام < 20) {
            return false;
        }
        int ورژن_قدر = (کوائف[مقام] >>> 4) & 0xf;
        int سرصفحہ_لمبا_ئی = (کوائف[مقام] & 0xf) * 4;
        return ورژن_قدر == 4 && سرصفحہ_لمبا_ئی >= 20 && کوائف.length - مقام >= سرصفحہ_لمبا_ئی;
    }

    private static void 범위확인(byte[] کوائف, int چلائیں, int لمبا_ئی_قدر) {
        if (کوائف == null || چلائیں < 0 || لمبا_ئی_قدر < 0 || چلائیں > کوائف.length - لمبا_ئی_قدر) {
            throw new IllegalArgumentException("نیٹ_ورک_اسٹیک کوائف 범위를 벗어났습니다.");
        }
    }
}

