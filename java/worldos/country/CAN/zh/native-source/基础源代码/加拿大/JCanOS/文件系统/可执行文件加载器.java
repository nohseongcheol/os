// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 加拿大.JCanOS.文件系统;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 验证小端 ELF32 可执行文件的头部和加载段。 */
public final class 可执行文件加载器 {
    public static final class 区段值 {
        private final int 种类值;
        private final int 标志值;
        private final int 地址;
        private final int 文件位置;
        private final int 大小;

        区段值(int 种类值, int 标志值, int 地址, int 文件位置, int 大小) {
            this.种类值 = 种类值;
            this.标志值 = 标志值;
            this.地址 = 地址;
            this.文件位置 = 文件位置;
            this.大小 = 大小;
        }

        public int 种类值() {
            return 种类值;
        }

        public int 标志值() {
            return 标志值;
        }

        public int 地址() {
            return 地址;
        }

        public int 文件位置() {
            return 文件位置;
        }

        public int 大小() {
            return 大小;
        }
    }

    public static final class 映像 {
        private final int 开始地址;
        private final List<区段值> 区段列列表;

        映像(int 开始地址, List<区段值> 区段列列表) {
            this.开始地址 = 开始地址;
            this.区段列列表 = Collections.unmodifiableList(区段列列表);
        }

        public int 开始地址() {
            return 开始地址;
        }

        public List<区段值> 区段列列表() {
            return 区段列列表;
        }
    }

    public 映像 检查项(byte[] 数据) {
        if (数据 == null || 数据.length < 52
                || 数据[0] != 0x7f || 数据[1] != 'E' || 数据[2] != 'L' || 数据[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (数据[4] != 1 || 数据[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int 开始地址 = 解析整数(数据, 24);
        int 区段表位置 = 解析整数(数据, 32);
        int 区段条目大小 = 读取短整数整数(数据, 46);
        int 区段个数 = 读取短整数整数(数据, 48);
        if (区段条目大小 < 40 || 区段表位置 < 0
                || (long) 区段表位置 + (long) 区段条目大小 * 区段个数 > 数据.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<区段值> 区段列列表 = new ArrayList<区段值>();
        for (int 编号 = 0; 编号 < 区段个数; 编号++) {
            int 位置 = 区段表位置 + 编号 * 区段条目大小;
            int 种类值 = 解析整数(数据, 位置 + 4);
            int 标志值 = 解析整数(数据, 位置 + 8);
            int 地址 = 解析整数(数据, 位置 + 12);
            int 文件位置 = 解析整数(数据, 位置 + 16);
            int 大小 = 解析整数(数据, 位置 + 20);
            if (大小 < 0 || (种类值 != 8 && ((long) 文件位置 + 大小 > 数据.length || 文件位置 < 0))) {
                throw new IllegalArgumentException("ELF 区段值 数据 범위가 올바르지 않습니다.");
            }
            区段列列表.add(new 区段值(种类值, 标志值, 地址, 文件位置, 大小));
        }
        return new 映像(开始地址, 区段列列表);
    }

    private int 解析整数(byte[] 数据, int 位置) {
        if (位置 < 0 || 位置 > 数据.length - 4) {
            throw new IllegalArgumentException("ELF 整数 범위를 벗어났습니다.");
        }
        return (数据[位置] & 0xff)
                | ((数据[位置 + 1] & 0xff) << 8)
                | ((数据[位置 + 2] & 0xff) << 16)
                | ((数据[位置 + 3] & 0xff) << 24);
    }

    private int 读取短整数整数(byte[] 数据, int 位置) {
        if (位置 < 0 || 位置 > 数据.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 整数 범위를 벗어났습니다.");
        }
        return (数据[位置] & 0xff) | ((数据[位置 + 1] & 0xff) << 8);
    }
}
