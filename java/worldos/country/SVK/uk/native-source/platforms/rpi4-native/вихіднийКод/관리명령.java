// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String Виконано_Ігри_в_слова() { return "налаштування-ip мережева-адреса перевірка-відгуку маршрути з’єднання процеси огляд-роботи пам’ять сховище час-роботи вимкнути довідка"; }
    static String Ігри_в_слова_Текст(int індекс) {
        if (індекс==0) return "налаштування-ip";
        if (індекс==1) return "мережева-адреса";
        if (індекс==2) return "перевірка-відгуку";
        if (індекс==3) return "маршрути";
        if (індекс==4) return "з’єднання";
        if (індекс==5) return "процеси";
        if (індекс==6) return "огляд-роботи";
        if (індекс==7) return "пам’ять";
        if (індекс==8) return "сховище";
        if (індекс==9) return "час-роботи";
        if (індекс==10) return "вимкнути";
        return "довідка";
    }
    static String 설명(int індекс) {
        if (індекс==0) return "IPv4 settings: address, netmask, gateway";
        if (індекс==1) return "IPv4 interface and route tools";
        if (індекс==2) return "ICMP echo and round-trip time";
        if (індекс==3) return "Connected network and default route";
        if (індекс==4) return "TCP/UDP sockets and traffic";
        if (індекс==5) return "Kernel tasks and user processes";
        if (індекс==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (індекс==7) return "Actual kernel pools and user mappings";
        if (індекс==8) return "RAM filesystem capacity and file slots";
        if (індекс==9) return "Time since boot";
        if (індекс==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
