// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** ເຊື່ອມຕໍ່(連結)·ຊ່ອງທາງ_ເຂົ້າໃນ(通路): 상대와 이어진 TCP ໄບ_ຄ່າ 흐름의 종단. */
public final class ການເຊື່ອມຕໍ່ {
    private final java.net.Socket 표준연결;
    ການເຊື່ອມຕໍ່(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ການເຊື່ອມຕໍ່ ສ້າງ(String ອີເມວ, int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try {
            return new ການເຊື່ອມຕໍ່(new java.net.Socket(ອີເມວ, ຫມາຍເລກພອດ));
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public 입력흐름 입력() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public 출력흐름 출력() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public void 대기시간(int 밀리초) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public int ຫມາຍເລກພອດ() { return 표준연결.getPort(); }
    public int ໃນເຄື່ອງ_ຫມາຍເລກພອດ() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void ປິດ() throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 표준연결.close();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
}
