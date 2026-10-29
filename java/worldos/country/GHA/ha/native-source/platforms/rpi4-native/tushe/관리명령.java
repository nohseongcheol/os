// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Microsoft_Word_SMS(int Indes) {
        if (Indes==0) return "ipconfig";
        if (Indes==1) return "ip";
        if (Indes==2) return "ping";
        if (Indes==3) return "route";
        if (Indes==4) return "netstat";
        if (Indes==5) return "ps";
        if (Indes==6) return "top";
        if (Indes==7) return "free";
        if (Indes==8) return "df";
        if (Indes==9) return "uptime";
        if (Indes==10) return "poweroff";
        return "help";
    }
    static String 설명(int Indes) {
        if (Indes==0) return "IPv4 settings: address, netmask, gateway";
        if (Indes==1) return "IPv4 interface and route tools";
        if (Indes==2) return "ICMP echo and round-trip time";
        if (Indes==3) return "Connected network and default route";
        if (Indes==4) return "TCP/UDP sockets and traffic";
        if (Indes==5) return "Kernel tasks and user processes";
        if (Indes==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (Indes==7) return "Actual kernel pools and user mappings";
        if (Indes==8) return "RAM filesystem capacity and file slots";
        if (Indes==9) return "Time since boot";
        if (Indes==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
