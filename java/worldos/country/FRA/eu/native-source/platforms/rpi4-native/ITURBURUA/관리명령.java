// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Osatutakoak_Word() { return ""; }
    static String Word_SMS(int INDIZE) {
        if (INDIZE==0) return "ipconfig";
        if (INDIZE==1) return "ip";
        if (INDIZE==2) return "ping";
        if (INDIZE==3) return "route";
        if (INDIZE==4) return "netstat";
        if (INDIZE==5) return "ps";
        if (INDIZE==6) return "top";
        if (INDIZE==7) return "free";
        if (INDIZE==8) return "df";
        if (INDIZE==9) return "uptime";
        if (INDIZE==10) return "poweroff";
        return "help";
    }
    static String 설명(int INDIZE) {
        if (INDIZE==0) return "IPv4 settings: address, netmask, gateway";
        if (INDIZE==1) return "IPv4 interface and route tools";
        if (INDIZE==2) return "ICMP echo and round-trip time";
        if (INDIZE==3) return "Connected network and default route";
        if (INDIZE==4) return "TCP/UDP sockets and traffic";
        if (INDIZE==5) return "Kernel tasks and user processes";
        if (INDIZE==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDIZE==7) return "Actual kernel pools and user mappings";
        if (INDIZE==8) return "RAM filesystem capacity and file slots";
        if (INDIZE==9) return "Time since boot";
        if (INDIZE==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
