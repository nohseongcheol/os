// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return ""; }
    static String Ọ̀rọ̀_SMS(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú==0) return "ipconfig";
        if (wá_atọ̀ka_àkóónú==1) return "ip";
        if (wá_atọ̀ka_àkóónú==2) return "ping";
        if (wá_atọ̀ka_àkóónú==3) return "route";
        if (wá_atọ̀ka_àkóónú==4) return "netstat";
        if (wá_atọ̀ka_àkóónú==5) return "ps";
        if (wá_atọ̀ka_àkóónú==6) return "top";
        if (wá_atọ̀ka_àkóónú==7) return "free";
        if (wá_atọ̀ka_àkóónú==8) return "df";
        if (wá_atọ̀ka_àkóónú==9) return "uptime";
        if (wá_atọ̀ka_àkóónú==10) return "poweroff";
        return "help";
    }
    static String 설명(int wá_atọ̀ka_àkóónú) {
        if (wá_atọ̀ka_àkóónú==0) return "IPv4 settings: address, netmask, gateway";
        if (wá_atọ̀ka_àkóónú==1) return "IPv4 interface and route tools";
        if (wá_atọ̀ka_àkóónú==2) return "ICMP echo and round-trip time";
        if (wá_atọ̀ka_àkóónú==3) return "Connected network and default route";
        if (wá_atọ̀ka_àkóónú==4) return "TCP/UDP sockets and traffic";
        if (wá_atọ̀ka_àkóónú==5) return "Kernel tasks and user processes";
        if (wá_atọ̀ka_àkóónú==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (wá_atọ̀ka_àkóónú==7) return "Actual kernel pools and user mappings";
        if (wá_atọ̀ka_àkóónú==8) return "RAM filesystem capacity and file slots";
        if (wá_atọ̀ka_àkóónú==9) return "Time since boot";
        if (wá_atọ̀ka_àkóónú==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
