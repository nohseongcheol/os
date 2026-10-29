// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String 말(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==0) return "ipconfig";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==1) return "ip";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==2) return "ping";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==3) return "route";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==4) return "netstat";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==5) return "ps";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==6) return "top";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==7) return "free";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==8) return "df";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==9) return "uptime";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==10) return "poweroff";
        return "help";
    }
    static String 설명(int ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ) {
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==0) return "IPv4 settings: address, netmask, gateway";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==1) return "IPv4 interface and route tools";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==2) return "ICMP echo and round-trip time";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==3) return "Connected network and default route";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==4) return "TCP/UDP sockets and traffic";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==5) return "Kernel tasks and user processes";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==7) return "Actual kernel pools and user mappings";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==8) return "RAM filesystem capacity and file slots";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==9) return "Time since boot";
        if (ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
