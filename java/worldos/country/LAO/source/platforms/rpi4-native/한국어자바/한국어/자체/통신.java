// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ຕົວເລກ_ຄ່າ 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ສ້າງ(int ຜອດ_ຄ່າ) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { return new DatagramSocket(ຜອດ_ຄ່າ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static void ສົ່ງ(DatagramSocket 종단, int ຜອດ_ຄ່າ, String ເນື້ອໃນ_ຄ່າ_cb0f2404) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try {
        ສົ່ງ(종단, "127.0.0.1", ຜອດ_ຄ່າ, ເນື້ອໃນ_ຄ່າ_cb0f2404);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static void ສົ່ງ(DatagramSocket 종단, String ອີເມວ, int ຜອດ_ຄ່າ, String ເນື້ອໃນ_ຄ່າ_cb0f2404) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try {
        byte[] ໄບ_ຄ່າ = 문자.부호화(ເນື້ອໃນ_ຄ່າ_cb0f2404);
        종단.send(new DatagramPacket(ໄບ_ຄ່າ, ໄບ_ຄ່າ.length, InetAddress.getByName(ອີເມວ), ຜອດ_ຄ່າ));
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static String 받기(DatagramSocket 종단) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try {
        byte[] ໄບ_ຄ່າ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ໄບ_ຄ່າ, ໄບ_ຄ່າ.length); 종단.receive(전문);
        byte[] ມາດຕະການ = new byte[전문.getLength()]; System.arraycopy(ໄບ_ຄ່າ, 0, ມາດຕະການ, 0, ມາດຕະການ.length); return 문자.ຖອດລະຫັດ_ຂໍ້ມູນ(ມາດຕະການ);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws ໄອ_ໂອ_ຂໍ້ຍົກເວັ້ນ {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ຂໍ້ຜິດພາດ) { throw 예외변환.ໄອ_ໂອ(ຂໍ້ຜິດພາດ); }
        catch (RuntimeException ຂໍ້ຜິດພາດ) { throw 예외변환.ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ຂໍ້ຜິດພາດ); }
    }
    public static void ປິດ(DatagramSocket 종단) { 종단.close(); }
}
