// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Lefoko_SMS(int tshupane) {
        if (tshupane==0) return "ipconfig";
        if (tshupane==1) return "ip";
        if (tshupane==2) return "ping";
        if (tshupane==3) return "route";
        if (tshupane==4) return "netstat";
        if (tshupane==5) return "ps";
        if (tshupane==6) return "top";
        if (tshupane==7) return "free";
        if (tshupane==8) return "df";
        if (tshupane==9) return "uptime";
        if (tshupane==10) return "poweroff";
        return "help";
    }
    static String 설명(int tshupane) {
        if (tshupane==0) return "IPv4 settings: address, netmask, gateway";
        if (tshupane==1) return "IPv4 interface and route tools";
        if (tshupane==2) return "ICMP echo and round-trip time";
        if (tshupane==3) return "Connected network and default route";
        if (tshupane==4) return "TCP/UDP sockets and traffic";
        if (tshupane==5) return "Kernel tasks and user processes";
        if (tshupane==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (tshupane==7) return "Actual kernel pools and user mappings";
        if (tshupane==8) return "RAM filesystem capacity and file slots";
        if (tshupane==9) return "Time since boot";
        if (tshupane==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
