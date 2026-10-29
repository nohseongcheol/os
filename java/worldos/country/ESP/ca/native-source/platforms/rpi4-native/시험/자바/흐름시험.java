// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket servidor_VALOR = new ServerSocket(9250);
        Socket convidat_VALOR = new Socket("localhost", 9250);
        Socket Connecta = servidor_VALOR.accept();
        if (Connecta.getPort() != convidat_VALOR.getLocalPort() || convidat_VALOR.getPort() != Connecta.getLocalPort()) throw new RuntimeException("port_VALOR 불일치");
        byte[] 전문 = "한글 flux_VALOR".getBytes("UTF-8");
        convidat_VALOR.getOutputStream().write(전문);
        byte[] CANTIDAD_RECIBIDA_element = new byte[100];
        int durada_VALOR = Connecta.getInputStream().read(CANTIDAD_RECIBIDA_element, 0, CANTIDAD_RECIBIDA_element.length);
        System.out.println(durada_VALOR == 전문.length);
        for (int i = 0; i < durada_VALOR; i++) if (CANTIDAD_RECIBIDA_element[i] != 전문[i]) throw new RuntimeException("contingut_VALOR 불일치");
        Connecta.getOutputStream().write(42);
        System.out.println(convidat_VALOR.getInputStream().read());
        convidat_VALOR.close();
        System.out.println(Connecta.getInputStream().read());
        Connecta.close(); servidor_VALOR.close();
        ServerSocket 빈서버 = new ServerSocket(9250);
        빈서버.setSoTimeout(10);
        try { 빈서버.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("Hora_VALOR 제한"); }
        빈서버.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
