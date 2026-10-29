// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String завершено_Word() { return "настройка-ip сетевой-адрес проверка-отклика маршруты соединения процессы обзор-работы память хранилище время-работы выключить справка"; }
    static String Word_SMS(int ИНДЕКС) {
        if (ИНДЕКС==0) return "настройка-ip";
        if (ИНДЕКС==1) return "сетевой-адрес";
        if (ИНДЕКС==2) return "проверка-отклика";
        if (ИНДЕКС==3) return "маршруты";
        if (ИНДЕКС==4) return "соединения";
        if (ИНДЕКС==5) return "процессы";
        if (ИНДЕКС==6) return "обзор-работы";
        if (ИНДЕКС==7) return "память";
        if (ИНДЕКС==8) return "хранилище";
        if (ИНДЕКС==9) return "время-работы";
        if (ИНДЕКС==10) return "выключить";
        return "справка";
    }
    static String описание(int ИНДЕКС) {
        if (ИНДЕКС==0) return "IPv4 settings: address, netmask, gateway";
        if (ИНДЕКС==1) return "IPv4 interface and route tools";
        if (ИНДЕКС==2) return "ICMP echo and round-trip time";
        if (ИНДЕКС==3) return "Connected network and default route";
        if (ИНДЕКС==4) return "TCP/UDP sockets and traffic";
        if (ИНДЕКС==5) return "Kernel tasks and user processes";
        if (ИНДЕКС==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ИНДЕКС==7) return "Actual kernel pools and user mappings";
        if (ИНДЕКС==8) return "RAM filesystem capacity and file slots";
        if (ИНДЕКС==9) return "Time since boot";
        if (ИНДЕКС==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
