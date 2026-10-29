// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "наладка-ip сеткавы-адрас праверка-водгуку маршруты злучэнні працэсы агляд-працы памяць сховішча час-працы выключыць даведка"; }
    static String Гульні_са_словамі_Тэкст(int індэкс) {
        if (індэкс==0) return "наладка-ip";
        if (індэкс==1) return "сеткавы-адрас";
        if (індэкс==2) return "праверка-водгуку";
        if (індэкс==3) return "маршруты";
        if (індэкс==4) return "злучэнні";
        if (індэкс==5) return "працэсы";
        if (індэкс==6) return "агляд-працы";
        if (індэкс==7) return "памяць";
        if (індэкс==8) return "сховішча";
        if (індэкс==9) return "час-працы";
        if (індэкс==10) return "выключыць";
        return "даведка";
    }
    static String 설명(int індэкс) {
        if (індэкс==0) return "IPv4 settings: address, netmask, gateway";
        if (індэкс==1) return "IPv4 interface and route tools";
        if (індэкс==2) return "ICMP echo and round-trip time";
        if (індэкс==3) return "Connected network and default route";
        if (індэкс==4) return "TCP/UDP sockets and traffic";
        if (індэкс==5) return "Kernel tasks and user processes";
        if (індэкс==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (індэкс==7) return "Actual kernel pools and user mappings";
        if (індэкс==8) return "RAM filesystem capacity and file slots";
        if (індэкс==9) return "Time since boot";
        if (індэкс==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
