// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket ön_VALUE = 통신.Aç(9431), GERİ_VALUE = 통신.Aç(9432);
        try {
            통신.göndərmək(ön_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(GERİ_VALUE));
            byte[] QAYNAQ = 문자.부호화("회신"); ön_VALUE.send(new DatagramPacket(QAYNAQ, QAYNAQ.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); GERİ_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(GERİ_VALUE.getLocalPort());
            GERİ_VALUE.setSoTimeout(10);
            try { GERİ_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_VALUE 초과"); }
            GERİ_VALUE.close();
            try { GERİ_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { ön_VALUE.close(); GERİ_VALUE.close(); }
    }
}
