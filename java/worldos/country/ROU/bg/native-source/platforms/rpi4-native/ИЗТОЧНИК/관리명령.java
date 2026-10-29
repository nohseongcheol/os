// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Завършени_Игри_с_думи() { return "настройка-ip мрежов-адрес проверка-отговор маршрути връзки процеси преглед-работа памет хранилище време-работа изключване помощ"; }
    static String Игри_с_думи_Текст(int индекс) {
        if (индекс==0) return "настройка-ip";
        if (индекс==1) return "мрежов-адрес";
        if (индекс==2) return "проверка-отговор";
        if (индекс==3) return "маршрути";
        if (индекс==4) return "връзки";
        if (индекс==5) return "процеси";
        if (индекс==6) return "преглед-работа";
        if (индекс==7) return "памет";
        if (индекс==8) return "хранилище";
        if (индекс==9) return "време-работа";
        if (индекс==10) return "изключване";
        return "помощ";
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
