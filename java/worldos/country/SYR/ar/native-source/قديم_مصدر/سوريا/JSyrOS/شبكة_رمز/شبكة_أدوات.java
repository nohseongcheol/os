// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package سوريا.JSyrOS.شبكة_رمز;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بايت_قيمة 순서와 مجموع_اختباري 도구다. */
public final class شبكة_أدوات {
    private شبكة_أدوات() {
    }

    public static int 큰순서짧은정수(byte[] بيانات, int موضع) {
        شيك_نطاق(بيانات, موضع, 2);
        return ((بيانات[موضع] & 0xff) << 8) | (بيانات[موضع + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] بيانات, int موضع) {
        شيك_نطاق(بيانات, موضع, 4);
        return ((long) (بيانات[موضع] & 0xff) << 24)
                | ((long) (بيانات[موضع + 1] & 0xff) << 16)
                | ((long) (بيانات[موضع + 2] & 0xff) << 8)
                | (بيانات[موضع + 3] & 0xffL);
    }

    public static int سحابة_مجموع_اختباري(byte[] بيانات, int تشغيل, int 길이) {
        شيك_نطاق(بيانات, تشغيل, 길이);
        long 합 = 0;
        int 끝 = تشغيل + 길이;
        int موضع = تشغيل;
        while (موضع + 1 < 끝) {
            합 += 큰순서짧은정수(بيانات, موضع);
            موضع += 2;
        }
        if (موضع < 끝) {
            합 += (بيانات[موضع] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] بيانات) {
        return بيانات != null && بيانات.length >= 14;
    }

    public static int 이더넷상위규약(byte[] بيانات) {
        if (!이더넷틀인가(بيانات)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(بيانات, 12);
    }

    public static boolean أنظمة_المعلومات_لقاح_شلل_الأطفال_4_بروتوكول(byte[] بيانات, int موضع) {
        if (بيانات == null || موضع < 0 || بيانات.length - موضع < 20) {
            return false;
        }
        int إصدار_قيمة = (بيانات[موضع] >>> 4) & 0xf;
        int 머리길이 = (بيانات[موضع] & 0xf) * 4;
        return إصدار_قيمة == 4 && 머리길이 >= 20 && بيانات.length - موضع >= 머리길이;
    }

    private static void شيك_نطاق(byte[] بيانات, int تشغيل, int 길이) {
        if (بيانات == null || تشغيل < 0 || 길이 < 0 || تشغيل > بيانات.length - 길이) {
            throw new IllegalArgumentException("شبكة_رمز بيانات 범위를 벗어났습니다.");
        }
    }
}

