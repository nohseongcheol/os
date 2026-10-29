// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.net.*;
import java.io.*;
public class teste_fluxo {
    public static void main(String[] args) throws Exception {
        ServerSocket servidor_VALOR = new ServerSocket(9250);
        Socket convidado_VALOR = new Socket("localhost", 9250);
        Socket Ligar = servidor_VALOR.accept();
        if (Ligar.getPort() != convidado_VALOR.getLocalPort() || convidado_VALOR.getPort() != Ligar.getLocalPort()) throw new RuntimeException("porta_VALOR 불일치");
        byte[] datagrama = "한글 fluxo_VALOR".getBytes("UTF-8");
        convidado_VALOR.getOutputStream().write(datagrama);
        byte[] RECEBER_item = new byte[100];
        int duração_VALOR = Ligar.getInputStream().read(RECEBER_item, 0, RECEBER_item.length);
        System.out.println(duração_VALOR == datagrama.length);
        for (int i = 0; i < duração_VALOR; i++) if (RECEBER_item[i] != datagrama[i]) throw new RuntimeException("Conteúdo_VALOR 불일치");
        Ligar.getOutputStream().write(42);
        System.out.println(convidado_VALOR.getInputStream().read());
        convidado_VALOR.close();
        System.out.println(Ligar.getInputStream().read());
        Ligar.close(); servidor_VALOR.close();
        ServerSocket vazio_servidor = new ServerSocket(9250);
        vazio_servidor.setSoTimeout(10);
        try { vazio_servidor.accept(); System.out.println("BAD"); }
        catch (SocketTimeoutException expected) { System.out.println("valor_temporal 제한"); }
        vazio_servidor.close();
        try { new Socket("invalid.example", 80); System.out.println("BAD"); }
        catch (UnknownHostException expected) { System.out.println("DNS 미지원"); }
        System.out.println("STREAM PASS");
    }
}
