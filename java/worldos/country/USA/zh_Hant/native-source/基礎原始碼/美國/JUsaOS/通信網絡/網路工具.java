// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 美國.JUsaOS.通信網絡;

/** Ethernet/ARP/IPv4/ICMP/UDP 層共用的位元組順序與總和檢查碼工具。 */
public final class 網路工具 {
    private 網路工具() {
    }

    public static int 大字節序短整數(byte[] 資料, int 位置) {
        檢查範圍(資料, 位置, 2);
        return ((資料[位置] & 0xff) << 8) | (資料[位置 + 1] & 0xff);
    }

    public static long 大字節序整數(byte[] 資料, int 位置) {
        檢查範圍(資料, 位置, 4);
        return ((long) (資料[位置] & 0xff) << 24)
                | ((long) (資料[位置 + 1] & 0xff) << 16)
                | ((long) (資料[位置 + 2] & 0xff) << 8)
                | (資料[位置 + 3] & 0xffL);
    }

    public static int 互聯網校驗和(byte[] 資料, int 運行, int 長度) {
        檢查範圍(資料, 運行, 長度);
        long 總和值 = 0;
        int 結尾 = 運行 + 長度;
        int 位置 = 運行;
        while (位置 + 1 < 結尾) {
            總和值 += 大字節序短整數(資料, 位置);
            位置 += 2;
        }
        if (位置 < 結尾) {
            總和值 += (資料[位置] & 0xff) << 8;
        }
        while ((總和值 >>> 16) != 0) {
            總和值 = (總和值 & 0xffff) + (總和值 >>> 16);
        }
        return (int) (~總和值) & 0xffff;
    }

    public static boolean 是否以太網幀(byte[] 資料) {
        return 資料 != null && 資料.length >= 14;
    }

    public static int 以太網上位側通訊協定(byte[] 資料) {
        if (!是否以太網幀(資料)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 大字節序短整數(資料, 12);
    }

    public static boolean 是否IP版本4通訊協定(byte[] 資料, int 位置) {
        if (資料 == null || 位置 < 0 || 資料.length - 位置 < 20) {
            return false;
        }
        int 版本值 = (資料[位置] >>> 4) & 0xf;
        int 標頭長度 = (資料[位置] & 0xf) * 4;
        return 版本值 == 4 && 標頭長度 >= 20 && 資料.length - 位置 >= 標頭長度;
    }

    private static void 檢查範圍(byte[] 資料, int 運行, int 長度) {
        if (資料 == null || 運行 < 0 || 長度 < 0 || 運行 > 資料.length - 長度) {
            throw new IllegalArgumentException("通信網絡 資料 범위를 벗어났습니다.");
        }
    }
}

