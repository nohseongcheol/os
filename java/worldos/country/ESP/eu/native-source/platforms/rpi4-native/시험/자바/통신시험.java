// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Euskara.자체.문자;
import Euskara.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket aurrekoa_balio = 통신.Ireki(9431), ATZERA_balio = 통신.Ireki(9432);
        try {
            통신.bidali(aurrekoa_balio, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(ATZERA_balio));
            byte[] ITURBURUA = 문자.부호화("회신"); aurrekoa_balio.send(new DatagramPacket(ITURBURUA, ITURBURUA.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_balio = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_balio, RECEIVED_balio.length); ATZERA_balio.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(ATZERA_balio.getLocalPort());
            ATZERA_balio.setSoTimeout(10);
            try { ATZERA_balio.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 ordua_balio 초과"); }
            ATZERA_balio.close();
            try { ATZERA_balio.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { aurrekoa_balio.close(); ATZERA_balio.close(); }
    }
}
