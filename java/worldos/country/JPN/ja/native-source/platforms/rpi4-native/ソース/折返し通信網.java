// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 初期ネットワーク層。単一カーネル内の IPv4/UDP ループバック通信。外部 IP は ENETUNREACH を返す。Ethernet/IP パケットドライバーの代わりではない。端点8個、各端点に電文4個、各電文512バイト。呼出しはすべて非待機式。 */
public final class 折返し通信網 {
    static int[] 使用値 = new int[8];
    static int[] ポート値 = new int[8];
    static int[] 番地 = new int[8];
    static int[] 前面値 = new int[8];
    static int[] 項目個数 = new int[8];
    static int[] 受信済みポート = new int[8];
    static int[] 長さ = new int[32];
    static int[] 送信済みポート = new int[32];
    static int[] データ = new int[32 * 512];
    static int[] 前方値 = new int[512];
    static int 次回通信端点 = 49152;
    static int 検証(int 番号) { return 番号 >= 32 && 番号 < 40 && 使用値[番号 - 32] != 0 ? 番号 - 32 : -1; }
    static boolean 重複範囲(int 番号) {
        for (int 槽入口 = 0; 槽入口 < 8; 槽入口++) if (使用値[槽入口] != 0 && ポート値[槽入口] == 番号) return true;
        return false;
    }
    static int 一時ポート() {
        for (int 試行値 = 0; 試行値 < 16; 試行値++) {
            int 候補 = 次回通信端点++;
            if (次回通信端点 > 65535) 次回通信端点 = 49152;
            if (!重複範囲(候補)) return 候補;
        }
        return -98;
    }
    public static int 入口作成(int 領域値, int 種別値, int 契約値) {
        if (領域値 != 2) return -97;
        if (種別値 != 2 || (契約値 != 0 && 契約値 != 17)) return -93;
        for (int 槽入口 = 0; 槽入口 < 8; 槽入口++) if (使用値[槽入口] == 0) {
            使用値[槽入口] = 1; ポート値[槽入口] = 0; 番地[槽入口] = 0; 前面値[槽入口] = 0; 項目個数[槽入口] = 0; 受信済みポート[槽入口] = 0;
            return 槽入口 + 32;
        }
        return -24;
    }
    public static int 実行束梱包(int 番号, int 通信網番地, int 通信端点ポート番号) {
        int 槽入口 = 検証(番号);
        if (槽入口 < 0) return -9;
        if (通信網番地 != 0 && 通信網番地 != 0x7f000001) return -99;
        if (ポート値[槽入口] != 0 || 通信端点ポート番号 < 0 || 通信端点ポート番号 > 65535) return -22;
        if (通信端点ポート番号 == 0) 通信端点ポート番号 = 一時ポート();
        if (通信端点ポート番号 < 0) return 通信端点ポート番号;
        if (重複範囲(通信端点ポート番号)) return -98;
        ポート値[槽入口] = 通信端点ポート番号; 番地[槽入口] = 通信網番地; return 0;
    }
    public static int データ格納(int 番号, int 値) {
        if (番号 < 0 || 番号 >= 512) return -22;
        前方値[番号] = 値 & 255; return 0;
    }
    public static int データ読取(int 番号) { return 番号 >= 0 && 番号 < 512 ? 前方値[番号] : -22; }
    public static int 送信(int 番号, int 通信網番地, int 通信端点ポート番号, int 容量) {
        int 槽入口 = 検証(番号);
        if (槽入口 < 0) return -9;
        if (通信網番地 != 0x7f000001) return -101;
        if (通信端点ポート番号 < 1 || 通信端点ポート番号 > 65535) return -22;
        if (容量 < 0 || 容量 > 512) return -90;
        if (ポート値[槽入口] == 0) {
            int 結果 = 実行束梱包(番号, 0x7f000001, 0);
            if (結果 < 0) return 結果;
        }
        int 宛先値 = -1;
        for (int 候補 = 0; 候補 < 8; 候補++) if (使用値[候補] != 0 && ポート値[候補] == 通信端点ポート番号) 宛先値 = 候補;
        if (宛先値 < 0) return -111;
        if (項目個数[宛先値] == 4) return -11;
        int 位置添字 = 宛先値 * 4 + (前面値[宛先値] + 項目個数[宛先値]) % 4;
        for (int バイト値 = 0; バイト値 < 容量; バイト値++) データ[位置添字 * 512 + バイト値] = 前方値[バイト値];
        長さ[位置添字] = 容量; 送信済みポート[位置添字] = ポート値[槽入口]; 項目個数[宛先値]++;
        return 容量;
    }
    public static int 受取(int 番号, int 容積値) {
        int 槽入口 = 検証(番号);
        if (槽入口 < 0) return -9;
        if (容積値 < 0 || 容積値 > 512) return -22;
        if (項目個数[槽入口] == 0) return -11;
        int 位置添字 = 槽入口 * 4 + 前面値[槽入口];
        int 容量 = 長さ[位置添字] < 容積値 ? 長さ[位置添字] : 容積値;
        for (int バイト値 = 0; バイト値 < 容量; バイト値++) 前方値[バイト値] = データ[位置添字 * 512 + バイト値];
        受信済みポート[槽入口] = 送信済みポート[位置添字]; 前面値[槽入口] = (前面値[槽入口] + 1) % 4; 項目個数[槽入口]--;
        return 容量;
    }
    public static int 通信端点ポート読取(int 番号) { int 槽入口 = 検証(番号); return 槽入口 < 0 ? -9 : ポート値[槽入口]; }
    public static int 番地読取(int 番号) { int 槽入口 = 検証(番号); return 槽入口 < 0 ? -9 : 番地[槽入口]; }
    public static int 送信者通信端点(int 番号) { int 槽入口 = 検証(番号); return 槽入口 < 0 ? -9 : 受信済みポート[槽入口]; }
    public static int 閉鎖(int 番号) {
        int 槽入口 = 検証(番号); if (槽入口 < 0) return -9;
        使用値[槽入口] = 0; 項目個数[槽入口] = 0; ポート値[槽入口] = 0; return 0;
    }
}
