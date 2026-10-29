// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 蒙古.JMngOS.任务;

import 蒙古.JMngOS.内存空间.页管理器;
import 蒙古.JMngOS.文件系统.文件描述符表;

public final class 进程值 {
    private final int 标识符值;
    private final int 父标识符;
    private final 页管理器.地址空间 地址空间;
    private final 文件描述符表 文件描述符;
    private 进程状态 状态值 = 进程状态.准备;
    private int 退出代码;
    private int 程序跳出 = 0x06000000;
    private int 执行状态开始地址;
    private String[] 执行状态参数 = new String[0];
    private String[] 环境值 = new String[0];

    进程值(int 标识符值, int 父标识符, 页管理器.地址空间 地址空间, 文件描述符表 文件描述符) {
        this.标识符值 = 标识符值;
        this.父标识符 = 父标识符;
        this.地址空间 = 地址空间;
        this.文件描述符 = 文件描述符;
    }

    public int 标识符值() {
        return 标识符值;
    }

    public int 父标识符() {
        return 父标识符;
    }

    public 页管理器.地址空间 地址空间() {
        return 地址空间;
    }

    public 文件描述符表 文件描述符() {
        return 文件描述符;
    }

    public 进程状态 状态值() {
        return 状态值;
    }

    public void 设定状态(进程状态 新建状态) {
        状态值 = 新建状态;
    }

    public int 退出代码() {
        return 退出代码;
    }

    public void 退出程序(int 值) {
        退出代码 = 值 & 0xff;
        状态值 = 进程状态.退出程序;
    }

    public int 程序跳出() {
        return 程序跳出;
    }

    public void 设定程序跳出(int 新建结束) {
        if (新建结束 < 0x06000000 || 新建结束 > 0x07000000) {
            throw new IllegalArgumentException("程序 结尾 범위를 벗어났습니다.");
        }
        程序跳出 = 新建结束;
    }

    public void 设定执行状态上下文(int 开始地址, String[] 形参参数, String[] 环境) {
        执行状态开始地址 = 开始地址;
        执行状态参数 = 形参参数.clone();
        环境值 = 环境.clone();
    }

    public int 执行状态开始地址() { return 执行状态开始地址; }
    public String[] 执行状态参数() { return 执行状态参数.clone(); }
    public String[] 环境值() { return 环境值.clone(); }
}
