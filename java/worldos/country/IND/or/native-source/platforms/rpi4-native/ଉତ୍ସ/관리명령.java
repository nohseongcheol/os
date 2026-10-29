// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String 말(int ଅନୁକ୍ରମଣିକା) {
        if (ଅନୁକ୍ରମଣିକା==0) return "ipconfig";
        if (ଅନୁକ୍ରମଣିକା==1) return "ip";
        if (ଅନୁକ୍ରମଣିକା==2) return "ping";
        if (ଅନୁକ୍ରମଣିକା==3) return "route";
        if (ଅନୁକ୍ରମଣିକା==4) return "netstat";
        if (ଅନୁକ୍ରମଣିକା==5) return "ps";
        if (ଅନୁକ୍ରମଣିକା==6) return "top";
        if (ଅନୁକ୍ରମଣିକା==7) return "free";
        if (ଅନୁକ୍ରମଣିକା==8) return "df";
        if (ଅନୁକ୍ରମଣିକା==9) return "uptime";
        if (ଅନୁକ୍ରମଣିକା==10) return "poweroff";
        return "help";
    }
    static String 설명(int ଅନୁକ୍ରମଣିକା) {
        if (ଅନୁକ୍ରମଣିକା==0) return "IPv4 settings: address, netmask, gateway";
        if (ଅନୁକ୍ରମଣିକା==1) return "IPv4 interface and route tools";
        if (ଅନୁକ୍ରମଣିକା==2) return "ICMP echo and round-trip time";
        if (ଅନୁକ୍ରମଣିକା==3) return "Connected network and default route";
        if (ଅନୁକ୍ରମଣିକା==4) return "TCP/UDP sockets and traffic";
        if (ଅନୁକ୍ରମଣିକା==5) return "Kernel tasks and user processes";
        if (ଅନୁକ୍ରମଣିକା==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ଅନୁକ୍ରମଣିକା==7) return "Actual kernel pools and user mappings";
        if (ଅନୁକ୍ରମଣିକା==8) return "RAM filesystem capacity and file slots";
        if (ଅନୁକ୍ରମଣିକା==9) return "Time since boot";
        if (ଅନୁକ୍ରମଣିକା==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
