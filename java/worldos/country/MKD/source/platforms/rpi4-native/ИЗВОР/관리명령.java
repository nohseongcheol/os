// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ип-поставки мрежна-адреса проверка-одговор патеки врски процеси активност меморија складирање време-работа исклучи помош"; }
    static String Word_СМС(int INDEX) {
        if (INDEX==0) return "ип-поставки";
        if (INDEX==1) return "мрежна-адреса";
        if (INDEX==2) return "проверка-одговор";
        if (INDEX==3) return "патеки";
        if (INDEX==4) return "врски";
        if (INDEX==5) return "процеси";
        if (INDEX==6) return "активност";
        if (INDEX==7) return "меморија";
        if (INDEX==8) return "складирање";
        if (INDEX==9) return "време-работа";
        if (INDEX==10) return "исклучи";
        return "помош";
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
