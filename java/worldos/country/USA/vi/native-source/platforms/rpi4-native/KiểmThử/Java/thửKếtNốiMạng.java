// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import tiếngViệt.tựThân.KýTự;
import tiếngViệt.tựThân.TruyềnThông;
public class thửKếtNốiMạng {
    public static void main(String[] args) throws Exception {
        DatagramSocket giáTrịPhíaTrước = TruyềnThông.mở(9431), giáTrịLùi = TruyềnThông.mở(9432);
        try {
            TruyềnThông.gửi(giáTrịPhíaTrước, 9432, "Java UDP 한글😀"); System.out.println(TruyềnThông.nhận(giáTrịLùi));
            byte[] mãNguồn = KýTự.mãHóa("회신"); giáTrịPhíaTrước.send(new DatagramPacket(mãNguồn, mãNguồn.length, InetAddress.getByName("localhost"), 9432));
            byte[] giáTrịĐãNhận = new byte[32]; DatagramPacket điệnDữLiệu = new DatagramPacket(giáTrịĐãNhận, giáTrịĐãNhận.length); giáTrịLùi.receive(điệnDữLiệu);
            System.out.println(điệnDữLiệu.getLength()); System.out.println(điệnDữLiệu.getPort()); System.out.println(điệnDữLiệu.getAddress().getHostAddress());
            System.out.println(giáTrịLùi.getLocalPort());
            giáTrịLùi.setSoTimeout(10);
            try { giáTrịLùi.receive(điệnDữLiệu); } catch (SocketTimeoutException e) { System.out.println("nhậnGiáTrị giáTrịThờiGian 초과"); }
            giáTrịLùi.close();
            try { giáTrịLùi.receive(điệnDữLiệu); } catch (java.io.IOException e) { System.out.println("닫힌 TruyềnThông"); }
        } finally { giáTrịPhíaTrước.close(); giáTrịLùi.close(); }
    }
}
