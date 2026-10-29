// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String 완성어() { return "تنظیم-شبکه نشانی-شبکه آزمون-پژواک مسیرها اتصال‌ها فرایندها فعالیت حافظه ذخیره‌سازی زمان-کار خاموش راهنما"; }
    static String کلمات_متن(int فهرست) {
        if (فهرست==0) return "تنظیم-شبکه";
        if (فهرست==1) return "نشانی-شبکه";
        if (فهرست==2) return "آزمون-پژواک";
        if (فهرست==3) return "مسیرها";
        if (فهرست==4) return "اتصال‌ها";
        if (فهرست==5) return "فرایندها";
        if (فهرست==6) return "فعالیت";
        if (فهرست==7) return "حافظه";
        if (فهرست==8) return "ذخیره‌سازی";
        if (فهرست==9) return "زمان-کار";
        if (فهرست==10) return "خاموش";
        return "راهنما";
    }
    static String 설명(int فهرست) {
        if (فهرست==0) return "IPv4 settings: address, netmask, gateway";
        if (فهرست==1) return "IPv4 interface and route tools";
        if (فهرست==2) return "ICMP echo and round-trip time";
        if (فهرست==3) return "Connected network and default route";
        if (فهرست==4) return "TCP/UDP sockets and traffic";
        if (فهرست==5) return "Kernel tasks and user processes";
        if (فهرست==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (فهرست==7) return "Actual kernel pools and user mappings";
        if (فهرست==8) return "RAM filesystem capacity and file slots";
        if (فهرست==9) return "Time since boot";
        if (فهرست==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
