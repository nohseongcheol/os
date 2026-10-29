// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** รับ_ค่า(受信)·แปลง_ค่า(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class รับ_แปลง {
    private final java.net.ServerSocket 표준창구;
    private รับ_แปลง(int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준창구 = new java.net.ServerSocket(หมายเลขพอร์ต);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static รับ_แปลง เปิด(int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new รับ_แปลง(หมายเลขพอร์ต);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public เพื่อน รับ() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new เพื่อน(표준창구.accept());
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public int หมายเลขพอร์ต() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public boolean เทคโนโลยีสารสนเทศ_ปิด() { return 표준창구.isClosed(); }
    public void ปิด() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준창구.close();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
}
