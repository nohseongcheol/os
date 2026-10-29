// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.רשת_רמז;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 בית_ערך 순서와 בדיקת_סיכום 도구다. */
public final class רשת_כלים {
    private רשת_כלים() {
    }

    public static int 큰순서짧은정수(byte[] נתונים, int מיקום) {
        שיק_טווח(נתונים, מיקום, 2);
        return ((נתונים[מיקום] & 0xff) << 8) | (נתונים[מיקום + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] נתונים, int מיקום) {
        שיק_טווח(נתונים, מיקום, 4);
        return ((long) (נתונים[מיקום] & 0xff) << 24)
                | ((long) (נתונים[מיקום + 1] & 0xff) << 16)
                | ((long) (נתונים[מיקום + 2] & 0xff) << 8)
                | (נתונים[מיקום + 3] & 0xffL);
    }

    public static int ענן_בדיקת_סיכום(byte[] נתונים, int הפעלה, int 길이) {
        שיק_טווח(נתונים, הפעלה, 길이);
        long 합 = 0;
        int 끝 = הפעלה + 길이;
        int מיקום = הפעלה;
        while (מיקום + 1 < 끝) {
            합 += 큰순서짧은정수(נתונים, מיקום);
            מיקום += 2;
        }
        if (מיקום < 끝) {
            합 += (נתונים[מיקום] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean 이더넷틀인가(byte[] נתונים) {
        return נתונים != null && נתונים.length >= 14;
    }

    public static int 이더넷상위규약(byte[] נתונים) {
        if (!이더넷틀인가(נתונים)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(נתונים, 12);
    }

    public static boolean מערכות_מידע_חיסון_נגד_פוליו_4_פרוטוקול(byte[] נתונים, int מיקום) {
        if (נתונים == null || מיקום < 0 || נתונים.length - מיקום < 20) {
            return false;
        }
        int גירסה_ערך = (נתונים[מיקום] >>> 4) & 0xf;
        int 머리길이 = (נתונים[מיקום] & 0xf) * 4;
        return גירסה_ערך == 4 && 머리길이 >= 20 && נתונים.length - מיקום >= 머리길이;
    }

    private static void שיק_טווח(byte[] נתונים, int הפעלה, int 길이) {
        if (נתונים == null || הפעלה < 0 || 길이 < 0 || הפעלה > נתונים.length - 길이) {
            throw new IllegalArgumentException("רשת_רמז נתונים 범위를 벗어났습니다.");
        }
    }
}

