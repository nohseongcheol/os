// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String ورڊ_متن(int ابتدائي) {
        if (ابتدائي==0) return "ipconfig";
        if (ابتدائي==1) return "ip";
        if (ابتدائي==2) return "ping";
        if (ابتدائي==3) return "route";
        if (ابتدائي==4) return "netstat";
        if (ابتدائي==5) return "ps";
        if (ابتدائي==6) return "top";
        if (ابتدائي==7) return "free";
        if (ابتدائي==8) return "df";
        if (ابتدائي==9) return "uptime";
        if (ابتدائي==10) return "poweroff";
        return "help";
    }
    static String 설명(int ابتدائي) {
        if (ابتدائي==0) return "IPv4 settings: address, netmask, gateway";
        if (ابتدائي==1) return "IPv4 interface and route tools";
        if (ابتدائي==2) return "ICMP echo and round-trip time";
        if (ابتدائي==3) return "Connected network and default route";
        if (ابتدائي==4) return "TCP/UDP sockets and traffic";
        if (ابتدائي==5) return "Kernel tasks and user processes";
        if (ابتدائي==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ابتدائي==7) return "Actual kernel pools and user mappings";
        if (ابتدائي==8) return "RAM filesystem capacity and file slots";
        if (ابتدائي==9) return "Time since boot";
        if (ابتدائي==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
