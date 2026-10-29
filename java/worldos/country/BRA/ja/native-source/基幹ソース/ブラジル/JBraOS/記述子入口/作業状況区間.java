// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.記述子入口;

/** x86 タスク切替え時の特権スタックを用意する TSS の管理表現。 */
public final class 作業状況区間 {
    private int スタック零ブロック;
    private int スタック零番地;
    private int 入出力許可表位置 = 104;

    public void 特権用スタック設定(int 断片値, int 番地) {
        スタック零ブロック = 断片値;
        スタック零番地 = 番地;
    }

    public int スタック零ブロック() { return スタック零ブロック; }
    public int スタック零番地() { return スタック零番地; }
    public int 入出力許可表位置() { return 入出力許可表位置; }
}

