// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "usanidi-ip anwani-ip jaribio-mwangwi njia miunganisho michakato shughuli kumbukumbu hifadhi muda-kazi zima msaada"; }
    static String Neno_SMS(int kielezo) {
        if (kielezo==0) return "usanidi-ip";
        if (kielezo==1) return "anwani-ip";
        if (kielezo==2) return "jaribio-mwangwi";
        if (kielezo==3) return "njia";
        if (kielezo==4) return "miunganisho";
        if (kielezo==5) return "michakato";
        if (kielezo==6) return "shughuli";
        if (kielezo==7) return "kumbukumbu";
        if (kielezo==8) return "hifadhi";
        if (kielezo==9) return "muda-kazi";
        if (kielezo==10) return "zima";
        return "msaada";
    }
    static String 설명(int kielezo) {
        if (kielezo==0) return "IPv4 settings: address, netmask, gateway";
        if (kielezo==1) return "IPv4 interface and route tools";
        if (kielezo==2) return "ICMP echo and round-trip time";
        if (kielezo==3) return "Connected network and default route";
        if (kielezo==4) return "TCP/UDP sockets and traffic";
        if (kielezo==5) return "Kernel tasks and user processes";
        if (kielezo==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (kielezo==7) return "Actual kernel pools and user mappings";
        if (kielezo==8) return "RAM filesystem capacity and file slots";
        if (kielezo==9) return "Time since boot";
        if (kielezo==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
