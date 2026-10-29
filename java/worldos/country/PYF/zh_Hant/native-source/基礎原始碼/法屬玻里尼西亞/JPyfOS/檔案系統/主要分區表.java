// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 法屬玻里尼西亞.JPyfOS.檔案系統;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 讀取 DOS MBR 的四個主要分割區。 */
public final class 主要分區表 {
    public static final class 分區值 {
        private final int 種類值;
        private final long 開始區段;
        private final long 區段個數;

        分區值(int 種類值, long 開始區段, long 區段個數) {
            this.種類值 = 種類值;
            this.開始區段 = 開始區段;
            this.區段個數 = 區段個數;
        }

        public int 種類值() { return 種類值; }
        public long 開始區段() { return 開始區段; }
        public long 區段個數() { return 區段個數; }
    }

    public List<分區值> 讀取(byte[] 首位區段) {
        if (首位區段 == null || 首位區段.length < 512
                || (首位區段[510] & 0xff) != 0x55 || (首位區段[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<分區值> 結果 = new ArrayList<分區值>();
        for (int 編號 = 0; 編號 < 4; 編號++) {
            int 位置 = 446 + 編號 * 16;
            int 種類值 = 首位區段[位置 + 4] & 0xff;
            long 運行 = 小字節序整數(首位區段, 位置 + 8);
            long 大小 = 小字節序整數(首位區段, 位置 + 12);
            if (種類值 != 0 && 大小 != 0) {
                結果.add(new 分區值(種類值, 運行, 大小));
            }
        }
        return Collections.unmodifiableList(結果);
    }

    private long 小字節序整數(byte[] 資料, int 位置) {
        return (資料[位置] & 0xffL)
                | ((資料[位置 + 1] & 0xffL) << 8)
                | ((資料[位置 + 2] & 0xffL) << 16)
                | ((資料[位置 + 3] & 0xffL) << 24);
    }
}

