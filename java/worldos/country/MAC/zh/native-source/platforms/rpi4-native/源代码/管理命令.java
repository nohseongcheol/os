// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 管理命令 {
    static String 已完成机器字() { return ""; }
    static String 机器字文本(int 编号) {
        if (编号==0) return "ipconfig";
        if (编号==1) return "ip";
        if (编号==2) return "ping";
        if (编号==3) return "route";
        if (编号==4) return "netstat";
        if (编号==5) return "ps";
        if (编号==6) return "top";
        if (编号==7) return "free";
        if (编号==8) return "df";
        if (编号==9) return "uptime";
        if (编号==10) return "poweroff";
        return "help";
    }
    static String 说明(int 编号) {
        if (编号==0) return "IPv4 settings: address, netmask, gateway";
        if (编号==1) return "IPv4 interface and route tools";
        if (编号==2) return "ICMP echo and round-trip time";
        if (编号==3) return "Connected network and default route";
        if (编号==4) return "TCP/UDP sockets and traffic";
        if (编号==5) return "Kernel tasks and user processes";
        if (编号==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (编号==7) return "Actual kernel pools and user mappings";
        if (编号==8) return "RAM filesystem capacity and file slots";
        if (编号==9) return "Time since boot";
        if (编号==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
