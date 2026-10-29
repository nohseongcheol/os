// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Lõpetatud_Word() { return "ip-seaded võrguaadress kajakatse marsruudid ühendused protsessid tegevus mälu salvestusruum tööaeg lülita-välja abi"; }
    static String Word_SMS(int INDEX) {
        if (INDEX==0) return "ip-seaded";
        if (INDEX==1) return "võrguaadress";
        if (INDEX==2) return "kajakatse";
        if (INDEX==3) return "marsruudid";
        if (INDEX==4) return "ühendused";
        if (INDEX==5) return "protsessid";
        if (INDEX==6) return "tegevus";
        if (INDEX==7) return "mälu";
        if (INDEX==8) return "salvestusruum";
        if (INDEX==9) return "tööaeg";
        if (INDEX==10) return "lülita-välja";
        return "abi";
    }
    static String 설명(int INDEX) {
        if (INDEX==0) return "IPv4 settings: address, netmask, gateway";
        if (INDEX==1) return "IPv4 interface and route tools";
        if (INDEX==2) return "ICMP echo and round-trip time";
        if (INDEX==3) return "Connected network and default route";
        if (INDEX==4) return "TCP/UDP sockets and traffic";
        if (INDEX==5) return "Kernel tasks and user processes";
        if (INDEX==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (INDEX==7) return "Actual kernel pools and user mappings";
        if (INDEX==8) return "RAM filesystem capacity and file slots";
        if (INDEX==9) return "Time since boot";
        if (INDEX==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
