// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 初始網路層：單一核心中的 IPv4/UDP 回送傳輸。外部 IP 回傳 ENETUNREACH，不取代 Ethernet/IP 封包驅動程式。8 個端點，每個端點容納 4 個資料報，每個資料報 512 位元組。所有呼叫均不阻塞。 */
public final class 環回網路 {
    static int[] 使用值 = new int[8];
    static int[] 埠值 = new int[8];
    static int[] 地址 = new int[8];
    static int[] 前端值 = new int[8];
    static int[] 項目個數 = new int[8];
    static int[] 已接收埠 = new int[8];
    static int[] 長度 = new int[32];
    static int[] 已發送埠 = new int[32];
    static int[] 資料 = new int[32 * 512];
    static int[] 前向值 = new int[512];
    static int 下一端點 = 49152;
    static int 驗證(int 編號) { return 編號 >= 32 && 編號 < 40 && 使用值[編號 - 32] != 0 ? 編號 - 32 : -1; }
    static boolean 重疊區列(int 編號) {
        for (int 槽條目 = 0; 槽條目 < 8; 槽條目++) if (使用值[槽條目] != 0 && 埠值[槽條目] == 編號) return true;
        return false;
    }
    static int 臨時埠() {
        for (int 嘗試值 = 0; 嘗試值 < 16; 嘗試值++) {
            int 候選 = 下一端點++;
            if (下一端點 > 65535) 下一端點 = 49152;
            if (!重疊區列(候選)) return 候選;
        }
        return -98;
    }
    public static int 創建條目(int 區域值, int 種類值, int 契約值) {
        if (區域值 != 2) return -97;
        if (種類值 != 2 || (契約值 != 0 && 契約值 != 17)) return -93;
        for (int 槽條目 = 0; 槽條目 < 8; 槽條目++) if (使用值[槽條目] == 0) {
            使用值[槽條目] = 1; 埠值[槽條目] = 0; 地址[槽條目] = 0; 前端值[槽條目] = 0; 項目個數[槽條目] = 0; 已接收埠[槽條目] = 0;
            return 槽條目 + 32;
        }
        return -24;
    }
    public static int 可執行束打包(int 編號, int 網路地址, int 端點埠編號) {
        int 槽條目 = 驗證(編號);
        if (槽條目 < 0) return -9;
        if (網路地址 != 0 && 網路地址 != 0x7f000001) return -99;
        if (埠值[槽條目] != 0 || 端點埠編號 < 0 || 端點埠編號 > 65535) return -22;
        if (端點埠編號 == 0) 端點埠編號 = 臨時埠();
        if (端點埠編號 < 0) return 端點埠編號;
        if (重疊區列(端點埠編號)) return -98;
        埠值[槽條目] = 端點埠編號; 地址[槽條目] = 網路地址; return 0;
    }
    public static int 放入資料(int 編號, int 值) {
        if (編號 < 0 || 編號 >= 512) return -22;
        前向值[編號] = 值 & 255; return 0;
    }
    public static int 讀取資料(int 編號) { return 編號 >= 0 && 編號 < 512 ? 前向值[編號] : -22; }
    public static int 發送(int 編號, int 網路地址, int 端點埠編號, int 大小) {
        int 槽條目 = 驗證(編號);
        if (槽條目 < 0) return -9;
        if (網路地址 != 0x7f000001) return -101;
        if (端點埠編號 < 1 || 端點埠編號 > 65535) return -22;
        if (大小 < 0 || 大小 > 512) return -90;
        if (埠值[槽條目] == 0) {
            int 結果 = 可執行束打包(編號, 0x7f000001, 0);
            if (結果 < 0) return 結果;
        }
        int 目的地址值 = -1;
        for (int 候選 = 0; 候選 < 8; 候選++) if (使用值[候選] != 0 && 埠值[候選] == 端點埠編號) 目的地址值 = 候選;
        if (目的地址值 < 0) return -111;
        if (項目個數[目的地址值] == 4) return -11;
        int 位置索引 = 目的地址值 * 4 + (前端值[目的地址值] + 項目個數[目的地址值]) % 4;
        for (int 位元組值 = 0; 位元組值 < 大小; 位元組值++) 資料[位置索引 * 512 + 位元組值] = 前向值[位元組值];
        長度[位置索引] = 大小; 已發送埠[位置索引] = 埠值[槽條目]; 項目個數[目的地址值]++;
        return 大小;
    }
    public static int 接收(int 編號, int 容量值) {
        int 槽條目 = 驗證(編號);
        if (槽條目 < 0) return -9;
        if (容量值 < 0 || 容量值 > 512) return -22;
        if (項目個數[槽條目] == 0) return -11;
        int 位置索引 = 槽條目 * 4 + 前端值[槽條目];
        int 大小 = 長度[位置索引] < 容量值 ? 長度[位置索引] : 容量值;
        for (int 位元組值 = 0; 位元組值 < 大小; 位元組值++) 前向值[位元組值] = 資料[位置索引 * 512 + 位元組值];
        已接收埠[槽條目] = 已發送埠[位置索引]; 前端值[槽條目] = (前端值[槽條目] + 1) % 4; 項目個數[槽條目]--;
        return 大小;
    }
    public static int 讀取端點埠(int 編號) { int 槽條目 = 驗證(編號); return 槽條目 < 0 ? -9 : 埠值[槽條目]; }
    public static int 讀取地址(int 編號) { int 槽條目 = 驗證(編號); return 槽條目 < 0 ? -9 : 地址[槽條目]; }
    public static int 發送方端點(int 編號) { int 槽條目 = 驗證(編號); return 槽條目 < 0 ? -9 : 已接收埠[槽條目]; }
    public static int 關閉(int 編號) {
        int 槽條目 = 驗證(編號); if (槽條目 < 0) return -9;
        使用值[槽條目] = 0; 項目個數[槽條目] = 0; 埠值[槽條目] = 0; return 0;
    }
}
