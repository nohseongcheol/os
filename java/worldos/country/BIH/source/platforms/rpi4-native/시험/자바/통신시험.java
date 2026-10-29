// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket 앞 = 통신.отворити(9431), Назад_вриједност = 통신.отворити(9432);
        try {
            통신.послати(앞, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Назад_вриједност));
            byte[] извор = 문자.부호화("회신"); 앞.send(new DatagramPacket(извор, извор.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); Назад_вриједност.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Назад_вриједност.getLocalPort());
            Назад_вриједност.setSoTimeout(10);
            try { Назад_вриједност.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 시간 초과"); }
            Назад_вриједност.close();
            try { Назад_вриједност.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { 앞.close(); Назад_вриједност.close(); }
    }
}
