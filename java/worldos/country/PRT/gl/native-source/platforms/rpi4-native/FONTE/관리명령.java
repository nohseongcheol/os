// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Completadas_Word() { return ""; }
    static String Word_SMS(int ÍNDICE) {
        if (ÍNDICE==0) return "ipconfig";
        if (ÍNDICE==1) return "ip";
        if (ÍNDICE==2) return "ping";
        if (ÍNDICE==3) return "route";
        if (ÍNDICE==4) return "netstat";
        if (ÍNDICE==5) return "ps";
        if (ÍNDICE==6) return "top";
        if (ÍNDICE==7) return "free";
        if (ÍNDICE==8) return "df";
        if (ÍNDICE==9) return "uptime";
        if (ÍNDICE==10) return "poweroff";
        return "help";
    }
    static String 설명(int ÍNDICE) {
        if (ÍNDICE==0) return "IPv4 settings: address, netmask, gateway";
        if (ÍNDICE==1) return "IPv4 interface and route tools";
        if (ÍNDICE==2) return "ICMP echo and round-trip time";
        if (ÍNDICE==3) return "Connected network and default route";
        if (ÍNDICE==4) return "TCP/UDP sockets and traffic";
        if (ÍNDICE==5) return "Kernel tasks and user processes";
        if (ÍNDICE==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ÍNDICE==7) return "Actual kernel pools and user mappings";
        if (ÍNDICE==8) return "RAM filesystem capacity and file slots";
        if (ÍNDICE==9) return "Time since boot";
        if (ÍNDICE==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
