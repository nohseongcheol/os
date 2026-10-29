// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP เดตาแกรม. ภายนอก_ค่า 주소는 ตัวเลข_ค่า 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket เปิด(int แปลง_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new DatagramSocket(แปลง_ค่า);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static void ส่ง(DatagramSocket ปลายทาง, int แปลง_ค่า, String เนื้อหา_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try {
        ส่ง(ปลายทาง, "127.0.0.1", แปลง_ค่า, เนื้อหา_ค่า);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static void ส่ง(DatagramSocket ปลายทาง, String อีเมล, int แปลง_ค่า, String เนื้อหา_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try {
        byte[] ไบต์_ค่า = 문자.เข้ารหัส(เนื้อหา_ค่า);
        ปลายทาง.send(new DatagramPacket(ไบต์_ค่า, ไบต์_ค่า.length, InetAddress.getByName(อีเมล), แปลง_ค่า));
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static String รับ(DatagramSocket ปลายทาง) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try {
        byte[] ไบต์_ค่า = new byte[512]; DatagramPacket เดตาแกรม = new DatagramPacket(ไบต์_ค่า, ไบต์_ค่า.length); ปลายทาง.receive(เดตาแกรม);
        byte[] ผลลัพธ์ = new byte[เดตาแกรม.getLength()]; System.arraycopy(ไบต์_ค่า, 0, ผลลัพธ์, 0, ผลลัพธ์.length); return 문자.ถอดรหัสลับ_ข้อมูล(ผลลัพธ์);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static void 대기시간(DatagramSocket ปลายทาง, int 밀리초) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { ปลายทาง.setSoTimeout(밀리초);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static void ปิด(DatagramSocket ปลายทาง) { ปลายทาง.close(); }
}
