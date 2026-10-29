// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 の機械境界。ポインターを Java の int に切り詰めて渡さない。 */
public final class 基板 {
    public static native int 表示処理画素読取(int 水平位置, int 垂直位置);
    public static native void 表示処理画素書込(int 水平位置, int 垂直位置, int 色値);
    public static native int 遠隔制御(int 種別値, int 動作);
    public static native void 終端位置遠隔命令(int 状況値);
    public static native void 遠隔待合(int 状況値);
    public static native void 直列書込(int 値);
    public static native int 直列読取();
    public static native int ミリ秒();
    public static native int CPU特権水準();
    public static native int 画面用意();
    public static native int 画面幅();
    public static native int 画面高さ();
    public static native void 画面画素格納(int 水平位置, int 垂直位置, int 色値);
    public static native void 処理機実行権譲渡();
    public static native int 作業作成(int 番号);
    public static native int 作業状況(int 番号);
    public static native void 停止(int 状況値);
    public static native int Cpp試験();
    public static native int 利用者プログラム起動処理(int 番号);
    public static native int 利用者プログラム検査();
    public static native int 引数列用意(int 項目個数);
    public static native int 利用者ファイル実行();
    public static native int Linuxファイル実行();
    public static native int 引数バイト(int 番号, int 位置, int 値);
    public static native int 端末(int 動作);
    public static native int 制御利用者プログラム(int 動作);
    public static native void 切替入出力(int 動作);
    public static native int ファイル転送サービス(int 動作);
    public static native int 通信網状態(int 入口値, int 番号);
    public static native int 通信網設定値(int 動作, int 番地, int マスク値, int 中継門値);
    public static native int 応答送信(int 番地, int 順序値);
    public static native int 応答読取(int 入口値);
    public static native int 照会システム(int 入口値, int 番号);
    public static native void 電源停止側();
}
