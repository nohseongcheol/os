// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class 흐름시험 {
    public static void main(String[] args) throws Exception {
        ServerSocket servidor_VALOR = new ServerSocket(9250);
        Socket convidado_VALOR = new Socket("localhost", 9250);
        Socket Conectar = servidor_VALOR.accept();
        if (Conectar.getPort() != convidado_VALOR.getLocalPort() || convidado_VALOR.getPort() != Conectar.getLocalPort()) throw new RuntimeException("porto_VALOR 불일치");
        byte[] 전문 = "한글 fluxo_VALOR".getBytes("UTF-8");
        convidado_VALOR.getOutputStream().write(전문);
        byte[] RECIBIDO_elemento = new byte[100];
        int duración_VALOR = Conectar.getInputStream().read(RECIBIDO_elemento, 0, RECIBIDO_elemento.length);
        System.out.println(duración_VALOR == 전문.length);
        for (int i = 0; i < duración_VALOR; i++) if (RECIBIDO_elemento[i] != 전문[i]) throw new RuntimeException("Contido_VALOR 불일치");
        Conectar.getOutputStream().write(42);
        System.out.println(convidado_VALOR.getInputStream().read());
        convidado_VALOR.close();
        System.out.println(Conectar.getInputStream().read());
        Conectar.close(); servidor_VALOR.close();
        ServerSocket baleiro_servidor = new ServerSocket(9250);
        baleiro_servidor.setSoTimeout(10);
        try { baleiro_servidor.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("hora_VALOR 제한"); }
        baleiro_servidor.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
