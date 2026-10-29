// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 法屬玻里尼西亞.JPyfOS.檔案系統;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 驗證小端序 ELF32 執行檔的標頭與載入區段。 */
public final class 可執行文件加載器 {
    public static final class 區段值 {
        private final int 種類值;
        private final int 標誌值;
        private final int 地址;
        private final int 檔案位置;
        private final int 大小;

        區段值(int 種類值, int 標誌值, int 地址, int 檔案位置, int 大小) {
            this.種類值 = 種類值;
            this.標誌值 = 標誌值;
            this.地址 = 地址;
            this.檔案位置 = 檔案位置;
            this.大小 = 大小;
        }

        public int 種類值() {
            return 種類值;
        }

        public int 標誌值() {
            return 標誌值;
        }

        public int 地址() {
            return 地址;
        }

        public int 檔案位置() {
            return 檔案位置;
        }

        public int 大小() {
            return 大小;
        }
    }

    public static final class 映像 {
        private final int 開始地址;
        private final List<區段值> 區段列列表;

        映像(int 開始地址, List<區段值> 區段列列表) {
            this.開始地址 = 開始地址;
            this.區段列列表 = Collections.unmodifiableList(區段列列表);
        }

        public int 開始地址() {
            return 開始地址;
        }

        public List<區段值> 區段列列表() {
            return 區段列列表;
        }
    }

    public 映像 檢查項(byte[] 資料) {
        if (資料 == null || 資料.length < 52
                || 資料[0] != 0x7f || 資料[1] != 'E' || 資料[2] != 'L' || 資料[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (資料[4] != 1 || 資料[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int 開始地址 = 解析整數(資料, 24);
        int 區段表位置 = 解析整數(資料, 32);
        int 區段條目大小 = 讀取短整數整數(資料, 46);
        int 區段個數 = 讀取短整數整數(資料, 48);
        if (區段條目大小 < 40 || 區段表位置 < 0
                || (long) 區段表位置 + (long) 區段條目大小 * 區段個數 > 資料.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<區段值> 區段列列表 = new ArrayList<區段值>();
        for (int 編號 = 0; 編號 < 區段個數; 編號++) {
            int 位置 = 區段表位置 + 編號 * 區段條目大小;
            int 種類值 = 解析整數(資料, 位置 + 4);
            int 標誌值 = 解析整數(資料, 位置 + 8);
            int 地址 = 解析整數(資料, 位置 + 12);
            int 檔案位置 = 解析整數(資料, 位置 + 16);
            int 大小 = 解析整數(資料, 位置 + 20);
            if (大小 < 0 || (種類值 != 8 && ((long) 檔案位置 + 大小 > 資料.length || 檔案位置 < 0))) {
                throw new IllegalArgumentException("ELF 區段值 資料 범위가 올바르지 않습니다.");
            }
            區段列列表.add(new 區段值(種類值, 標誌值, 地址, 檔案位置, 大小));
        }
        return new 映像(開始地址, 區段列列表);
    }

    private int 解析整數(byte[] 資料, int 位置) {
        if (位置 < 0 || 位置 > 資料.length - 4) {
            throw new IllegalArgumentException("ELF 整數 범위를 벗어났습니다.");
        }
        return (資料[位置] & 0xff)
                | ((資料[位置 + 1] & 0xff) << 8)
                | ((資料[位置 + 2] & 0xff) << 16)
                | ((資料[位置 + 3] & 0xff) << 24);
    }

    private int 讀取短整數整數(byte[] 資料, int 位置) {
        if (位置 < 0 || 位置 > 資料.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 整數 범위를 벗어났습니다.");
        }
        return (資料[位置] & 0xff) | ((資料[位置 + 1] & 0xff) << 8);
    }
}
