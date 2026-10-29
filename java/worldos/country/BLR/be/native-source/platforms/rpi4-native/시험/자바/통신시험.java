// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import 한국어.자체.문자;
import 한국어.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket пярэдняя_камера_значэнне = 통신.Адкрыць(9431), Назад_значэнне = 통신.Адкрыць(9432);
        try {
            통신.адправіць(пярэдняя_камера_значэнне, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Назад_значэнне));
            byte[] КРЫНІЦА = 문자.부호화("회신"); пярэдняя_камера_значэнне.send(new DatagramPacket(КРЫНІЦА, КРЫНІЦА.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket 전문 = new DatagramPacket(받은값, 받은값.length); Назад_значэнне.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Назад_значэнне.getLocalPort());
            Назад_значэнне.setSoTimeout(10);
            try { Назад_значэнне.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 час_значэнне 초과"); }
            Назад_значэнне.close();
            try { Назад_значэнне.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { пярэдняя_камера_значэнне.close(); Назад_значэнне.close(); }
    }
}
