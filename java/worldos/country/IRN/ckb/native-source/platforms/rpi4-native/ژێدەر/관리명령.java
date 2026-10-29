// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String وشە_دەق(int پێرست) {
        if (پێرست==0) return "ipconfig";
        if (پێرست==1) return "ip";
        if (پێرست==2) return "ping";
        if (پێرست==3) return "route";
        if (پێرست==4) return "netstat";
        if (پێرست==5) return "ps";
        if (پێرست==6) return "top";
        if (پێرست==7) return "free";
        if (پێرست==8) return "df";
        if (پێرست==9) return "uptime";
        if (پێرست==10) return "poweroff";
        return "help";
    }
    static String 설명(int پێرست) {
        if (پێرست==0) return "IPv4 settings: address, netmask, gateway";
        if (پێرست==1) return "IPv4 interface and route tools";
        if (پێرست==2) return "ICMP echo and round-trip time";
        if (پێرست==3) return "Connected network and default route";
        if (پێرست==4) return "TCP/UDP sockets and traffic";
        if (پێرست==5) return "Kernel tasks and user processes";
        if (پێرست==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (پێرست==7) return "Actual kernel pools and user mappings";
        if (پێرست==8) return "RAM filesystem capacity and file slots";
        if (پێرست==9) return "Time since boot";
        if (پێرست==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
