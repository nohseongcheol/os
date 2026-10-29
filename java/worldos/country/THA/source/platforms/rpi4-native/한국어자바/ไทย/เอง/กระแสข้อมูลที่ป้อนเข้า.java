// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** 입력(入力)과 สตรีม_ค่า: 순서대로 들어오는 바이트를 읽는 ช่อง_รายการ. */
public final class กระแสข้อมูลที่ป้อนเข้า {
    private final java.io.InputStream 표준흐름;
    กระแสข้อมูลที่ป้อนเข้า(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int อ่าน() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return 표준흐름.read();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public int อ่าน(byte[] ข้อมูล) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return 표준흐름.read(ข้อมูล);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public int อ่าน(byte[] ข้อมูล, int เรียกใช้งาน, int 길이) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return 표준흐름.read(ข้อมูล, เรียกใช้งาน, 길이);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void ปิด() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준흐름.close();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
}
