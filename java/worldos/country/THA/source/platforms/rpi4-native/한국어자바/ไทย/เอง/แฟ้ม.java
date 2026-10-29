// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ผู้ใช้ 용어를 보존한다. ปัจจุบัน_รายการ 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class แฟ้ม {
    private แฟ้ม() {}
    public static byte[] 바이트읽기(String ชื่อ) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try {
        FileInputStream สตรีม_ค่า = new FileInputStream(ชื่อ);
        try {
            byte[] 임시 = new byte[16384]; int หมายเลข = 0, ค่า;
            while ((ค่า = สตรีม_ค่า.read()) != -1) { if (หมายเลข == 임시.length) throw new รับเข้า_ส่งออก_ข้อยกเว้น("แฟ้ม ขนาด 제한"); 임시[หมายเลข++] = (byte)ค่า; }
            byte[] ผลลัพธ์ = new byte[หมายเลข]; System.arraycopy(임시, 0, ผลลัพธ์, 0, หมายเลข); return ผลลัพธ์;
        } finally { สตรีม_ค่า.close(); }
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static void 바이트쓰기(String ชื่อ, byte[] เนื้อหา_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try {
        FileOutputStream สตรีม_ค่า = new FileOutputStream(ชื่อ);
        try { for (int วน_ดัชนี = 0; วน_ดัชนี < เนื้อหา_ค่า.length; วน_ดัชนี++) สตรีม_ค่า.write(เนื้อหา_ค่า[วน_ดัชนี] & 255); } finally { สตรีม_ค่า.close(); }
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static String อ่าน(String ชื่อ) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return 문자.ถอดรหัสลับ_ข้อมูล(바이트읽기(ชื่อ));
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static void เขียน(String ชื่อ, String เนื้อหา_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 바이트쓰기(ชื่อ, 문자.เข้ารหัส(เนื้อหา_ค่า));
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
}
