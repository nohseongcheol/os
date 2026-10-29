// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String சொல்_உரை(int அடைவு) {
        if (அடைவு==0) return "ipconfig";
        if (அடைவு==1) return "ip";
        if (அடைவு==2) return "ping";
        if (அடைவு==3) return "route";
        if (அடைவு==4) return "netstat";
        if (அடைவு==5) return "ps";
        if (அடைவு==6) return "top";
        if (அடைவு==7) return "free";
        if (அடைவு==8) return "df";
        if (அடைவு==9) return "uptime";
        if (அடைவு==10) return "poweroff";
        return "help";
    }
    static String 설명(int அடைவு) {
        if (அடைவு==0) return "IPv4 settings: address, netmask, gateway";
        if (அடைவு==1) return "IPv4 interface and route tools";
        if (அடைவு==2) return "ICMP echo and round-trip time";
        if (அடைவு==3) return "Connected network and default route";
        if (அடைவு==4) return "TCP/UDP sockets and traffic";
        if (அடைவு==5) return "Kernel tasks and user processes";
        if (அடைவு==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (அடைவு==7) return "Actual kernel pools and user mappings";
        if (அடைவு==8) return "RAM filesystem capacity and file slots";
        if (அடைவு==9) return "Time since boot";
        if (அடைவு==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
