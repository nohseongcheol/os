// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.通信網;

/** Ethernet/ARP/IPv4/ICMP/UDP 層で共有するバイト順序と検査和の道具。 */
public final class 通信網道具 {
    private 通信網道具() {
    }

    public static int 大エンディアン短整数(byte[] データ, int 位置) {
        範囲検査(データ, 位置, 2);
        return ((データ[位置] & 0xff) << 8) | (データ[位置 + 1] & 0xff);
    }

    public static long 大エンディアン整数値(byte[] データ, int 位置) {
        範囲検査(データ, 位置, 4);
        return ((long) (データ[位置] & 0xff) << 24)
                | ((long) (データ[位置 + 1] & 0xff) << 16)
                | ((long) (データ[位置 + 2] & 0xff) << 8)
                | (データ[位置 + 3] & 0xffL);
    }

    public static int インターネット検査和(byte[] データ, int 起動処理, int 長さ) {
        範囲検査(データ, 起動処理, 長さ);
        long 総和値 = 0;
        int 終端 = 起動処理 + 長さ;
        int 位置 = 起動処理;
        while (位置 + 1 < 終端) {
            総和値 += 大エンディアン短整数(データ, 位置);
            位置 += 2;
        }
        if (位置 < 終端) {
            総和値 += (データ[位置] & 0xff) << 8;
        }
        while ((総和値 >>> 16) != 0) {
            総和値 = (総和値 & 0xffff) + (総和値 >>> 16);
        }
        return (int) (~総和値) & 0xffff;
    }

    public static boolean 判定Ethernet枠組(byte[] データ) {
        return データ != null && データ.length >= 14;
    }

    public static int Ethernet上限側通信規約(byte[] データ) {
        if (!判定Ethernet枠組(データ)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 大エンディアン短整数(データ, 12);
    }

    public static boolean 判定IP版4通信規約(byte[] データ, int 位置) {
        if (データ == null || 位置 < 0 || データ.length - 位置 < 20) {
            return false;
        }
        int 版値 = (データ[位置] >>> 4) & 0xf;
        int ヘッダー長さ = (データ[位置] & 0xf) * 4;
        return 版値 == 4 && ヘッダー長さ >= 20 && データ.length - 位置 >= ヘッダー長さ;
    }

    private static void 範囲検査(byte[] データ, int 起動処理, int 長さ) {
        if (データ == null || 起動処理 < 0 || 長さ < 0 || 起動処理 > データ.length - 長さ) {
            throw new IllegalArgumentException("通信網 データ 범위를 벗어났습니다.");
        }
    }
}

