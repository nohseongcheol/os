// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "litlhophiso-ip aterese-ip teko-karabo litsela likhokahano mesebetsi tšebetso mohopolo polokelo nako-tshebetso tima thuso"; }
    static String 말(int 번호) {
        if (번호==0) return "litlhophiso-ip";
        if (번호==1) return "aterese-ip";
        if (번호==2) return "teko-karabo";
        if (번호==3) return "litsela";
        if (번호==4) return "likhokahano";
        if (번호==5) return "mesebetsi";
        if (번호==6) return "tšebetso";
        if (번호==7) return "mohopolo";
        if (번호==8) return "polokelo";
        if (번호==9) return "nako-tshebetso";
        if (번호==10) return "tima";
        return "thuso";
    }
    static String 설명(int 번호) {
        if (번호==0) return "IPv4 settings: address, netmask, gateway";
        if (번호==1) return "IPv4 interface and route tools";
        if (번호==2) return "ICMP echo and round-trip time";
        if (번호==3) return "Connected network and default route";
        if (번호==4) return "TCP/UDP sockets and traffic";
        if (번호==5) return "Kernel tasks and user processes";
        if (번호==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (번호==7) return "Actual kernel pools and user mappings";
        if (번호==8) return "RAM filesystem capacity and file slots";
        if (번호==9) return "Time since boot";
        if (번호==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
