// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import українська.своє.문자;
import українська.своє.통신;
public class 통신시험 {
    public static void main(String[] args) throws Exception {
        DatagramSocket фронтальна_камера_значення = 통신.Відкрити(9431), НАЗАД_значення = 통신.Відкрити(9432);
        try {
            통신.надсилати(фронтальна_камера_значення, 9432, "자바 UDP 한글😀"); System.out.println(통신.отримувати(НАЗАД_значення));
            byte[] вихіднийКод = 문자.кодувати("회신"); фронтальна_камера_значення.send(new DatagramPacket(вихіднийКод, вихіднийКод.length, InetAddress.getByName("localhost"), 9432));
            byte[] 받은값 = new byte[32]; DatagramPacket дейтаграма = new DatagramPacket(받은값, 받은값.length); НАЗАД_значення.receive(дейтаграма);
            System.out.println(дейтаграма.getLength()); System.out.println(дейтаграма.getPort()); System.out.println(дейтаграма.getAddress().getHostAddress());
            System.out.println(НАЗАД_значення.getLocalPort());
            НАЗАД_значення.setSoTimeout(10);
            try { НАЗАД_значення.receive(дейтаграма); } catch (SocketTimeoutException e) { System.out.println("отримувати_значення_cef4d8ab час_значення 초과"); }
            НАЗАД_значення.close();
            try { НАЗАД_значення.receive(дейтаграма); } catch (java.io.IOException e) { System.out.println("닫힌 통신"); }
        } finally { фронтальна_камера_значення.close(); НАЗАД_значення.close(); }
    }
}
