// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عمان.JOmnOS.شبکه_پشته;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 بایت_مقدار 순서와 مجموع_مقابله_ای 도구다. */
public final class شبکه_ابزارها {
    private شبکه_ابزارها() {
    }

    public static int 큰순서짧은정수(byte[] داده_ها, int مرتب_کردن) {
        범위확인(داده_ها, مرتب_کردن, 2);
        return ((داده_ها[مرتب_کردن] & 0xff) << 8) | (داده_ها[مرتب_کردن + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] داده_ها, int مرتب_کردن) {
        범위확인(داده_ها, مرتب_کردن, 4);
        return ((long) (داده_ها[مرتب_کردن] & 0xff) << 24)
                | ((long) (داده_ها[مرتب_کردن + 1] & 0xff) << 16)
                | ((long) (داده_ها[مرتب_کردن + 2] & 0xff) << 8)
                | (داده_ها[مرتب_کردن + 3] & 0xffL);
    }

    public static int ابری_مجموع_مقابله_ای(byte[] داده_ها, int اجرا_2, int طول_مقدار) {
        범위확인(داده_ها, اجرا_2, طول_مقدار);
        long 합 = 0;
        int 끝 = اجرا_2 + طول_مقدار;
        int مرتب_کردن = اجرا_2;
        while (مرتب_کردن + 1 < 끝) {
            합 += 큰순서짧은정수(داده_ها, مرتب_کردن);
            مرتب_کردن += 2;
        }
        if (مرتب_کردن < 끝) {
            합 += (داده_ها[مرتب_کردن] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean فناوری_اطلاعات_اترنت_قاب(byte[] داده_ها) {
        return داده_ها != null && داده_ها.length >= 14;
    }

    public static int 이더넷상위규약(byte[] داده_ها) {
        if (!فناوری_اطلاعات_اترنت_قاب(داده_ها)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(داده_ها, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] داده_ها, int مرتب_کردن) {
        if (داده_ها == null || مرتب_کردن < 0 || داده_ها.length - مرتب_کردن < 20) {
            return false;
        }
        int نسخه_مقدار = (داده_ها[مرتب_کردن] >>> 4) & 0xf;
        int سرصفحه_طول = (داده_ها[مرتب_کردن] & 0xf) * 4;
        return نسخه_مقدار == 4 && سرصفحه_طول >= 20 && داده_ها.length - مرتب_کردن >= سرصفحه_طول;
    }

    private static void 범위확인(byte[] داده_ها, int اجرا_2, int طول_مقدار) {
        if (داده_ها == null || اجرا_2 < 0 || طول_مقدار < 0 || اجرا_2 > داده_ها.length - طول_مقدار) {
            throw new IllegalArgumentException("شبکه_پشته داده_ها 범위를 벗어났습니다.");
        }
    }
}

