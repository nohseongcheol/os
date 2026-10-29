// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** ข้อความออก(出力)과 สตรีม_ค่า: 순서를 보존해 내보내는 바이트의 ช่อง_รายการ. */
public final class กระแสข้อมูลขาออก {
    private final java.io.OutputStream 표준흐름;
    กระแสข้อมูลขาออก(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void เขียน(int ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준흐름.write(ค่า);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void เขียน(byte[] ข้อมูล) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준흐름.write(ข้อมูล);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void เขียน(byte[] ข้อมูล, int เรียกใช้งาน, int 길이) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준흐름.write(ข้อมูล, เรียกใช้งาน, 길이);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void 내보내기() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준흐름.flush();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void ปิด() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준흐름.close();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
}
