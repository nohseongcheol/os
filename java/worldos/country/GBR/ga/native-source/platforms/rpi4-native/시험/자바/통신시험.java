// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Gaeilge.자체.문자;
import Gaeilge.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.Oscail(9431), Siar_VALUE = 통신.Oscail(9432);
        try {
            통신.seol(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Siar_VALUE));
            byte[] FOINSE = 문자.부호화("회신"); 앞.send(new DatagramPacket(FOINSE, FOINSE.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); Siar_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Siar_VALUE.getLocalPort());
            Siar_VALUE.setSoTimeout(10);
            try { Siar_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_VALUE 초과"); }
            Siar_VALUE.close();
            try { Siar_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); Siar_VALUE.close(); }
    }
}
