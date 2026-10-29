// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** パイプは16 KiBずつ順に実行する。プロセスや並行パイプを模擬しない。 */
public final class シェル入出力 {
    static int[] 入力データ = new int[16384], 出力データ = new int[16384];
    static int 入力長さ, 入力位置, 出力長さ, 入力ファイル = -1, 出力ファイル = -1;
    static boolean パイプ入力, パイプ出力;
    static int 失敗値;
    static boolean 対話式許可処理 = true;
    public static int 判定対話式() { return 対話式許可処理 && 入力ファイル < 3 && 出力ファイル < 3 && !パイプ入力 && !パイプ出力 ? 1 : 0; }
    public static int 出力(int チャネル値, int 値) {
        if (チャネル値 != 1) return 0;
        if (出力ファイル >= 3) { int 処理済み値 = 記憶ファイル群.書込(出力ファイル, 値); if (処理済み値 < 0) 失敗値 = 処理済み値; return 1; }
        if (!パイプ出力) return 0;
        if (出力長さ == 出力データ.length) 失敗値 = -28;
        else 出力データ[出力長さ++] = 値;
        return 1;
    }
    public static int 入力値() {
        if (入力ファイル >= 3) { int 処理済み値 = 記憶ファイル群.読取(入力ファイル); return 処理済み値 == 256 ? -2 : 処理済み値; }
        if (パイプ入力) return 入力位置 < 入力長さ ? 入力データ[入力位置++] : -2;
        return -3; // UART へ転送する。
    }
    static void 起動処理(boolean 先行パイプ, boolean 末尾側パイプ) {
        パイプ入力 = 先行パイプ; パイプ出力 = 末尾側パイプ;
        入力位置 = 0; 出力長さ = 0; 入力ファイル = -1; 出力ファイル = -1; 失敗値 = 0;
    }
    static void 終端() {
        基板.切替入出力(0);
        if (入力ファイル >= 3) 記憶ファイル群.閉鎖(入力ファイル);
        if (出力ファイル >= 3) 記憶ファイル群.閉鎖(出力ファイル);
        if (パイプ出力) { 入力長さ = 出力長さ; for (int ループ添字 = 0; ループ添字 < 出力長さ; ループ添字++) 入力データ[ループ添字] = 出力データ[ループ添字]; }
        入力ファイル = -1; 出力ファイル = -1; パイプ入力 = false; パイプ出力 = false;
    }
}
