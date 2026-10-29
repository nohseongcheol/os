// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 관리명령 {
    static String เสร็จสมบูรณ์_คํา() { return "ตั้งค่าไอพี ที่อยู่ไอพี ทดสอบตอบกลับ เส้นทาง การเชื่อมต่อ กระบวนการ สถานะงาน หน่วยความจำ พื้นที่เก็บข้อมูล เวลาทำงาน ปิดเครื่อง ช่วยเหลือ"; }
    static String คํา_ข้อความ(int ดัชนี) {
        if (ดัชนี==0) return "ตั้งค่าไอพี";
        if (ดัชนี==1) return "ที่อยู่ไอพี";
        if (ดัชนี==2) return "ทดสอบตอบกลับ";
        if (ดัชนี==3) return "เส้นทาง";
        if (ดัชนี==4) return "การเชื่อมต่อ";
        if (ดัชนี==5) return "กระบวนการ";
        if (ดัชนี==6) return "สถานะงาน";
        if (ดัชนี==7) return "หน่วยความจำ";
        if (ดัชนี==8) return "พื้นที่เก็บข้อมูล";
        if (ดัชนี==9) return "เวลาทำงาน";
        if (ดัชนี==10) return "ปิดเครื่อง";
        return "ช่วยเหลือ";
    }
    static String 설명(int ดัชนี) {
        if (ดัชนี==0) return "IPv4 settings: address, netmask, gateway";
        if (ดัชนี==1) return "IPv4 interface and route tools";
        if (ดัชนี==2) return "ICMP echo and round-trip time";
        if (ดัชนี==3) return "Connected network and default route";
        if (ดัชนี==4) return "TCP/UDP sockets and traffic";
        if (ดัชนี==5) return "Kernel tasks and user processes";
        if (ดัชนี==6) return "Refresh tasks and memory; q or Ctrl+C quits";
        if (ดัชนี==7) return "Actual kernel pools and user mappings";
        if (ดัชนี==8) return "RAM filesystem capacity and file slots";
        if (ดัชนี==9) return "Time since boot";
        if (ดัชนี==10) return "Stop the OS; RAM files are not preserved";
        return "Commands and local names";
    }
}
