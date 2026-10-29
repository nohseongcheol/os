// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ip-жөндөөлөр тармак-дареги жаңырык-сыноо багыттар байланыштар процесстер иш-аракет эс-тутум сактагыч иштөө-убактысы өчүрүү жардам"; }
    static String Сөз_СМС(int индекс) {
        if (индекс==0) return "ip-жөндөөлөр";
        if (индекс==1) return "тармак-дареги";
        if (индекс==2) return "жаңырык-сыноо";
        if (индекс==3) return "багыттар";
        if (индекс==4) return "байланыштар";
        if (индекс==5) return "процесстер";
        if (индекс==6) return "иш-аракет";
        if (индекс==7) return "эс-тутум";
        if (индекс==8) return "сактагыч";
        if (индекс==9) return "иштөө-убактысы";
        if (индекс==10) return "өчүрүү";
        return "жардам";
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
