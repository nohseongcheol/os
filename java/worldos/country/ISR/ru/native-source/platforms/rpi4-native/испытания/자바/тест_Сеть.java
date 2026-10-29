// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import русский.свой.문자;
import русский.свой.коммуникация;
public class тест_Сеть {
    public static void main(String[] args) throws Exception {
        DatagramSocket лицевая_камера_ЗНАЧЕН = коммуникация.Открыть(9431), BACK_ЗНАЧЕН = коммуникация.Открыть(9432);
        try {
            коммуникация.написать(лицевая_камера_ЗНАЧЕН, 9432, "자바 UDP 한글😀"); System.out.println(коммуникация.получить(BACK_ЗНАЧЕН));
            byte[] исходныйКод = 문자.кодировать("회신"); лицевая_камера_ЗНАЧЕН.send(new DatagramPacket(исходныйКод, исходныйКод.length, InetAddress.getByName("localhost"), 9432));
            byte[] ПОЛУЧЕНО_ЗНАЧЕН = new byte[32]; DatagramPacket датаграмма = new DatagramPacket(ПОЛУЧЕНО_ЗНАЧЕН, ПОЛУЧЕНО_ЗНАЧЕН.length); BACK_ЗНАЧЕН.receive(датаграмма);
            System.out.println(датаграмма.getLength()); System.out.println(датаграмма.getPort()); System.out.println(датаграмма.getAddress().getHostAddress());
            System.out.println(BACK_ЗНАЧЕН.getLocalPort());
            BACK_ЗНАЧЕН.setSoTimeout(10);
            try { BACK_ЗНАЧЕН.receive(датаграмма); } catch (SocketTimeoutException e) { System.out.println("получить_ЗНАЧЕН значение_времени 초과"); }
            BACK_ЗНАЧЕН.close();
            try { BACK_ЗНАЧЕН.receive(датаграмма); } catch (java.io.IOException e) { System.out.println("닫힌 коммуникация"); }
        } finally { лицевая_камера_ЗНАЧЕН.close(); BACK_ЗНАЧЕН.close(); }
    }
}
