// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros の利用者 ELF 専用 API。Linux/JVM 向けの JNI や java.net API ではない。 */
public final class 利用者 {
    public static native int ファイル記述子開放(int[] ファイル入口名前, int 設定値開放);
    public static native int 一ファイルバイト読取(int ファイル記述子);
    public static native int 一ファイルバイト書込(int ファイル記述子, int バイト値);
    public static native int ファイル記述子閉鎖(int ファイル記述子);
    public static native int 確定ファイル記憶装置(int ファイル記述子);
    public static native int ファイル読取(int[] 名前, int[] データ);
    public static native int 文字値書込(int 文字);
    public static native int ファイル書込(int[] 名前, int[] データ, int 長さ);
    public static native int 書込(String 内容物値);
    public static native int 引数列個数();
    public static native String 引数(int 番号);
    public static native int 実行状態許可();
    public static native int 通信網開放(int 局所ポート);
    public static native int データ送信(int 取扱い値, int 番地, int 宛先ポート, int[] データ, int 長さ);
    public static native int データ受取(int 取扱い値, int[] データ, int 上限ミリ秒);
    public static native int 通信網閉鎖(int 取扱い値);
    public static native int 自前番地();
    public static native int 送信済み番地(int 取扱い値);
    public static native int 送信済みポート(int 取扱い値);
}
