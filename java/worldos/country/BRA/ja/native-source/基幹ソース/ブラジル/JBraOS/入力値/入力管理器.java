// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ブラジル.JBraOS.入力値;

import java.util.ArrayDeque;
import java.util.Queue;

/** 割込みと管理コードの間で入力事象を安全に渡す。 */
public final class 入力管理器 {
    private final Queue<入力イベント> イベント一覧一覧 = new ArrayDeque<入力イベント>();
    private final int 最大イベント個数;
    private int 破棄件数イベント個数;

    public 入力管理器(int 最大イベント個数) {
        if (最大イベント個数 <= 0) {
            throw new IllegalArgumentException("イベント 수가 올바르지 않습니다.");
        }
        this.最大イベント個数 = 最大イベント個数;
    }

    public synchronized void キー下方(int キーデータ) {
        値格納(new 入力イベント(入力イベント.種別値.キー下方, キーデータ & 0xff, 0));
    }

    public synchronized void キー上方(int キーデータ) {
        値格納(new 入力イベント(入力イベント.種別値.キー上方, キーデータ & 0xff, 0));
    }

    public synchronized void マウス移動量(int 水平位置, int 垂直位置) {
        値格納(new 入力イベント(入力イベント.種別値.マウス移動量, 水平位置, 垂直位置));
    }

    public synchronized 入力イベント 次回イベント() {
        return イベント一覧一覧.poll();
    }

    public synchronized int 破棄件数イベント個数() {
        return 破棄件数イベント個数;
    }

    private void 値格納(入力イベント イベント) {
        if (イベント一覧一覧.size() == 最大イベント個数) {
            イベント一覧一覧.poll();
            破棄件数イベント個数++;
        }
        イベント一覧一覧.offer(イベント);
    }
}

