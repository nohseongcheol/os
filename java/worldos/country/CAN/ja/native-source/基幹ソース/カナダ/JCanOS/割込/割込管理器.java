// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.割込;

import java.util.Arrays;

/** IDT の Java 管理側の処理器登録と振分けを担う。 */
public final class 割込管理器 {
    private final 割込処理器[] 処理器一覧 = new 割込処理器[256];
    private boolean 活動中;

    public void 入口レジスタ(int 番号, 割込処理器 処理器) {
        番号検証(番号);
        処理器一覧[番号] = 処理器;
    }

    public void 記憶装置解放(int 番号) {
        番号検証(番号);
        処理器一覧[番号] = null;
    }

    public int 値配分(int 番号, int 保存済みスタック番地) {
        番号検証(番号);
        if (!活動中) {
            return 保存済みスタック番地;
        }
        割込処理器 処理器 = 処理器一覧[番号];
        return 処理器 == null ? 保存済みスタック番地 : 処理器.プロセス値入口(保存済みスタック番地);
    }

    public void 有効化() {
        活動中 = true;
    }

    public void 無効化() {
        活動中 = false;
    }

    public boolean 判定活動中() {
        return 活動中;
    }

    public void 全体解放() {
        Arrays.fill(処理器一覧, null);
    }

    private void 番号検証(int 番号) {
        if (番号 < 0 || 番号 >= 処理器一覧.length) {
            throw new IllegalArgumentException("割込 번호가 올바르지 않습니다.");
        }
    }
}

