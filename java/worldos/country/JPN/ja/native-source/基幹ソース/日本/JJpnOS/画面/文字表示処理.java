// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 日本.JJpnOS.画面;

import java.util.Arrays;

/** VGA 文字モードに相当する80×25文字画面のモデル。 */
public final class 文字表示処理 {
    public static final int 幅値 = 80;
    public static final int 高さ値 = 25;
    private final char[] 文字値一覧 = new char[幅値 * 高さ値];
    private int 水平位置;
    private int 垂直位置;

    public 文字表示処理() {
        入口消去処理();
    }

    public void 出力(String 内容物値) {
        for (int 番号 = 0; 番号 < 内容物値.length(); 番号++) {
            char 文字 = 内容物値.charAt(番号);
            if (文字 == '\n') {
                水平位置 = 0;
                垂直位置++;
            } else {
                文字印刷(水平位置++, 垂直位置, 文字);
            }
            if (水平位置 >= 幅値) {
                水平位置 = 0;
                垂直位置++;
            }
            if (垂直位置 >= 高さ値) {
                スクロール上方();
            }
        }
    }

    public char 文字(int 水平位置, int 垂直位置) {
        位置検証(水平位置, 垂直位置);
        return 文字値一覧[垂直位置 * 幅値 + 水平位置];
    }

    public void 入口消去処理() {
        Arrays.fill(文字値一覧, ' ');
        水平位置 = 0;
        垂直位置 = 0;
    }

    private void 文字印刷(int 水平位置, int 垂直位置, char 文字) {
        位置検証(水平位置, 垂直位置);
        文字値一覧[垂直位置 * 幅値 + 水平位置] = 文字;
    }

    private void スクロール上方() {
        System.arraycopy(文字値一覧, 幅値, 文字値一覧, 0, 幅値 * (高さ値 - 1));
        Arrays.fill(文字値一覧, 幅値 * (高さ値 - 1), 文字値一覧.length, ' ');
        垂直位置 = 高さ値 - 1;
    }

    private void 位置検証(int 水平位置, int 垂直位置) {
        if (水平位置 < 0 || 水平位置 >= 幅値 || 垂直位置 < 0 || 垂直位置 >= 高さ値) {
            throw new IllegalArgumentException("画面 위치가 올바르지 않습니다.");
        }
    }
}

