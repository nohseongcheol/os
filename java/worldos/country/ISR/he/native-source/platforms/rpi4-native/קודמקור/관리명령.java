// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String הושלם_מילים() { return "הגדרות-רשת כתובת-רשת בדיקת-הד נתיבים חיבורים תהליכים פעילות זיכרון אחסון זמן-פעולה כיבוי עזרה"; }
    static String מילים_טקסט(int מדד) {
        if (מדד==0) return "הגדרות-רשת";
        if (מדד==1) return "כתובת-רשת";
        if (מדד==2) return "בדיקת-הד";
        if (מדד==3) return "נתיבים";
        if (מדד==4) return "חיבורים";
        if (מדד==5) return "תהליכים";
        if (מדד==6) return "פעילות";
        if (מדד==7) return "זיכרון";
        if (מדד==8) return "אחסון";
        if (מדד==9) return "זמן-פעולה";
        if (מדד==10) return "כיבוי";
        return "עזרה";
    }
    static String 설명(int מדד) {
        if (מדד==0) return "IPv4 settings: address, netmask, gateway";
        if (מדד==1) return "IPv4 interface and route tools";
        if (מדד==2) return "ICMP echo and round-trip time";
        if (מדד==3) return "Connected network and default route";
        if (מדד==4) return "TCP/UDP sockets and traffic";
        if (מדד==5) return "Kernel tasks and user processes";
        if (מדד==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (מדד==7) return "Actual kernel pools and user mappings";
        if (מדד==8) return "RAM filesystem capacity and file slots";
        if (מדד==9) return "Time since boot";
        if (מדד==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
