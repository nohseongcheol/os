// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "ip-կարգավորում ցանցի-հասցե արձագանքի-ստուգում երթուղիներ կապեր գործընթացներ գործունեություն հիշողություն պահեստ աշխատանքի-ժամանակ անջատել օգնություն"; }
    static String Բառ_Գրվածք(int դասիչ) {
        if (դասիչ==0) return "ip-կարգավորում";
        if (դասիչ==1) return "ցանցի-հասցե";
        if (դասիչ==2) return "արձագանքի-ստուգում";
        if (դասիչ==3) return "երթուղիներ";
        if (դասիչ==4) return "կապեր";
        if (դասիչ==5) return "գործընթացներ";
        if (դասիչ==6) return "գործունեություն";
        if (դասիչ==7) return "հիշողություն";
        if (դասիչ==8) return "պահեստ";
        if (դասիչ==9) return "աշխատանքի-ժամանակ";
        if (դասիչ==10) return "անջատել";
        return "օգնություն";
    }
    static String 설명(int դասիչ) {
        if (դասիչ==0) return "IPv4 settings: address, netmask, gateway";
        if (դասիչ==1) return "IPv4 interface and route tools";
        if (դասիչ==2) return "ICMP echo and round-trip time";
        if (դասիչ==3) return "Connected network and default route";
        if (դասիչ==4) return "TCP/UDP sockets and traffic";
        if (դասիչ==5) return "Kernel tasks and user processes";
        if (դասիչ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (դասիչ==7) return "Actual kernel pools and user mappings";
        if (դասիչ==8) return "RAM filesystem capacity and file slots";
        if (դասիչ==9) return "Time since boot";
        if (դասիչ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
