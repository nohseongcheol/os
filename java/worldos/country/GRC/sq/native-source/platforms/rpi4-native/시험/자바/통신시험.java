// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket e_përparme_VALUE = 통신.Hap(9431), PAS_VALUE = 통신.Hap(9432);
        try {
            통신.dërgoj(e_përparme_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(PAS_VALUE));
            byte[] BURIMI = 문자.부호화("회신"); e_përparme_VALUE.send(new DatagramPacket(BURIMI, BURIMI.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); PAS_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(PAS_VALUE.getLocalPort());
            PAS_VALUE.setSoTimeout(10);
            try { PAS_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 Ora_VALUE_4692cef5 초과"); }
            PAS_VALUE.close();
            try { PAS_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { e_përparme_VALUE.close(); PAS_VALUE.close(); }
    }
}
