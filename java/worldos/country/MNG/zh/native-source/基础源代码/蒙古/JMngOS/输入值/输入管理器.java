// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蒙古.JMngOS.输入值;

import java.util.ArrayDeque;
import java.util.Queue;

/** 在中断与受管理代码之间安全传递输入事件。 */
public final class 输入管理器 {
    private final Queue<输入事件> 事件列列表 = new ArrayDeque<输入事件>();
    private final int 最大事件个数;
    private int 已丢弃数事件个数;

    public 输入管理器(int 最大事件个数) {
        if (最大事件个数 <= 0) {
            throw new IllegalArgumentException("事件 수가 올바르지 않습니다.");
        }
        this.最大事件个数 = 最大事件个数;
    }

    public synchronized void 键向下(int 键数据) {
        放入值(new 输入事件(输入事件.种类值.键向下, 键数据 & 0xff, 0));
    }

    public synchronized void 键向上(int 键数据) {
        放入值(new 输入事件(输入事件.种类值.键向上, 键数据 & 0xff, 0));
    }

    public synchronized void 鼠标移动量(int 水平位置, int 垂直位置) {
        放入值(new 输入事件(输入事件.种类值.鼠标移动量, 水平位置, 垂直位置));
    }

    public synchronized 输入事件 下一事件() {
        return 事件列列表.poll();
    }

    public synchronized int 已丢弃数事件个数() {
        return 已丢弃数事件个数;
    }

    private void 放入值(输入事件 事件) {
        if (事件列列表.size() == 最大事件个数) {
            事件列列表.poll();
            已丢弃数事件个数++;
        }
        事件列列表.offer(事件);
    }
}

