// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String مكتمل_الكلمات() { return "إعداد-الشبكة عنوان-الشبكة اختبار-الصدى المسارات الاتصالات العمليات مراقبة-النشاط الذاكرة التخزين مدة-التشغيل إيقاف-التشغيل مساعدة"; }
    static String الكلمات_نص(int فهرس) {
        if (فهرس==0) return "إعداد-الشبكة";
        if (فهرس==1) return "عنوان-الشبكة";
        if (فهرس==2) return "اختبار-الصدى";
        if (فهرس==3) return "المسارات";
        if (فهرس==4) return "الاتصالات";
        if (فهرس==5) return "العمليات";
        if (فهرس==6) return "مراقبة-النشاط";
        if (فهرس==7) return "الذاكرة";
        if (فهرس==8) return "التخزين";
        if (فهرس==9) return "مدة-التشغيل";
        if (فهرس==10) return "إيقاف-التشغيل";
        return "مساعدة";
    }
    static String 설명(int فهرس) {
        if (فهرس==0) return "IPv4 settings: address, netmask, gateway";
        if (فهرس==1) return "IPv4 interface and route tools";
        if (فهرس==2) return "ICMP echo and round-trip time";
        if (فهرس==3) return "Connected network and default route";
        if (فهرس==4) return "TCP/UDP sockets and traffic";
        if (فهرس==5) return "Kernel tasks and user processes";
        if (فهرس==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (فهرس==7) return "Actual kernel pools and user mappings";
        if (فهرس==8) return "RAM filesystem capacity and file slots";
        if (فهرس==9) return "Time since boot";
        if (فهرس==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
