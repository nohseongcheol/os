// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 新加坡.JSgpOS.描述符条目;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 保存 x86 全局描述符表和任务状态段的设置。 */
public final class 全局描述符表 {
    public static final class 片段值 {
        private final int 背景值;
        private final int 边界位置限制;
        private final int 存取值;

        片段值(int 背景值, int 边界位置限制, int 存取值) {
            this.背景值 = 背景值;
            this.边界位置限制 = 边界位置限制;
            this.存取值 = 存取值;
        }

        public int 背景值() { return 背景值; }
        public int 边界位置限制() { return 边界位置限制; }
        public int 存取值() { return 存取值; }
    }

    private final List<片段值> 片段列列表 = new ArrayList<片段值>();

    public int 追加条目(int 背景值, int 边界位置限制, int 存取值) {
        片段列列表.add(new 片段值(背景值, 边界位置限制, 存取值));
        return (片段列列表.size() - 1) * 8;
    }

    public List<片段值> 片段列列表() {
        return Collections.unmodifiableList(片段列列表);
    }

    public void 设定默认值() {
        片段列列表.clear();
        追加条目(0, 0, 0);
        追加条目(0, 0xfffff, 0x9a);
        追加条目(0, 0xfffff, 0x92);
        追加条目(0, 0xfffff, 0xfa);
        追加条目(0, 0xfffff, 0xf2);
    }
}

