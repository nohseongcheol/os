// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** เดตาแกรม(電文)·ช่อง_รายการ(通路): 경계를 가진 UDP 자료를 주고받는 ปลายทาง. */
public final class เดตาแกรม_ช่อง {
    private final java.net.DatagramSocket 표준종단;
    private เดตาแกรม_ช่อง(int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준종단 = 통신.เปิด(หมายเลขพอร์ต);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static เดตาแกรม_ช่อง เปิด(int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new เดตาแกรม_ช่อง(หมายเลขพอร์ต);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void ส่ง(String อีเมล, int หมายเลขพอร์ต, String ข้อมูล) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 통신.ส่ง(표준종단, อีเมล, หมายเลขพอร์ต, ข้อมูล);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public String รับ() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return 통신.รับ(표준종단);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void 대기시간(int 밀리초) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public int หมายเลขพอร์ต() { return 표준종단.getLocalPort(); }
    public boolean เทคโนโลยีสารสนเทศ_ปิด() { return 표준종단.isClosed(); }
    public void ปิด() { 통신.ปิด(표준종단); }
}
