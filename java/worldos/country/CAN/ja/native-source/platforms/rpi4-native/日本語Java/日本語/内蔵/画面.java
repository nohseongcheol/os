// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 起動時に選んだ大きさの、独自カーネルの RGB32 フレームバッファー。 */
public final class 画面 {
    private 画面() {}
    public static int 幅値() { int 値 = 中核値.画面幅(); if (値 < 0) throw new 状況例外("フレームバッファがありません"); return 値; }
    public static int 高さ値() { int 値 = 中核値.画面高さ(); if (値 < 0) throw new 状況例外("フレームバッファがありません"); return 値; }
    public static void 矩形(int 水平位置, int 垂直位置, int 幅跨域, int 高さ値, int 色値) {
        if (水平位置 < 0 || 垂直位置 < 0 || 幅跨域 < 0 || 高さ値 < 0 || 水平位置 > 幅値() || 垂直位置 > 高さ値() || 幅跨域 > 幅値() - 水平位置 || 高さ値 > 高さ値() - 垂直位置) throw new 無効引数例外("画面の範囲");
        if (中核値.矩形(水平位置, 垂直位置, 幅跨域, 高さ値, 色値) < 0) throw new 状況例外("フレームバッファがありません");
    }
    public static void 入口消去処理(int 色値) { 矩形(0, 0, 幅値(), 高さ値(), 色値); }
    public static void 待機() { if (中核値.対象イメージ待合() < 0) throw new 状況例外("対話的な入力が必要です"); }
}
