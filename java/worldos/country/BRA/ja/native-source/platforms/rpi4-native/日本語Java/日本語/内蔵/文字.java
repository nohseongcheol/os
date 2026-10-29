// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** UTF-8 バイト列と UTF-16 文字列を変換する。正規化と組合せ入力は別に扱う。 */
public final class 文字 {
    public static int バイト個数(byte[] データ) { return データ.length; }
    private 文字() {}
    public static int 長さ(String 文) { return 文.length(); }
    public static boolean 等価本文(String 前面値, String 後端値) { return 前面値 == null ? 後端値 == null : 前面値.equals(後端値); }
    public static String 貼付け本文(String 前面値, String 後端値) { return 前面値.concat(後端値); }
    public static String 切断処理値(String 文, int 起動処理, int 終端) { return 文.substring(起動処理, 終端); }
    public static int 整数値解析(String 文) { try { return Integer.parseInt(文); } catch (NumberFormatException エラー) { throw new 番号書式失敗("数値の形式と範囲を確認してください。"); } }
    public static String 整数値値書込(int 数) { return Integer.toString(数); }
    public static int コード点個数(String 文) {
        int 数 = 0;
        for (int ループ添字 = 0; ループ添字 < 文.length(); ループ添字++, 数++) {
            int 文字コード = 文.charAt(ループ添字);
            if (文字コード >= 0xd800 && 文字コード <= 0xdbff && ループ添字 + 1 < 文.length() && 文.charAt(ループ添字 + 1) >= 0xdc00 && 文.charAt(ループ添字 + 1) <= 0xdfff) ループ添字++;
        }
        return 数;
    }
    public static byte[] 符号化(String 文) {
        byte[] 一時値 = new byte[文.length() * 3]; int 書込済み = 0;
        for (int ループ添字 = 0; ループ添字 < 文.length(); ループ添字++) {
            int 文字コード = 文.charAt(ループ添字);
            if (文字コード >= 0xd800 && 文字コード <= 0xdbff && ループ添字 + 1 < 文.length() && 文.charAt(ループ添字 + 1) >= 0xdc00 && 文.charAt(ループ添字 + 1) <= 0xdfff) 文字コード = 0x10000 + ((文字コード - 0xd800) << 10) + 文.charAt(++ループ添字) - 0xdc00;
            else if (文字コード >= 0xd800 && 文字コード <= 0xdfff) 文字コード = '?';
            if (文字コード < 128) 一時値[書込済み++] = (byte)文字コード;
            else if (文字コード < 2048) { 一時値[書込済み++] = (byte)(192 | 文字コード >> 6); 一時値[書込済み++] = (byte)(128 | 文字コード & 63); }
            else if (文字コード < 65536) { 一時値[書込済み++] = (byte)(224 | 文字コード >> 12); 一時値[書込済み++] = (byte)(128 | 文字コード >> 6 & 63); 一時値[書込済み++] = (byte)(128 | 文字コード & 63); }
            else { 一時値[書込済み++] = (byte)(240 | 文字コード >> 18); 一時値[書込済み++] = (byte)(128 | 文字コード >> 12 & 63); 一時値[書込済み++] = (byte)(128 | 文字コード >> 6 & 63); 一時値[書込済み++] = (byte)(128 | 文字コード & 63); }
        }
        byte[] 結果 = new byte[書込済み]; System.arraycopy(一時値, 0, 結果, 0, 書込済み); return 結果;
    }
    /** 不正な UTF-8 は API の不正引数例外で拒否する。 */
    public static String データ復号化(byte[] バイト値) {
        StringBuilder 結果 = new StringBuilder();
        for (int ループ添字 = 0; ループ添字 < バイト値.length;) {
            int 文字コード = バイト値[ループ添字++] & 255, 数 = 文字コード < 128 ? 0 : 文字コード >= 194 && 文字コード < 224 ? 1 : 文字コード >= 224 && 文字コード < 240 ? 2 : 文字コード >= 240 && 文字コード <= 244 ? 3 : -1;
            if (数 < 0 || バイト値.length - ループ添字 < 数) throw new 無効引数例外("不正な UTF-8");
            int 最小値 = 数 == 1 ? 128 : 数 == 2 ? 2048 : 数 == 3 ? 65536 : 0;
            if (数 > 0) 文字コード &= (1 << (6 - 数)) - 1;
            for (int 内側位置 = 0; 内側位置 < 数; 内側位置++) { int 後端値 = バイト値[ループ添字++] & 255; if ((後端値 & 192) != 128) throw new 無効引数例外("不正な UTF-8"); 文字コード = 文字コード << 6 | 後端値 & 63; }
            if (文字コード < 最小値 || 文字コード > 0x10ffff || 文字コード >= 0xd800 && 文字コード <= 0xdfff) throw new 無効引数例外("不正な UTF-8");
            if (文字コード < 65536) 結果.append((char)文字コード);
            else { 文字コード -= 65536; 結果.append((char)(0xd800 | 文字コード >> 10)); 結果.append((char)(0xdc00 | 文字コード & 1023)); }
        }
        return 結果.toString();
    }
}
