// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "танзими-ip суроғаи-шабака санҷиши-акси-садо масирҳо пайвастҳо равандҳо фаъолият хотира захирагоҳ вақти-кор хомӯш-кардан ёрӣ"; }
    static String Калимабозӣ_Матн(int индекс) {
        if (индекс==0) return "танзими-ip";
        if (индекс==1) return "суроғаи-шабака";
        if (индекс==2) return "санҷиши-акси-садо";
        if (индекс==3) return "масирҳо";
        if (индекс==4) return "пайвастҳо";
        if (индекс==5) return "равандҳо";
        if (индекс==6) return "фаъолият";
        if (индекс==7) return "хотира";
        if (индекс==8) return "захирагоҳ";
        if (индекс==9) return "вақти-кор";
        if (индекс==10) return "хомӯш-кардан";
        return "ёрӣ";
    }
    static String 설명(int индекс) {
        if (индекс==0) return "IPv4 settings: address, netmask, gateway";
        if (индекс==1) return "IPv4 interface and route tools";
        if (индекс==2) return "ICMP echo and round-trip time";
        if (индекс==3) return "Connected network and default route";
        if (индекс==4) return "TCP/UDP sockets and traffic";
        if (индекс==5) return "Kernel tasks and user processes";
        if (индекс==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (индекс==7) return "Actual kernel pools and user mappings";
        if (индекс==8) return "RAM filesystem capacity and file slots";
        if (индекс==9) return "Time since boot";
        if (индекс==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
