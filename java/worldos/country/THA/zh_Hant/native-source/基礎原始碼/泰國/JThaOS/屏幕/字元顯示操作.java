// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 泰國.JThaOS.屏幕;

import java.util.Arrays;

/** 類似 VGA 文字模式的 80×25 字元畫面模型。 */
public final class 字元顯示操作 {
    public static final int 寬度值 = 80;
    public static final int 高度值 = 25;
    private final char[] 字元值列 = new char[寬度值 * 高度值];
    private int 水平位置;
    private int 垂直位置;

    public 字元顯示操作() {
        擦除條目();
    }

    public void 輸出(String 內容值) {
        for (int 編號 = 0; 編號 < 內容值.length(); 編號++) {
            char 字元 = 內容值.charAt(編號);
            if (字元 == '\n') {
                水平位置 = 0;
                垂直位置++;
            } else {
                打印字元(水平位置++, 垂直位置, 字元);
            }
            if (水平位置 >= 寬度值) {
                水平位置 = 0;
                垂直位置++;
            }
            if (垂直位置 >= 高度值) {
                滾動向上();
            }
        }
    }

    public char 字元(int 水平位置, int 垂直位置) {
        驗證位置(水平位置, 垂直位置);
        return 字元值列[垂直位置 * 寬度值 + 水平位置];
    }

    public void 擦除條目() {
        Arrays.fill(字元值列, ' ');
        水平位置 = 0;
        垂直位置 = 0;
    }

    private void 打印字元(int 水平位置, int 垂直位置, char 字元) {
        驗證位置(水平位置, 垂直位置);
        字元值列[垂直位置 * 寬度值 + 水平位置] = 字元;
    }

    private void 滾動向上() {
        System.arraycopy(字元值列, 寬度值, 字元值列, 0, 寬度值 * (高度值 - 1));
        Arrays.fill(字元值列, 寬度值 * (高度值 - 1), 字元值列.length, ' ');
        垂直位置 = 高度值 - 1;
    }

    private void 驗證位置(int 水平位置, int 垂直位置) {
        if (水平位置 < 0 || 水平位置 >= 寬度值 || 垂直位置 < 0 || 垂直位置 >= 高度值) {
            throw new IllegalArgumentException("屏幕 위치가 올바르지 않습니다.");
        }
    }
}

