// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国.JChnOS.设备;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 管理 PCI 设备发现结果及 BAR/IRQ 值。 */
public final class 外设总线管理器 {
    public static final class 设备 {
        private final int 供应商标识符;
        private final int 设备标识符;
        private final int 输入输出基底;
        private final int 中断编号;

        public 设备(int 供应商标识符, int 设备标识符, int 输入输出基底, int 中断编号) {
            this.供应商标识符 = 供应商标识符;
            this.设备标识符 = 设备标识符;
            this.输入输出基底 = 输入输出基底;
            this.中断编号 = 中断编号;
        }

        public int 供应商标识符() { return 供应商标识符; }
        public int 设备标识符() { return 设备标识符; }
        public int 输入输出基底() { return 输入输出基底; }
        public int 中断编号() { return 中断编号; }
    }

    private final List<设备> 设备列列表 = new ArrayList<设备>();

    public void 已发现值(设备 设备) {
        设备列列表.add(设备);
    }

    public List<设备> 设备列列表() {
        return Collections.unmodifiableList(设备列列表);
    }

    public 设备 查找条目(int 供应商标识符, int 设备标识符) {
        for (设备 候选 : 设备列列表) {
            if (候选.供应商标识符 == 供应商标识符 && 候选.设备标识符 == 设备标识符) {
                return 候选;
            }
        }
        return null;
    }
}

