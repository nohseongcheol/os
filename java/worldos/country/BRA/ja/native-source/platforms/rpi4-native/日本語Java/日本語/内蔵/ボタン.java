// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本語.内蔵;
/** 独自画面で動作通知を送るボタン。 */
public final class ボタン extends 画面要素 {
    public ボタン(String 文, int 水平位置, int 垂直位置, int 幅跨域, int 高さ値, 動作受信先 受信先値) {
        throw new 状況例外("自前の JVM に日本語 API のボタンを作成する機能が必要です。");
    }
    public native void 動作受信先設定(動作受信先 受信先値);
}
