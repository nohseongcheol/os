// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "igenamiterere-ip aderesi-ip igerageza-igisubizo inzira amasano ibikorwa imikorere ububiko-bwibuka ububiko igihe-cyakazi zimya ubufasha"; }
    static String Ijambo_SMS(int umugerekashakiro) {
        if (umugerekashakiro==0) return "igenamiterere-ip";
        if (umugerekashakiro==1) return "aderesi-ip";
        if (umugerekashakiro==2) return "igerageza-igisubizo";
        if (umugerekashakiro==3) return "inzira";
        if (umugerekashakiro==4) return "amasano";
        if (umugerekashakiro==5) return "ibikorwa";
        if (umugerekashakiro==6) return "imikorere";
        if (umugerekashakiro==7) return "ububiko-bwibuka";
        if (umugerekashakiro==8) return "ububiko";
        if (umugerekashakiro==9) return "igihe-cyakazi";
        if (umugerekashakiro==10) return "zimya";
        return "ubufasha";
    }
    static String 설명(int umugerekashakiro) {
        if (umugerekashakiro==0) return "IPv4 settings: address, netmask, gateway";
        if (umugerekashakiro==1) return "IPv4 interface and route tools";
        if (umugerekashakiro==2) return "ICMP echo and round-trip time";
        if (umugerekashakiro==3) return "Connected network and default route";
        if (umugerekashakiro==4) return "TCP/UDP sockets and traffic";
        if (umugerekashakiro==5) return "Kernel tasks and user processes";
        if (umugerekashakiro==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (umugerekashakiro==7) return "Actual kernel pools and user mappings";
        if (umugerekashakiro==8) return "RAM filesystem capacity and file slots";
        if (umugerekashakiro==9) return "Time since boot";
        if (umugerekashakiro==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
