// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package worldos.PRT.l_pt;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.net.*;
import java.util.*;

/** Local-language Java entry points into the real JDK/Linux implementation. */
public final class chamada_ao_sistema {
    private chamada_ao_sistema() { }
    public static RandomAccessFile Abrir(String caminho, String Modo) throws IOException {
        return new RandomAccessFile(caminho, Modo);
    }
    public static int Leitura(RandomAccessFile ficheiro, byte[] dados) throws IOException {
        return ficheiro.read(dados);
    }
    public static void Escrita(RandomAccessFile ficheiro, byte[] dados) throws IOException {
        ficheiro.write(dados);
    }
    public static void seek(RandomAccessFile ficheiro, long posição) throws IOException {
        ficheiro.seek(posição);
    }
    public static void sync(RandomAccessFile ficheiro) throws IOException {
        ficheiro.getFD().sync();
    }
    public static void Fechar(RandomAccessFile ficheiro) throws IOException {
        ficheiro.close();
    }
    public static void Remover(String caminho) throws IOException {
        Files.delete(Paths.get(caminho));
    }
    public static long Tamanho(String caminho) throws IOException {
        return Files.size(Paths.get(caminho));
    }
    public static Socket Ligar(String Endereço, int númeroPorta) throws IOException {
        return new Socket(Endereço, númeroPorta);
    }
    public static DatagramSocket datagram(int númeroPorta) throws SocketException {
        return new DatagramSocket(númeroPorta);
    }
    public static Thread fioExecução(Runnable Acção) {
        Thread fioExecução = new Thread(Acção);
        fioExecução.start();
        return fioExecução;
    }
    public static Process Executar(List<String> comando) throws IOException {
        return new ProcessBuilder(comando).start();
    }
}
