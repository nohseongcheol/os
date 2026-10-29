// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ການເຊື່ອມຕໍ່ ສ້າງ(String ອີເມວ, int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return ການເຊື່ອມຕໍ່.ສ້າງ(ອີເມວ, ຫມາຍເລກພອດ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static 수신창구 수신열기(int ຫມາຍເລກພອດ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 수신창구.ສ້າງ(ຫມາຍເລກພອດ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static Socket ເຊື່ອມຕໍ່(String ອີເມວ, int ຜອດ_ຄ່າ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new Socket(ອີເມວ, ຜອດ_ຄ່າ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static ServerSocket 듣기(int ຜອດ_ຄ່າ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new ServerSocket(ຜອດ_ຄ່າ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static Socket 받기(ServerSocket 서버) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return 서버.accept();
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
}
