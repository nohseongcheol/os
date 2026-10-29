// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 马来西亚.JMysOS.内核;

import 马来西亚.JMysOS.内存空间.内存管理器;
import 马来西亚.JMysOS.内存空间.页管理器;
import 马来西亚.JMysOS.输入值.输入管理器;
import 马来西亚.JMysOS.任务.进程值;
import 马来西亚.JMysOS.任务.调度器;
import 马来西亚.JMysOS.系统调用.系统调用;
import 马来西亚.JMysOS.文件系统.文件描述符表;
import 马来西亚.JMysOS.文件系统.文件系统;

/** 负责 Java 管理内核的组装和启动。 */
public final class 内核 {
    private final 硬件值 设备;
    private final 内存管理器 内存空间 = new 内存管理器(32 * 1024 * 1024);
    private final 页管理器 页管理工作 = new 页管理器();
    private final 文件系统 文件系统 = new 文件系统();
    private final 调度器 调度器 = new 调度器(页管理工作);
    private final 输入管理器 输入管理工作 = new 输入管理器(256);
    private final 进程值 首位进程;
    private final 系统调用 系统调用;

    public 内核(硬件值 设备) {
        this.设备 = 设备;
        首位进程 = 调度器.首位进程(new 文件描述符表(文件系统));
        系统调用 = new 系统调用(文件系统, 页管理工作, 调度器, 设备, 输入管理工作);
    }

    public void 运行() {
        设备.串行输出("=== JMysOS 관리 内核值 ===\n");
    }

    public void 执行步骤() {
        设备.停机CPU();
    }

    public 内存管理器 内存空间() {
        return 内存空间;
    }

    public 页管理器 页管理工作() {
        return 页管理工作;
    }

    public 文件系统 文件系统() {
        return 文件系统;
    }

    public 调度器 调度器() {
        return 调度器;
    }

    public 输入管理器 输入管理工作() {
        return 输入管理工作;
    }

    public 进程值 首位进程() {
        return 首位进程;
    }

    public 系统调用 系统调用() {
        return 系统调用;
    }
}
