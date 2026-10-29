// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import ไทย.เอง.문자;
import ไทย.เอง.통신;
public class การทดสอบ_ระบบเครือข่าย {
    public static void main(String[] args) throws Exception {
        DatagramSocket กล้องหน้า_ค่า = 통신.เปิด(9431), ย้อนกลับ_ค่า = 통신.เปิด(9432);
        try {
            통신.ส่ง(กล้องหน้า_ค่า, 9432, "자바 UDP 한글😀"); System.out.println(통신.รับ(ย้อนกลับ_ค่า));
            byte[] รหัสต้นฉบับ = 문자.เข้ารหัส("회신"); กล้องหน้า_ค่า.send(new DatagramPacket(รหัสต้นฉบับ, รหัสต้นฉบับ.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket เดตาแกรม = new DatagramPacket(받은값, 받은값.length); ย้อนกลับ_ค่า.receive(เดตาแกรม);
            System.out.println(เดตาแกรม.getLength()); System.out.println(เดตาแกรม.getPort()); System.out.println(เดตาแกรม.getAddress().getHostAddress());
            System.out.println(ย้อนกลับ_ค่า.getLocalPort());
            ย้อนกลับ_ค่า.setSoTimeout(10);
            try { ย้อนกลับ_ค่า.receive(เดตาแกรม); } catch (SocketTimeoutException e) { System.out.println("รับ_ค่า ค่าเวลา 초과"); }
            ย้อนกลับ_ค่า.close();
            try { ย้อนกลับ_ค่า.receive(เดตาแกรม); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { กล้องหน้า_ค่า.close(); ย้อนกลับ_ค่า.close(); }
    }
}
