// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 の Java 道具専用の SVC 接続。既存の x86 道具のソースと一緒にビルドする。 */
public final class 利用者 {
    public static native int ファイル記述子開放(int[] 名前, int 設定値);
    public static native int 一ファイルバイト読取(int 記述子入口);
    public static native int 一ファイルバイト書込(int 記述子入口, int 値);
    public static native int ファイル記述子閉鎖(int 記述子入口);
    public static native int ファイル読取(int[] 名前, int[] データ);
    public static native int ファイル書込(int[] 名前, int[] データ, int 長さ);
    public static native int 書込(String 文);
    public static native int 文字値書込(int 値);
    public static native int 引数列個数();
    public static native String 引数(int 番号);
    public static native int 道具要素番号();
    public static native int 画面接続状態(int 動作, int 番号, int 先頭位置被演算子, int 第二被演算子, int 第三被演算子, int 第四被演算子);
    public static native int 画面本文(int 番号, int[] 文, int 長さ);
    public static native int 画面幅();
    public static native int 画面高さ();
    public static native int ストリーム制御(int 動作, int 記述子入口, int 値);
    public static native int ストリーム接続(int 記述子入口, int 番地, int ポート値);
    public static native int 通信網開放(int ポート値);
    public static native int 通信網送信(int 記述子入口, int 番地, int ポート値, int[] データ, int 長さ);
    public static native int 通信網受取(int 記述子入口, int[] データ, int 長さ);
    public static native int 通信網ポート(int 記述子入口);
    public static native int ミリ秒();
    public static native int 対象イメージ待合();
    public static native int 矩形(int 水平位置, int 垂直位置, int 幅跨域, int 高さ値, int 色値);
}
