// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 英國.JGbrOS.設備;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 管理 PCI 裝置探索結果及 BAR/IRQ 值。 */
public final class 外設總線管理器 {
    public static final class 設備 {
        private final int 供應商標識符;
        private final int 設備標識符;
        private final int 輸入輸出基底;
        private final int 中斷編號;

        public 設備(int 供應商標識符, int 設備標識符, int 輸入輸出基底, int 中斷編號) {
            this.供應商標識符 = 供應商標識符;
            this.設備標識符 = 設備標識符;
            this.輸入輸出基底 = 輸入輸出基底;
            this.中斷編號 = 中斷編號;
        }

        public int 供應商標識符() { return 供應商標識符; }
        public int 設備標識符() { return 設備標識符; }
        public int 輸入輸出基底() { return 輸入輸出基底; }
        public int 中斷編號() { return 中斷編號; }
    }

    private final List<設備> 設備列列表 = new ArrayList<設備>();

    public void 已發現值(設備 設備) {
        設備列列表.add(設備);
    }

    public List<設備> 設備列列表() {
        return Collections.unmodifiableList(設備列列表);
    }

    public 設備 查找條目(int 供應商標識符, int 設備標識符) {
        for (設備 候選 : 設備列列表) {
            if (候選.供應商標識符 == 供應商標識符 && 候選.設備標識符 == 設備標識符) {
                return 候選;
            }
        }
        return null;
    }
}

