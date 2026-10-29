// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国香港特别行政区.JHkgOS.文件系统;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** 读取 DOS MBR 的四个主分区。 */
public final class 主要分区表 {
    public static final class 分区值 {
        private final int 种类值;
        private final long 开始区段;
        private final long 区段个数;

        分区值(int 种类值, long 开始区段, long 区段个数) {
            this.种类值 = 种类值;
            this.开始区段 = 开始区段;
            this.区段个数 = 区段个数;
        }

        public int 种类值() { return 种类值; }
        public long 开始区段() { return 开始区段; }
        public long 区段个数() { return 区段个数; }
    }

    public List<分区值> 读取(byte[] 首位区段) {
        if (首位区段 == null || 首位区段.length < 512
                || (首位区段[510] & 0xff) != 0x55 || (首位区段[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<分区值> 结果 = new ArrayList<分区值>();
        for (int 编号 = 0; 编号 < 4; 编号++) {
            int 位置 = 446 + 编号 * 16;
            int 种类值 = 首位区段[位置 + 4] & 0xff;
            long 运行 = 小字节序整数(首位区段, 位置 + 8);
            long 大小 = 小字节序整数(首位区段, 位置 + 12);
            if (种类值 != 0 && 大小 != 0) {
                结果.add(new 分区值(种类值, 运行, 大小));
            }
        }
        return Collections.unmodifiableList(结果);
    }

    private long 小字节序整数(byte[] 数据, int 位置) {
        return (数据[位置] & 0xffL)
                | ((数据[位置 + 1] & 0xffL) << 8)
                | ((数据[位置 + 2] & 0xffL) << 16)
                | ((数据[位置 + 3] & 0xffL) << 24);
    }
}

