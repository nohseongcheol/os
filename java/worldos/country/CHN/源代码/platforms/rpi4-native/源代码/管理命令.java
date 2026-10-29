// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 管理命令 {
    static String 已完成机器字() { return "网络设置 网络地址 回声测试 路由表 网络状态 进程列表 运行概况 内存状态 存储容量 运行时间 关机 帮助"; }
    static String 机器字文本(int 编号) {
        if (编号==0) return "网络设置";
        if (编号==1) return "网络地址";
        if (编号==2) return "回声测试";
        if (编号==3) return "路由表";
        if (编号==4) return "网络状态";
        if (编号==5) return "进程列表";
        if (编号==6) return "运行概况";
        if (编号==7) return "内存状态";
        if (编号==8) return "存储容量";
        if (编号==9) return "运行时间";
        if (编号==10) return "关机";
        return "帮助";
    }
    static String 说明(int 编号) {
        if (编号==0) return "IPv4 地址、子网掩码与网关设置";
        if (编号==1) return "IPv4 接口与路由工具";
        if (编号==2) return "ICMP 回声与往返时间";
        if (编号==3) return "直连网络与默认路由";
        if (编号==4) return "TCP/UDP 连接与流量";
        if (编号==5) return "内核任务与用户进程";
        if (编号==6) return "刷新任务和内存; q 或 Ctrl+C 退出";
        if (编号==7) return "实际内核内存池与用户映射";
        if (编号==8) return "RAM 文件系统容量和文件槽";
        if (编号==9) return "启动后的运行时间";
        if (编号==10) return "关闭系统; RAM 文件不会保留";
        return "命令与中文名称";
    }
}
