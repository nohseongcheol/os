// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Indonesia.Asli.문자;
import Indonesia.Asli.komunikasi;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket depan_VALUE = komunikasi.Buka(9431), BACK_VALUE = komunikasi.Buka(9432);
        try {
            komunikasi.kirim(depan_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(komunikasi.terima(BACK_VALUE));
            byte[] kodeSumber = 문자.부호화("회신"); depan_VALUE.send(new DatagramPacket(kodeSumber, kodeSumber.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); BACK_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(BACK_VALUE.getLocalPort());
            BACK_VALUE.setSoTimeout(10);
            try { BACK_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("terima_VALUE TIME_VALUE 초과"); }
            BACK_VALUE.close();
            try { BACK_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 komunikasi"); }
        } finally { depan_VALUE.close(); BACK_VALUE.close(); }
    }
}
