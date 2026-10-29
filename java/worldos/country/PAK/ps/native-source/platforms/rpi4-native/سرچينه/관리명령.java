// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String 말(int لړیال) {
        if (لړیال==0) return "ipconfig";
        if (لړیال==1) return "ip";
        if (لړیال==2) return "ping";
        if (لړیال==3) return "route";
        if (لړیال==4) return "netstat";
        if (لړیال==5) return "ps";
        if (لړیال==6) return "top";
        if (لړیال==7) return "free";
        if (لړیال==8) return "df";
        if (لړیال==9) return "uptime";
        if (لړیال==10) return "poweroff";
        return "help";
    }
    static String 설명(int لړیال) {
        if (لړیال==0) return "IPv4 settings: address, netmask, gateway";
        if (لړیال==1) return "IPv4 interface and route tools";
        if (لړیال==2) return "ICMP echo and round-trip time";
        if (لړیال==3) return "Connected network and default route";
        if (لړیال==4) return "TCP/UDP sockets and traffic";
        if (لړیال==5) return "Kernel tasks and user processes";
        if (لړیال==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (لړیال==7) return "Actual kernel pools and user mappings";
        if (لړیال==8) return "RAM filesystem capacity and file slots";
        if (لړیال==9) return "Time since boot";
        if (لړیال==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
