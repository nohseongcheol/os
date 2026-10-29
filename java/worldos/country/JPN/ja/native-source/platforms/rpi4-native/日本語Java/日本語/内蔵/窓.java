// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自 JVM とカーネルの窓管理機能へ直接接続する窓。 */
public final class 窓 extends 画面要素 {
    public 窓(String 窓表題, int 幅跨域, int 高さ値) {
        throw new 状況例外("自前の JVM に日本語 API の窓を作成する機能が必要です。");
    }
    public native void 要素追加(画面要素 要素値);
    public native void 窓表示();
    public native void 閉鎖();
    public native boolean 判定可視();
}
