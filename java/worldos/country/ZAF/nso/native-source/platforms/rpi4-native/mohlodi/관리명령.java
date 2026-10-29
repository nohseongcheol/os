// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Thalokontšu_SMS(int lokela) {
        if (lokela==0) return "ipconfig";
        if (lokela==1) return "ip";
        if (lokela==2) return "ping";
        if (lokela==3) return "route";
        if (lokela==4) return "netstat";
        if (lokela==5) return "ps";
        if (lokela==6) return "top";
        if (lokela==7) return "free";
        if (lokela==8) return "df";
        if (lokela==9) return "uptime";
        if (lokela==10) return "poweroff";
        return "help";
    }
    static String 설명(int lokela) {
        if (lokela==0) return "IPv4 settings: address, netmask, gateway";
        if (lokela==1) return "IPv4 interface and route tools";
        if (lokela==2) return "ICMP echo and round-trip time";
        if (lokela==3) return "Connected network and default route";
        if (lokela==4) return "TCP/UDP sockets and traffic";
        if (lokela==5) return "Kernel tasks and user processes";
        if (lokela==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (lokela==7) return "Actual kernel pools and user mappings";
        if (lokela==8) return "RAM filesystem capacity and file slots";
        if (lokela==9) return "Time since boot";
        if (lokela==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
