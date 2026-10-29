// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.fosgail(9431), Air_ais_VALUE = 통신.fosgail(9432);
        try {
            통신.cuir(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Air_ais_VALUE));
            byte[] tùs = 문자.부호화("회신"); 앞.send(new DatagramPacket(tùs, tùs.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); Air_ais_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Air_ais_VALUE.getLocalPort());
            Air_ais_VALUE.setSoTimeout(10);
            try { Air_ais_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_VALUE 초과"); }
            Air_ais_VALUE.close();
            try { Air_ais_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); Air_ais_VALUE.close(); }
    }
}
