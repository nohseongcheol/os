// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package カナダ.JCanOS.記述子入口;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 全域記述子表とタスク状態区画の設定を保持する。 */
public final class 大域記述子表 {
    public static final class 断片値 {
        private final int 背景値;
        private final int 境界位置上限;
        private final int アクセス値;

        断片値(int 背景値, int 境界位置上限, int アクセス値) {
            this.背景値 = 背景値;
            this.境界位置上限 = 境界位置上限;
            this.アクセス値 = アクセス値;
        }

        public int 背景値() { return 背景値; }
        public int 境界位置上限() { return 境界位置上限; }
        public int アクセス値() { return アクセス値; }
    }

    private final List<断片値> 断片群一覧 = new ArrayList<断片値>();

    public int 入口追記(int 背景値, int 境界位置上限, int アクセス値) {
        断片群一覧.add(new 断片値(背景値, 境界位置上限, アクセス値));
        return (断片群一覧.size() - 1) * 8;
    }

    public List<断片値> 断片群一覧() {
        return Collections.unmodifiableList(断片群一覧);
    }

    public void 既定値設定() {
        断片群一覧.clear();
        入口追記(0, 0, 0);
        入口追記(0, 0xfffff, 0x9a);
        入口追記(0, 0xfffff, 0x92);
        入口追記(0, 0xfffff, 0xfa);
        入口追記(0, 0xfffff, 0xf2);
    }
}

