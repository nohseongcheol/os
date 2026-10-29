// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·ຊ່ອງທາງ_ເຂົ້າໃນ(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준종단 = 통신.ສ້າງ(ຫມາຍເລກພອດ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static 전문통로 ສ້າງ(int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new 전문통로(ຫມາຍເລກພອດ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void ສົ່ງ(String ອີເມວ, int ຫມາຍເລກພອດ, String ຂໍ້ມູນ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 통신.ສົ່ງ(표준종단, ອີເມວ, ຫມາຍເລກພອດ, ຂໍ້ມູນ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public String 받기() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void 대기시간(int 밀리초) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public int ຫມາຍເລກພອດ() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void ປິດ() { 통신.ປິດ(표준종단); }
}
