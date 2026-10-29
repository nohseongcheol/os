// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ип-поставке мрежна-адреса провјера-одзива путање везе процеси активност меморија похрана вријеме-рада искључи помоћ"; }
    static String 말(int индекс) {
        if (индекс==0) return "ип-поставке";
        if (индекс==1) return "мрежна-адреса";
        if (индекс==2) return "провјера-одзива";
        if (индекс==3) return "путање";
        if (индекс==4) return "везе";
        if (индекс==5) return "процеси";
        if (индекс==6) return "активност";
        if (индекс==7) return "меморија";
        if (индекс==8) return "похрана";
        if (индекс==9) return "вријеме-рада";
        if (индекс==10) return "искључи";
        return "помоћ";
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
