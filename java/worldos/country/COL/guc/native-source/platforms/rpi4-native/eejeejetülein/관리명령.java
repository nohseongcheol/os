// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String 말(int ee_iyatialujuna) {
        if (ee_iyatialujuna==0) return "ipconfig";
        if (ee_iyatialujuna==1) return "ip";
        if (ee_iyatialujuna==2) return "ping";
        if (ee_iyatialujuna==3) return "route";
        if (ee_iyatialujuna==4) return "netstat";
        if (ee_iyatialujuna==5) return "ps";
        if (ee_iyatialujuna==6) return "top";
        if (ee_iyatialujuna==7) return "free";
        if (ee_iyatialujuna==8) return "df";
        if (ee_iyatialujuna==9) return "uptime";
        if (ee_iyatialujuna==10) return "poweroff";
        return "help";
    }
    static String 설명(int ee_iyatialujuna) {
        if (ee_iyatialujuna==0) return "IPv4 settings: address, netmask, gateway";
        if (ee_iyatialujuna==1) return "IPv4 interface and route tools";
        if (ee_iyatialujuna==2) return "ICMP echo and round-trip time";
        if (ee_iyatialujuna==3) return "Connected network and default route";
        if (ee_iyatialujuna==4) return "TCP/UDP sockets and traffic";
        if (ee_iyatialujuna==5) return "Kernel tasks and user processes";
        if (ee_iyatialujuna==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ee_iyatialujuna==7) return "Actual kernel pools and user mappings";
        if (ee_iyatialujuna==8) return "RAM filesystem capacity and file slots";
        if (ee_iyatialujuna==9) return "Time since boot";
        if (ee_iyatialujuna==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
