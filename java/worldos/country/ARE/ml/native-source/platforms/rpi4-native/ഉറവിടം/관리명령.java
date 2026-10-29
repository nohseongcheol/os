// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String വാക്ക്_ലിഖിതം(int സൂചിക) {
        if (സൂചിക==0) return "ipconfig";
        if (സൂചിക==1) return "ip";
        if (സൂചിക==2) return "ping";
        if (സൂചിക==3) return "route";
        if (സൂചിക==4) return "netstat";
        if (സൂചിക==5) return "ps";
        if (സൂചിക==6) return "top";
        if (സൂചിക==7) return "free";
        if (സൂചിക==8) return "df";
        if (സൂചിക==9) return "uptime";
        if (സൂചിക==10) return "poweroff";
        return "help";
    }
    static String 설명(int സൂചിക) {
        if (സൂചിക==0) return "IPv4 settings: address, netmask, gateway";
        if (സൂചിക==1) return "IPv4 interface and route tools";
        if (സൂചിക==2) return "ICMP echo and round-trip time";
        if (സൂചിക==3) return "Connected network and default route";
        if (സൂചിക==4) return "TCP/UDP sockets and traffic";
        if (സൂചിക==5) return "Kernel tasks and user processes";
        if (സൂചിക==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (സൂചിക==7) return "Actual kernel pools and user mappings";
        if (സൂചിക==8) return "RAM filesystem capacity and file slots";
        if (സൂചിക==9) return "Time since boot";
        if (സൂചിക==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
