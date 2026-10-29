// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.ファイルシステム;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR の四つの基本区画を読む。 */
public final class 主分割表 {
    public static final class 分割値 {
        private final int 種別値;
        private final long 区画開始処理;
        private final long 区画個数;

        分割値(int 種別値, long 区画開始処理, long 区画個数) {
            this.種別値 = 種別値;
            this.区画開始処理 = 区画開始処理;
            this.区画個数 = 区画個数;
        }

        public int 種別値() { return 種別値; }
        public long 区画開始処理() { return 区画開始処理; }
        public long 区画個数() { return 区画個数; }
    }

    public List<分割値> 読取(byte[] 先頭位置区画) {
        if (先頭位置区画 == null || 先頭位置区画.length < 512
                || (先頭位置区画[510] & 0xff) != 0x55 || (先頭位置区画[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<分割値> 結果 = new ArrayList<分割値>();
        for (int 番号 = 0; 番号 < 4; 番号++) {
            int 位置 = 446 + 番号 * 16;
            int 種別値 = 先頭位置区画[位置 + 4] & 0xff;
            long 起動処理 = 小エンディアン整数値(先頭位置区画, 位置 + 8);
            long 容量 = 小エンディアン整数値(先頭位置区画, 位置 + 12);
            if (種別値 != 0 && 容量 != 0) {
                結果.add(new 分割値(種別値, 起動処理, 容量));
            }
        }
        return Collections.unmodifiableList(結果);
    }

    private long 小エンディアン整数値(byte[] データ, int 位置) {
        return (データ[位置] & 0xffL)
                | ((データ[位置 + 1] & 0xffL) << 8)
                | ((データ[位置 + 2] & 0xffL) << 16)
                | ((データ[位置 + 3] & 0xffL) << 24);
    }
}

