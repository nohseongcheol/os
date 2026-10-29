// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ไทย.เอง;
import java.net.*;
public final class เพื่อน_การโอนถ่ายข้อมูล {
    private เพื่อน_การโอนถ่ายข้อมูล() {}
    public static เพื่อน เปิด(String อีเมล, int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return เพื่อน.เปิด(อีเมล, หมายเลขพอร์ต);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static รับ_แปลง 수신열기(int หมายเลขพอร์ต) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return รับ_แปลง.เปิด(หมายเลขพอร์ต);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static Socket เชื่อมต่อ(String อีเมล, int แปลง_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new Socket(อีเมล, แปลง_ค่า);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static ServerSocket รอการติดต่อ_ปลายทาง(int แปลง_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return new ServerSocket(แปลง_ค่า);
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
    public static Socket รับ(ServerSocket เซิร์ฟเวอร์_ค่า) throws รับเข้า_ส่งออก_ข้อยกเว้น {
        try { return เซิร์ฟเวอร์_ค่า.accept();
        } catch (java.io.IOException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.รับเข้า_ส่งออก(ข้อผิดพลาด); }
        catch (RuntimeException ข้อผิดพลาด) { throw แปลง_ข้อยกเว้น.ดําเนินการ_คําสั่ง(ข้อผิดพลาด); }
    }
}
