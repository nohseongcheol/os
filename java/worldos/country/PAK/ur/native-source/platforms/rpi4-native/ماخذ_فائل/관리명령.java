// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "نیٹ-ترتیب نیٹ-پتا جواب-آزمائش راستے رابطے عمل سرگرمی حافظہ ذخیرہ چلنے-کا-وقت بند-کریں مدد"; }
    static String الفاظ_متن(int اشاریہ) {
        if (اشاریہ==0) return "نیٹ-ترتیب";
        if (اشاریہ==1) return "نیٹ-پتا";
        if (اشاریہ==2) return "جواب-آزمائش";
        if (اشاریہ==3) return "راستے";
        if (اشاریہ==4) return "رابطے";
        if (اشاریہ==5) return "عمل";
        if (اشاریہ==6) return "سرگرمی";
        if (اشاریہ==7) return "حافظہ";
        if (اشاریہ==8) return "ذخیرہ";
        if (اشاریہ==9) return "چلنے-کا-وقت";
        if (اشاریہ==10) return "بند-کریں";
        return "مدد";
    }
    static String 설명(int اشاریہ) {
        if (اشاریہ==0) return "IPv4 settings: address, netmask, gateway";
        if (اشاریہ==1) return "IPv4 interface and route tools";
        if (اشاریہ==2) return "ICMP echo and round-trip time";
        if (اشاریہ==3) return "Connected network and default route";
        if (اشاریہ==4) return "TCP/UDP sockets and traffic";
        if (اشاریہ==5) return "Kernel tasks and user processes";
        if (اشاریہ==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (اشاریہ==7) return "Actual kernel pools and user mappings";
        if (اشاریہ==8) return "RAM filesystem capacity and file slots";
        if (اشاریہ==9) return "Time since boot";
        if (اشاریہ==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
