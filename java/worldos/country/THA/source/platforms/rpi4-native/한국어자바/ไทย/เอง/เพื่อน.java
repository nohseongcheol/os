// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;

/** เชื่อมต่อ(連結)·ช่อง_รายการ(通路): 상대와 이어진 TCP ไบต์_ค่า 흐름의 ปลายทาง. */
public final class เพื่อน {
    private final java.net.Socket 표준연결;
    เพื่อน(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static เพื่อน เปิด(String อีเมล, int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try {
            return new เพื่อน(new java.net.Socket(อีเมล, หมายเลขพอร์ต));
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public กระแสข้อมูลที่ป้อนเข้า 입력() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new กระแสข้อมูลที่ป้อนเข้า(표준연결.getInputStream());
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public กระแสข้อมูลขาออก ข้อความออก() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new กระแสข้อมูลขาออก(표준연결.getOutputStream());
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public void 대기시간(int 밀리초) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public int หมายเลขพอร์ต() { return 표준연결.getPort(); }
    public int ท้องถิ่น_หมายเลขพอร์ต() { return 표준연결.getLocalPort(); }
    public boolean เทคโนโลยีสารสนเทศ_ปิด() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void ปิด() throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { 표준연결.close();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
}
