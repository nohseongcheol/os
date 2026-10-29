// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 日本語 API の画面部品を作るための補助メソッド。 */
public final class 操作部品 {
    private 操作部品() {}
    public static void 後続呼出(実行可能処理作業 作業動作) { イベント待ち行列.後続呼出(作業動作); }
    public static ラベル 印札値(String 文, int 水平位置, int 垂直位置, int 幅跨域, int 高さ値) {
        return new ラベル(文, 水平位置, 垂直位置, 幅跨域, 高さ値);
    }
    public static ボタン ボタン(String 文, int 水平位置, int 垂直位置, int 幅跨域, int 高さ値, 動作受信先 受信先値) {
        return new ボタン(文, 水平位置, 垂直位置, 幅跨域, 高さ値, 受信先値);
    }
    public static 本文フィールド 本文フィールド(String 文, int 水平位置, int 垂直位置, int 幅跨域, int 高さ値) {
        return new 本文フィールド(文, 水平位置, 垂直位置, 幅跨域, 高さ値);
    }
}
