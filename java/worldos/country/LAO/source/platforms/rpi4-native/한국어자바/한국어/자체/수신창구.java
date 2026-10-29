// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·ຜອດ_ຄ່າ(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준창구 = new java.net.ServerSocket(ຫມາຍເລກພອດ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static 수신창구 ສ້າງ(int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new 수신창구(ຫມາຍເລກພອດ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public ການເຊື່ອມຕໍ່ 받기() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new ການເຊື່ອມຕໍ່(표준창구.accept());
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public int ຫມາຍເລກພອດ() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void ປິດ() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준창구.close();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
}
