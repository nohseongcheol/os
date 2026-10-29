// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Melayu.Asli.문자;
import Melayu.Asli.통신;
public class ujian_Rangkaian {
    public static void main(String[] args) throws Exception {
        DatagramSocket hadapan_VALUE = 통신.Buka(9431), BACK_VALUE = 통신.Buka(9432);
        try {
            통신.e_mel_9aee63bd(hadapan_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(BACK_VALUE));
            byte[] SUMBER = 문자.부호화("회신"); hadapan_VALUE.send(new DatagramPacket(SUMBER, SUMBER.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); BACK_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(BACK_VALUE.getLocalPort());
            BACK_VALUE.setSoTimeout(10);
            try { BACK_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 nilai_masa 초과"); }
            BACK_VALUE.close();
            try { BACK_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { hadapan_VALUE.close(); BACK_VALUE.close(); }
    }
}
