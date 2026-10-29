// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 中国香港特别行政区.JHkgOS.任务;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import 中国香港特别行政区.JHkgOS.内存空间.页管理器;
import 中国香港特别行政区.JHkgOS.文件系统.文件描述符表;

/** 管理进程标识符和轮转调度的就绪队列。 */
public final class 调度器 {
    private final 页管理器 页管理工作;
    private final Map<Integer, 进程值> 进程列表 = new HashMap<Integer, 进程值>();
    private final Queue<进程值> 就绪排队 = new ArrayDeque<进程值>();
    private int 下一标识符 = 1;

    public 调度器(页管理器 页管理工作) {
        this.页管理工作 = 页管理工作;
    }

    public 进程值 首位进程(文件描述符表 文件描述符) {
        进程值 新建进程 = new 进程值(分配标识符(), 0, 页管理工作.新建地址空间(), 文件描述符);
        进程列表.put(Integer.valueOf(新建进程.标识符值()), 新建进程);
        就绪排队.offer(新建进程);
        return 新建进程;
    }

    public 进程值 克隆值(进程值 父值) {
        进程值 子值 = new 进程值(
                分配标识符(),
                父值.标识符值(),
                页管理工作.克隆复制启用侧写入(父值.地址空间()),
                父值.文件描述符().克隆值());
        子值.设定程序跳出(父值.程序跳出());
        进程列表.put(Integer.valueOf(子值.标识符值()), 子值);
        就绪排队.offer(子值);
        return 子值;
    }

    public 进程值 下一进程() {
        int 检查个数 = 就绪排队.size();
        for (int 编号 = 0; 编号 < 检查个数; 编号++) {
            进程值 下一项目 = 就绪排队.poll();
            if (下一项目 != null && (下一项目.状态值() == 进程状态.准备 || 下一项目.状态值() == 进程状态.执行命令)) {
                下一项目.设定状态(进程状态.执行命令);
                就绪排队.offer(下一项目);
                return 下一项目;
            }
        }
        return null;
    }

    public int 等待状态用于子(进程值 父值, int 子标识符, boolean 非阻塞) {
        for (进程值 候选 : 进程列表.values()) {
            if (候选.父标识符() != 父值.标识符值()) {
                continue;
            }
            if (子标识符 > 0 && 候选.标识符值() != 子标识符) {
                continue;
            }
            if (候选.状态值() == 进程状态.退出程序) {
                int 结果 = (候选.退出代码() & 0xff) << 8;
                进程列表.remove(Integer.valueOf(候选.标识符值()));
                return 结果;
            }
            return 非阻塞 ? 0 : -11;
        }
        return -10;
    }

    public 进程值 查找进程(int 标识符值) {
        return 进程列表.get(Integer.valueOf(标识符值));
    }

    private int 分配标识符() {
        return 下一标识符++;
    }
}
