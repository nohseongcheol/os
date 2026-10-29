// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自画面の事象待ち行列へ仕事を渡す。 */
public final class イベント待ち行列 {
    private イベント待ち行列() {}
    public static native void 後続呼出(実行可能処理作業 作業動作);
    public static native boolean 判定イベント配送中();
}
