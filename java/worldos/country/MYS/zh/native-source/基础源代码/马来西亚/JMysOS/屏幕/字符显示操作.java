// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 马来西亚.JMysOS.屏幕;

import java.util.Arrays;

/** 类似 VGA 文本模式的 80×25 字符屏幕模型。 */
public final class 字符显示操作 {
    public static final int 宽度值 = 80;
    public static final int 高度值 = 25;
    private final char[] 字符值列 = new char[宽度值 * 高度值];
    private int 水平位置;
    private int 垂直位置;

    public 字符显示操作() {
        擦除条目();
    }

    public void 输出(String 内容值) {
        for (int 编号 = 0; 编号 < 内容值.length(); 编号++) {
            char 字符 = 内容值.charAt(编号);
            if (字符 == '\n') {
                水平位置 = 0;
                垂直位置++;
            } else {
                打印字符(水平位置++, 垂直位置, 字符);
            }
            if (水平位置 >= 宽度值) {
                水平位置 = 0;
                垂直位置++;
            }
            if (垂直位置 >= 高度值) {
                滚动向上();
            }
        }
    }

    public char 字符(int 水平位置, int 垂直位置) {
        验证位置(水平位置, 垂直位置);
        return 字符值列[垂直位置 * 宽度值 + 水平位置];
    }

    public void 擦除条目() {
        Arrays.fill(字符值列, ' ');
        水平位置 = 0;
        垂直位置 = 0;
    }

    private void 打印字符(int 水平位置, int 垂直位置, char 字符) {
        验证位置(水平位置, 垂直位置);
        字符值列[垂直位置 * 宽度值 + 水平位置] = 字符;
    }

    private void 滚动向上() {
        System.arraycopy(字符值列, 宽度值, 字符值列, 0, 宽度值 * (高度值 - 1));
        Arrays.fill(字符值列, 宽度值 * (高度值 - 1), 字符值列.length, ' ');
        垂直位置 = 高度值 - 1;
    }

    private void 验证位置(int 水平位置, int 垂直位置) {
        if (水平位置 < 0 || 水平位置 >= 宽度值 || 垂直位置 < 0 || 垂直位置 >= 高度值) {
            throw new IllegalArgumentException("屏幕 위치가 올바르지 않습니다.");
        }
    }
}

