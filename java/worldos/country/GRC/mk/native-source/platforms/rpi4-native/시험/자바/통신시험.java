// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Македонски.자체.문자;
import Македонски.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket предна_VALUE = 통신.Отвори(9431), Назад_VALUE = 통신.Отвори(9432);
        try {
            통신.испрати(предна_VALUE, 9432, "자바 UDP 한글😀"); System.out.println(통신.받기(Назад_VALUE));
            byte[] ИЗВОР = 문자.부호화("회신"); предна_VALUE.send(new DatagramPacket(ИЗВОР, ИЗВОР.length, InetAddress.getByName("localhost"), 9432));
            byte[] RECEIVED_VALUE = new byte[32]; DatagramPacket 전문 = new DatagramPacket(RECEIVED_VALUE, RECEIVED_VALUE.length); Назад_VALUE.receive(전문);
            System.out.println(전문.getLength()); System.out.println(전문.getPort()); System.out.println(전문.getAddress().getHostAddress());
            System.out.println(Назад_VALUE.getLocalPort());
            Назад_VALUE.setSoTimeout(10);
            try { Назад_VALUE.receive(전문); } catch (SocketTimeoutException e) { System.out.println("수신 TIME_VALUE 초과"); }
            Назад_VALUE.close();
            try { Назад_VALUE.receive(전문); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { предна_VALUE.close(); Назад_VALUE.close(); }
    }
}
