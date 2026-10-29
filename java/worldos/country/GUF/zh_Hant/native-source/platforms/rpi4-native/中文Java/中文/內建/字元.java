// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中文.內建;
/** 在 UTF-8 位元組與 UTF-16 字串之間轉換；正規化與組合輸入另行處理。 */
public final class 字元 {
    public static int 位元組個數(byte[] 資料) { return 資料.length; }
    private 字元() {}
    public static int 長度(String 文本) { return 文本.length(); }
    public static boolean 相等文本(String 前端值, String 後端值) { return 前端值 == null ? 後端值 == null : 前端值.equals(後端值); }
    public static String 粘貼文本(String 前端值, String 後端值) { return 前端值.concat(後端值); }
    public static String 剪切值(String 文本, int 運行, int 結尾) { return 文本.substring(運行, 結尾); }
    public static int 解析整數(String 文本) { try { return Integer.parseInt(文本); } catch (NumberFormatException 錯誤) { throw new 編號格式失敗("請檢查數字格式和範圍。"); } }
    public static String 寫入整數值(int 數) { return Integer.toString(數); }
    public static int 程式碼分個數(String 文本) {
        int 數 = 0;
        for (int 循環索引 = 0; 循環索引 < 文本.length(); 循環索引++, 數++) {
            int 字元程式碼 = 文本.charAt(循環索引);
            if (字元程式碼 >= 0xd800 && 字元程式碼 <= 0xdbff && 循環索引 + 1 < 文本.length() && 文本.charAt(循環索引 + 1) >= 0xdc00 && 文本.charAt(循環索引 + 1) <= 0xdfff) 循環索引++;
        }
        return 數;
    }
    public static byte[] 編碼(String 文本) {
        byte[] 臨時值 = new byte[文本.length() * 3]; int 已寫入 = 0;
        for (int 循環索引 = 0; 循環索引 < 文本.length(); 循環索引++) {
            int 字元程式碼 = 文本.charAt(循環索引);
            if (字元程式碼 >= 0xd800 && 字元程式碼 <= 0xdbff && 循環索引 + 1 < 文本.length() && 文本.charAt(循環索引 + 1) >= 0xdc00 && 文本.charAt(循環索引 + 1) <= 0xdfff) 字元程式碼 = 0x10000 + ((字元程式碼 - 0xd800) << 10) + 文本.charAt(++循環索引) - 0xdc00;
            else if (字元程式碼 >= 0xd800 && 字元程式碼 <= 0xdfff) 字元程式碼 = '?';
            if (字元程式碼 < 128) 臨時值[已寫入++] = (byte)字元程式碼;
            else if (字元程式碼 < 2048) { 臨時值[已寫入++] = (byte)(192 | 字元程式碼 >> 6); 臨時值[已寫入++] = (byte)(128 | 字元程式碼 & 63); }
            else if (字元程式碼 < 65536) { 臨時值[已寫入++] = (byte)(224 | 字元程式碼 >> 12); 臨時值[已寫入++] = (byte)(128 | 字元程式碼 >> 6 & 63); 臨時值[已寫入++] = (byte)(128 | 字元程式碼 & 63); }
            else { 臨時值[已寫入++] = (byte)(240 | 字元程式碼 >> 18); 臨時值[已寫入++] = (byte)(128 | 字元程式碼 >> 12 & 63); 臨時值[已寫入++] = (byte)(128 | 字元程式碼 >> 6 & 63); 臨時值[已寫入++] = (byte)(128 | 字元程式碼 & 63); }
        }
        byte[] 結果 = new byte[已寫入]; System.arraycopy(臨時值, 0, 結果, 0, 已寫入); return 結果;
    }
    /** 以 API 的無效引數例外拒絕格式錯誤的 UTF-8。 */
    public static String 解密資料(byte[] 位元組值) {
        StringBuilder 結果 = new StringBuilder();
        for (int 循環索引 = 0; 循環索引 < 位元組值.length;) {
            int 字元程式碼 = 位元組值[循環索引++] & 255, 數 = 字元程式碼 < 128 ? 0 : 字元程式碼 >= 194 && 字元程式碼 < 224 ? 1 : 字元程式碼 >= 224 && 字元程式碼 < 240 ? 2 : 字元程式碼 >= 240 && 字元程式碼 <= 244 ? 3 : -1;
            if (數 < 0 || 位元組值.length - 循環索引 < 數) throw new 無效實際參數異常("無效的 UTF-8");
            int 最小值 = 數 == 1 ? 128 : 數 == 2 ? 2048 : 數 == 3 ? 65536 : 0;
            if (數 > 0) 字元程式碼 &= (1 << (6 - 數)) - 1;
            for (int 內部側位置 = 0; 內部側位置 < 數; 內部側位置++) { int 後端值 = 位元組值[循環索引++] & 255; if ((後端值 & 192) != 128) throw new 無效實際參數異常("無效的 UTF-8"); 字元程式碼 = 字元程式碼 << 6 | 後端值 & 63; }
            if (字元程式碼 < 最小值 || 字元程式碼 > 0x10ffff || 字元程式碼 >= 0xd800 && 字元程式碼 <= 0xdfff) throw new 無效實際參數異常("無效的 UTF-8");
            if (字元程式碼 < 65536) 結果.append((char)字元程式碼);
            else { 字元程式碼 -= 65536; 結果.append((char)(0xd800 | 字元程式碼 >> 10)); 結果.append((char)(0xdc00 | 字元程式碼 & 1023)); }
        }
        return 結果.toString();
    }
}
