// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "yoon liggéey melo-liggéey diiru-liggéey fay ndimbal"; }
    static String Word_SMS(int àlluwa_tur) {
        if (àlluwa_tur==0) return "ipconfig";
        if (àlluwa_tur==1) return "ip";
        if (àlluwa_tur==2) return "ping";
        if (àlluwa_tur==3) return "yoon";
        if (àlluwa_tur==4) return "netstat";
        if (àlluwa_tur==5) return "liggéey";
        if (àlluwa_tur==6) return "melo-liggéey";
        if (àlluwa_tur==7) return "free";
        if (àlluwa_tur==8) return "df";
        if (àlluwa_tur==9) return "diiru-liggéey";
        if (àlluwa_tur==10) return "fay";
        return "ndimbal";
    }
    static String 설명(int àlluwa_tur) {
        if (àlluwa_tur==0) return "IPv4 settings: address, netmask, gateway";
        if (àlluwa_tur==1) return "IPv4 interface and route tools";
        if (àlluwa_tur==2) return "ICMP echo and round-trip time";
        if (àlluwa_tur==3) return "Connected network and default route";
        if (àlluwa_tur==4) return "TCP/UDP sockets and traffic";
        if (àlluwa_tur==5) return "Kernel tasks and user processes";
        if (àlluwa_tur==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (àlluwa_tur==7) return "Actual kernel pools and user mappings";
        if (àlluwa_tur==8) return "RAM filesystem capacity and file slots";
        if (àlluwa_tur==9) return "Time since boot";
        if (àlluwa_tur==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
