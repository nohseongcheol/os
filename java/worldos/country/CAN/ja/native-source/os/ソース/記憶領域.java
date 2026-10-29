// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 起動情報の参照と4 KiB固定長タスク領域の確保・返却。一般的な物理ページ管理器ではない。 */
public final class 記憶領域 {
    static int[] 区画値 = new int[8192];
    static int[] 使用値 = new int[8];

    static int 整数値解析(int 番地) {
        return 装置.記憶読取(番地) | (装置.記憶読取(番地 + 1) << 8)
            | (装置.記憶読取(番地 + 2) << 16) | (装置.記憶読取(番地 + 3) << 24);
    }

    static int 上限側記憶容量() {
        int システム情報 = 装置.起動情報();
        if (装置.起動標識() != 0x2badb002 || システム情報 == 0 || (整数値解析(システム情報) & 1) == 0) return -1;
        return 整数値解析(システム情報 + 8);
    }

    static int 記憶装置確保() {
        for (int 番号 = 0; 番号 < 使用値.length; 番号++) {
            if (使用値[番号] == 0) {
                使用値[番号] = 1;
                for (int 槽入口 = 0; 槽入口 < 1024; 槽入口++) 区画値[番号 * 1024 + 槽入口] = 0;
                return 番号;
            }
        }
        return -1;
    }

    static boolean 復帰結果(int 番号) {
        if (番号 < 0 || 番号 >= 使用値.length || 使用値[番号] == 0) return false;
        使用値[番号] = 0;
        return true;
    }

    static int 使用済み入口個数() {
        int 項目個数 = 0;
        for (int 番号 = 0; 番号 < 使用値.length; 番号++) 項目個数 += 使用値[番号];
        return 項目個数;
    }
}
