// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket old_kamera_VALUE = 통신.Ochish(9431), Orqaga_VALUE = 통신.Ochish(9432);
        try {
            통신.yuborish(old_kamera_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Orqaga_VALUE));
            byte[] manba = 문자.부호화("회신"); old_kamera_VALUE.send(new DatagramPacket(manba, manba.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); Orqaga_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Orqaga_VALUE.getLocalPort());
            Orqaga_VALUE.setSoTimeout(10);
            try { Orqaga_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_VALUE 초과"); }
            Orqaga_VALUE.close();
            try { Orqaga_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { old_kamera_VALUE.close(); Orqaga_VALUE.close(); }
    }
}
