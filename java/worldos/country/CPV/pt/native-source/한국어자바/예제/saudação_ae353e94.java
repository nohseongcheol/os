// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Português.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class saudação_ae353e94 {
    public static void main(String[] argumentos) throws Exception {
        String texto = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path caminho = ficheiro.caminho("saudação_ae353e94.txt");
        ficheiro.Escrita(caminho, texto);
        System.out.println(ficheiro.Leitura(caminho));
        Thread Trabalho_VALOR = 작업.iniciar("saudação_ae353e94 작업", () -> System.out.println("작업 thread_VALOR Executar_comando"));
        작업.기다리기(Trabalho_VALOR);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            tela.나중에(() -> tela.Janela("다국어 saudação_ae353e94", new JLabel(texto), 700, 160));
        }
    }
}
