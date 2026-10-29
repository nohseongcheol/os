// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String لفظ_متن(int اشاریہ) {
        if (اشاریہ==0) return "ipconfig";
        if (اشاریہ==1) return "ip";
        if (اشاریہ==2) return "ping";
        if (اشاریہ==3) return "route";
        if (اشاریہ==4) return "netstat";
        if (اشاریہ==5) return "ps";
        if (اشاریہ==6) return "top";
        if (اشاریہ==7) return "free";
        if (اشاریہ==8) return "df";
        if (اشاریہ==9) return "uptime";
        if (اشاریہ==10) return "poweroff";
        return "help";
    }
    static String 설명(int اشاریہ) {
        if (اشاریہ==0) return "IPv4 settings: address, netmask, gateway";
        if (اشاریہ==1) return "IPv4 interface and route tools";
        if (اشاریہ==2) return "ICMP echo and round-trip time";
        if (اشاریہ==3) return "Connected network and default route";
        if (اشاریہ==4) return "TCP/UDP sockets and traffic";
        if (اشاریہ==5) return "Kernel tasks and user processes";
        if (اشاریہ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (اشاریہ==7) return "Actual kernel pools and user mappings";
        if (اشاریہ==8) return "RAM filesystem capacity and file slots";
        if (اشاریہ==9) return "Time since boot";
        if (اشاریہ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
