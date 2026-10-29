// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 独自 Java カーネルの Pi4 初期移植版。Linux やホスト JVM の上では動かさない。 */
public final class 中核 {
    static int[] 作業反復回数 = new int[3];
    static int[] 作業総和 = new int[3];
    static int 作業順序;
    static int 作業エラー;
    static int 乱数種 = 17;

    static void 検証(boolean 条件, int 番号) {
        if (!条件) { 端末入出力.書込("FAIL "); 端末入出力.数(番号); 基板.停止(番号); }
    }
    static int 分岐(int 値) {
        switch (値) { case -100: return 7; case 2: return 9; case 1000: return 11; default: return 3; }
    }
    static int 密切替(int 値) {
        switch (値) { case 0: return 9; case 1: return 12; case 2: return 17; case 3: return 20; default: return -1; }
    }
    static int[] 復帰配列(int[] 配列値) { return 配列値; }
    static void 算術試験() {
        int 値 = 乱数種;
        検証(値 * 7 - 値 == 102 && 値 / 3 == 5 && 値 % 3 == 2, 1);
        int 最小整数値 = 0x80000000, 負数一 = -1;
        検証(最小整数値 / 負数一 == 最小整数値 && 最小整数値 % 負数一 == 0, 2);
        検証(最小整数値 + 最小整数値 == 0 && -最小整数値 == 最小整数値, 3);
        検証((-値 >> 2) == -5 && (-値 >>> 2) == 1073741819 && (値 << 33) == 34, 4);
        検証((byte)(値 * 16) == 16 && (short)65535 == -1 && (char)負数一 == 65535, 5);
        int[] 配列値 = new int[5];
        for (int ループ添字 = 0; ループ添字 < 配列値.length; ループ添字++) 配列値[ループ添字] = ループ添字 * 値;
        配列値[2]++;
        検証(復帰配列(配列値) == 配列値 && 配列値[2] == 35 && 配列値[4] == 68, 6);
        検証(分岐(値 - 117) == 7 && 分岐(値 - 15) == 9 && 分岐(値) == 3 && 密切替(値 - 15) == 17, 7);
        String 文 = "한글 😀";
        検証(文.length() == 5 && 文.charAt(0) == '한' && 文.charAt(3) == 0xd83d, 8);
        検証(基板.CPU特権水準() == 1, 9);
        端末入出力.書込("JAVA AOT PASS int32/ref64/array/string/switch EL1\n");
    }
    public static void 作業(int 番号) {
        // 実行権を譲る前後で局所変数が保たれるか確認する。各タスクは独立した機械スタックを使う。
        int 局所値 = 番号 * 100;
        for (int ループ添字 = 0; ループ添字 < 10; ループ添字++) {
            if (作業順序 % 2 + 1 != 番号) 作業エラー++;
            作業順序++;
            局所値 += ループ添字 + 番号;
            作業総和[番号] = 局所値;
            作業反復回数[番号]++;
            基板.処理機実行権譲渡();
            if (局所値 != 作業総和[番号]) 作業エラー++;
        }
    }
    static void 作業一覧試験() {
        作業順序 = 0; 作業エラー = 0;
        作業反復回数[1] = 0; 作業反復回数[2] = 0;
        検証(基板.作業作成(1) == 0 && 基板.作業作成(2) == 0, 20);
        int 回転個数 = 0;
        while (基板.作業状況(1) != 0 || 基板.作業状況(2) != 0) {
            基板.処理機実行権譲渡();
            検証(++回転個数 < 100, 21);
        }
        検証(作業反復回数[1] == 10 && 作業反復回数[2] == 10 && 作業順序 == 20 && 作業エラー == 0, 22);
        検証(作業総和[1] == 155 && 作業総和[2] == 265, 23);
        端末入出力.書込("TASK PASS two stacks / 20 alternating steps (cooperative)\n");
    }
    static void 矩形(int 水平位置, int 垂直位置, int 幅値, int 高さ値, int 色値) {
        for (int 縦座標 = 垂直位置; 縦座標 < 垂直位置 + 高さ値; 縦座標++)
            for (int 横座標 = 水平位置; 横座標 < 水平位置 + 幅値; 横座標++) 基板.画面画素格納(横座標, 縦座標, 色値);
    }
    static void 画面() {
        if (基板.画面用意() == 0) { 端末入出力.書込("FRAMEBUFFER unavailable\n"); return; }
        矩形(0, 0, 基板.画面幅(), 基板.画面高さ(), 0x302018);
        矩形(40, 40, 560, 400, 0xefe8e2);
        矩形(40, 40, 560, 40, 0x905020);
        矩形(60, 110, 240, 140, 0x90b050);
        矩形(320, 110, 260, 140, 0xd0a040);
        矩形(60, 290, 520, 120, 0xd8d0c8);
        端末入出力.書込("FRAMEBUFFER PASS "); 端末入出力.数(基板.画面幅()); 端末入出力.文字('x');
        端末入出力.数(基板.画面高さ()); 端末入出力.書込(" RGB32 (drawing only)\n");
    }
    static void C試験() {
        int 結果 = 基板.Cpp試験();
        検証(結果 == 0, 100 + 結果);
        端末入出力.書込("C++ POSIX-KOR PASS direct Java RAM file API\n");
    }
    static void 利用者プログラム一覧試験() {
        検証(基板.利用者プログラム検査() == 0, 200);
        端末入出力.書込("ELF64 REJECT PASS malformed / ABI / bounds / W^X\n");
        int 初期結果 = 基板.利用者プログラム起動処理(0);
        if (初期結果 != 0) { 端末入出力.書込("USER DEMO RESULT "); 端末入出力.数(初期結果); 端末入出力.文字(10); }
        検証(初期結果 == 0, 201);
        端末入出力.書込("EL0 C++ PASS constructors / RAII / file / heap / syscall pointers\n");
        int[] 期待値一覧 = new int[]{-1001, -1001, -1002, -1001, -1003, -1004, -1001, -1002};
        for (int 番号 = 0; 番号 < 期待値一覧.length; 番号++) {
            端末入出力.書込("USER CHECK "); 端末入出力.数(番号); 端末入出力.文字(10);
            int 結果 = 基板.利用者プログラム起動処理(番号 + 1);
            if (結果 != 期待値一覧[番号]) { 端末入出力.書込("USER RESULT "); 端末入出力.数(結果); 端末入出力.文字(10); }
            検証(結果 == 期待値一覧[番号], 210 + 番号);
        }
        検証(基板.利用者プログラム起動処理(0) == 0, 220);
        端末入出力.書込("USER PROTECTION PASS kernel/text/MMIO/stack/NX/privilege/timer; kernel recovered\n");
    }
    static void 通信機構試験() {
        int 結果 = 基板.利用者プログラム起動処理(9);
        if (結果 != 0) { 端末入出力.書込("UDP RESULT "); 端末入出力.数(結果); 端末入出力.文字(10); }
        検証(結果 == 0, 230);
    }
    static void システム情報() {
        端末入出力.書込("Own Java AOT kernel / AArch64 EL1 / Raspberry Pi 4\n");
        端末入出力.書込("No Linux kernel. Java subset + MicroPython; no full OpenJDK/CPython/Swing.\n");
        端末入出力.書込("EL0 ELF64 / MMU / W^X / SVC ABI v1 / 2-second user deadline\n");
        端末入出力.書込("IPv4 TCP/UDP: lwIP over auxiliary UART SLIP; guest FTP. No GENET/Wi-Fi/DNS/TLS yet.\n");
        端末入出力.書込("Guest TinyCC and static-subset jaot. No SD filesystem or full OpenJDK/pthread.\n");
    }
    public static void 起動処理() {
        端末入出力.書込("WorldOS ja · こんにちは · 😀\n");
        算術試験();
        C試験();
        作業一覧試験();
        画面();
        利用者プログラム一覧試験();
        通信機構試験();
        端末入出力.書込("NATIVE READY\n");
        命令解釈器.命令実行();
    }
}
