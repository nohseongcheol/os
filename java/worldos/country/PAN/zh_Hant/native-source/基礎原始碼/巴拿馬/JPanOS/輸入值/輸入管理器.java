// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 巴拿馬.JPanOS.輸入值;

import java.util.ArrayDeque;
import java.util.Queue;

/** 在中斷與受管理程式之間安全傳遞輸入事件。 */
public final class 輸入管理器 {
    private final Queue<輸入事件> 事件列列表 = new ArrayDeque<輸入事件>();
    private final int 最大事件個數;
    private int 已丟棄數事件個數;

    public 輸入管理器(int 最大事件個數) {
        if (最大事件個數 <= 0) {
            throw new IllegalArgumentException("事件 수가 올바르지 않습니다.");
        }
        this.最大事件個數 = 最大事件個數;
    }

    public synchronized void 鍵向下(int 鍵資料) {
        放入值(new 輸入事件(輸入事件.種類值.鍵向下, 鍵資料 & 0xff, 0));
    }

    public synchronized void 鍵向上(int 鍵資料) {
        放入值(new 輸入事件(輸入事件.種類值.鍵向上, 鍵資料 & 0xff, 0));
    }

    public synchronized void 鼠標移動量(int 水平位置, int 垂直位置) {
        放入值(new 輸入事件(輸入事件.種類值.鼠標移動量, 水平位置, 垂直位置));
    }

    public synchronized 輸入事件 下一事件() {
        return 事件列列表.poll();
    }

    public synchronized int 已丟棄數事件個數() {
        return 已丟棄數事件個數;
    }

    private void 放入值(輸入事件 事件) {
        if (事件列列表.size() == 最大事件個數) {
            事件列列表.poll();
            已丟棄數事件個數++;
        }
        事件列列表.offer(事件);
    }
}

