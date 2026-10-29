// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class тест_поток {
    public static void main(String[] args) throws Exception {
        ServerSocket сервер_ЗНАЧЕН = new ServerSocket(9250);
        Socket гость_ЗНАЧЕН = new Socket("localhost", 9250);
        Socket Подключить = сервер_ЗНАЧЕН.accept();
        if (Подключить.getPort() != гость_ЗНАЧЕН.getLocalPort() || гость_ЗНАЧЕН.getPort() != Подключить.getLocalPort()) throw new RuntimeException("порт_ЗНАЧЕН 불일치");
        byte[] датаграмма = "한글 поток_ЗНАЧЕН".getBytes("UTF-8");
        гость_ЗНАЧЕН.getOutputStream().write(датаграмма);
        byte[] ПОЛУЧЕНО_товар = new byte[100];
        int длина_ЗНАЧЕН = Подключить.getInputStream().read(ПОЛУЧЕНО_товар, 0, ПОЛУЧЕНО_товар.length);
        System.out.println(длина_ЗНАЧЕН == датаграмма.length);
        for (int i = 0; i < длина_ЗНАЧЕН; i++) if (ПОЛУЧЕНО_товар[i] != датаграмма[i]) throw new RuntimeException("контент_ЗНАЧЕН 불일치");
        Подключить.getOutputStream().write(42);
        System.out.println(гость_ЗНАЧЕН.getInputStream().read());
        гость_ЗНАЧЕН.close();
        System.out.println(Подключить.getInputStream().read());
        Подключить.close(); сервер_ЗНАЧЕН.close();
        ServerSocket пустой_сервер = new ServerSocket(9250);
        пустой_сервер.setSoTimeout(10);
        try { пустой_сервер.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("значение_времени 제한"); }
        пустой_сервер.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
