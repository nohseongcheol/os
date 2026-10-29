// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本.JJpnOS.装置;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI 装置の探索結果と BAR/IRQ 値を管理する。 */
public final class 周辺バス管理器 {
    public static final class 装置 {
        private final int 供給元識別子;
        private final int 装置識別子;
        private final int 入出力基底;
        private final int 割込番号;

        public 装置(int 供給元識別子, int 装置識別子, int 入出力基底, int 割込番号) {
            this.供給元識別子 = 供給元識別子;
            this.装置識別子 = 装置識別子;
            this.入出力基底 = 入出力基底;
            this.割込番号 = 割込番号;
        }

        public int 供給元識別子() { return 供給元識別子; }
        public int 装置識別子() { return 装置識別子; }
        public int 入出力基底() { return 入出力基底; }
        public int 割込番号() { return 割込番号; }
    }

    private final List<装置> 装置一覧一覧 = new ArrayList<装置>();

    public void 発見済み値(装置 装置) {
        装置一覧一覧.add(装置);
    }

    public List<装置> 装置一覧一覧() {
        return Collections.unmodifiableList(装置一覧一覧);
    }

    public 装置 入口探索(int 供給元識別子, int 装置識別子) {
        for (装置 候補 : 装置一覧一覧) {
            if (候補.供給元識別子 == 供給元識別子 && 候補.装置識別子 == 装置識別子) {
                return 候補;
            }
        }
        return null;
    }
}

