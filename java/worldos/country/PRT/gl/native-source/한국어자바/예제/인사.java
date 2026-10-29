// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Galego.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class 인사 {
    public static void main(String[] Argumentos) throws Exception {
        String Texto = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path CAMIÑO = Ficheiro.CAMIÑO("인사.txt");
        Ficheiro.Escritura(CAMIÑO, Texto);
        System.out.println(Ficheiro.Lectura(CAMIÑO));
        Thread traballo_VALOR = 작업.Executar_2("인사 작업", () -> System.out.println("작업 tema_VALOR executar_comando"));
        작업.기다리기(traballo_VALOR);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 Terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            화면.나중에(() -> 화면.Xanela("다국어 인사", new JLabel(Texto), 700, 160));
        }
    }
}
