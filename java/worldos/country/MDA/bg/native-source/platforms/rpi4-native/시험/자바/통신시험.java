// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import Български.자체.문자;
import Български.자체.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket предна_стойност = 통신.Отваряне(9431), НАЗАД_стойност = 통신.Отваряне(9432);
        try {
            통신.изпращам(предна_стойност, 9432, "자바 UDP 한글😀"); System.out.println(통신.получавам(НАЗАД_стойност));
            byte[] ИЗТОЧНИК = 문자.кодирам("회신"); предна_стойност.send(new DatagramPacket(ИЗТОЧНИК, ИЗТОЧНИК.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket дейтаграма = new DatagramPacket(받은값, 받은값.length); НАЗАД_стойност.receive(дейтаграма);
            System.out.println(дейтаграма.getLength()); System.out.println(дейтаграма.getPort()); System.out.println(дейтаграма.getAddress().getHostAddress());
            System.out.println(НАЗАД_стойност.getLocalPort());
            НАЗАД_стойност.setSoTimeout(10);
            try { НАЗАД_стойност.receive(дейтаграма); } catch (SocketTimeoutException e) { System.out.println("получавам_стойност_cef4d8ab час_стойност 초과"); }
            НАЗАД_стойност.close();
            try { НАЗАД_стойност.receive(дейтаграма); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { предна_стойност.close(); НАЗАД_стойност.close(); }
    }
}
