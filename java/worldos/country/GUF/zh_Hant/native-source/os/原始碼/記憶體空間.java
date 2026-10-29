// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 查詢啟動資訊，配置與釋放固定 4 KiB 工作區域；不是通用實體頁管理器。 */
public final class 記憶體空間 {
    static int[] 區段值 = new int[8192];
    static int[] 使用值 = new int[8];

    static int 解析整數(int 地址) {
        return 設備.讀取記憶體(地址) | (設備.讀取記憶體(地址 + 1) << 8)
            | (設備.讀取記憶體(地址 + 2) << 16) | (設備.讀取記憶體(地址 + 3) << 24);
    }

    static int 上位側記憶體大小() {
        int 系統信息 = 設備.啓動信息();
        if (設備.啓動標記() != 0x2badb002 || 系統信息 == 0 || (解析整數(系統信息) & 1) == 0) return -1;
        return 解析整數(系統信息 + 8);
    }

    static int 分配存儲裝置() {
        for (int 編號 = 0; 編號 < 使用值.length; 編號++) {
            if (使用值[編號] == 0) {
                使用值[編號] = 1;
                for (int 槽條目 = 0; 槽條目 < 1024; 槽條目++) 區段值[編號 * 1024 + 槽條目] = 0;
                return 編號;
            }
        }
        return -1;
    }

    static boolean 發回結果(int 編號) {
        if (編號 < 0 || 編號 >= 使用值.length || 使用值[編號] == 0) return false;
        使用值[編號] = 0;
        return true;
    }

    static int 已使用條目個數() {
        int 項目個數 = 0;
        for (int 編號 = 0; 編號 < 使用值.length; 編號++) 項目個數 += 使用值[編號];
        return 項目個數;
    }
}
