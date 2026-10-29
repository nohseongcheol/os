// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class การทดสอบ_สตรีม {
    public static void main(String[] args) throws Exception {
        ServerSocket เซิร์ฟเวอร์_ค่า = new ServerSocket(9250);
        Socket ผู้เยี่ยมชม_ค่า = new Socket("localhost", 9250);
        Socket เชื่อมต่อ = เซิร์ฟเวอร์_ค่า.accept();
        if (เชื่อมต่อ.getPort() != ผู้เยี่ยมชม_ค่า.getLocalPort() || ผู้เยี่ยมชม_ค่า.getPort() != เชื่อมต่อ.getLocalPort()) throw new RuntimeException("แปลง_ค่า 불일치");
        byte[] เดตาแกรม = "한글 สตรีม_ค่า".getBytes("UTF-8");
        ผู้เยี่ยมชม_ค่า.getOutputStream().write(เดตาแกรม);
        byte[] 받은것 = new byte[100];
        int 길이 = เชื่อมต่อ.getInputStream().read(받은것, 0, 받은것.length);
        System.out.println(길이 == เดตาแกรม.length);
        for (int i = 0; i < 길이; i++) if (받은것[i] != เดตาแกรม[i]) throw new RuntimeException("เนื้อหา_ค่า 불일치");
        เชื่อมต่อ.getOutputStream().write(42);
        System.out.println(ผู้เยี่ยมชม_ค่า.getInputStream().read());
        ผู้เยี่ยมชม_ค่า.close();
        System.out.println(เชื่อมต่อ.getInputStream().read());
        เชื่อมต่อ.close(); เซิร์ฟเวอร์_ค่า.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("ค่าเวลา 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
