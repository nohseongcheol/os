// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.नॅटवर्क_स्टॅक;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 बायट_मोल 순서와 검사합 도구다. */
public final class नॅटवर्क_साधनां {
    private नॅटवर्क_साधनां() {
    }

    public static int 큰순서짧은정수(byte[] डेटा, int स्थिती) {
        범위확인(डेटा, स्थिती, 2);
        return ((डेटा[स्थिती] & 0xff) << 8) | (डेटा[स्थिती + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] डेटा, int स्थिती) {
        범위확인(डेटा, स्थिती, 4);
        return ((long) (डेटा[स्थिती] & 0xff) << 24)
                | ((long) (डेटा[स्थिती + 1] & 0xff) << 16)
                | ((long) (डेटा[स्थिती + 2] & 0xff) << 8)
                | (डेटा[स्थिती + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] डेटा, int चलोवप, int लांबाय_मोल) {
        범위확인(डेटा, चलोवप, लांबाय_मोल);
        long SUM_मोल = 0;
        int 끝 = चलोवप + लांबाय_मोल;
        int स्थिती = चलोवप;
        while (स्थिती + 1 < 끝) {
            SUM_मोल += 큰순서짧은정수(डेटा, स्थिती);
            स्थिती += 2;
        }
        if (स्थिती < 끝) {
            SUM_मोल += (डेटा[स्थिती] & 0xff) << 8;
        }
        while ((SUM_मोल >>> 16) != 0) {
            SUM_मोल = (SUM_मोल & 0xffff) + (SUM_मोल >>> 16);
        }
        return (int) (~SUM_मोल) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] डेटा) {
        return डेटा != null && डेटा.length >= 14;
    }

    public static int इथरनॅट_UPPER_प्रोटोकॉल(byte[] डेटा) {
        if (!이더넷틀인가(डेटा)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(डेटा, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] डेटा, int स्थिती) {
        if (डेटा == null || स्थिती < 0 || डेटा.length - स्थिती < 20) {
            return false;
        }
        int वर्जन_मोल = (डेटा[स्थिती] >>> 4) & 0xf;
        int माथाळो_लांबाय = (डेटा[स्थिती] & 0xf) * 4;
        return वर्जन_मोल == 4 && माथाळो_लांबाय >= 20 && डेटा.length - स्थिती >= माथाळो_लांबाय;
    }

    private static void 범위확인(byte[] डेटा, int चलोवप, int लांबाय_मोल) {
        if (डेटा == null || चलोवप < 0 || लांबाय_मोल < 0 || चलोवप > डेटा.length - लांबाय_मोल) {
            throw new IllegalArgumentException("नॅटवर्क_स्टॅक डेटा 범위를 벗어났습니다.");
        }
    }
}

