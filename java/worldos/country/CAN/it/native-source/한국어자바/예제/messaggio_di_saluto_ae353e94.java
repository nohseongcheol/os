// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.자바.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class messaggio_di_saluto_ae353e94 {
    public static void main(String[] argomenti) throws Exception {
        String testo = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path percorso = file.percorso("messaggio_di_saluto_ae353e94.txt");
        file.Scrittura(percorso, testo);
        System.out.println(file.Lettura(percorso));
        Thread lavoro_VALORE = 작업.avvia("messaggio_di_saluto_ae353e94 작업", () -> System.out.println("작업 thread_VALORE Esegui_comando"));
        작업.기다리기(lavoro_VALORE);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminale 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            schermata.나중에(() -> schermata.Finestra("다국어 messaggio_di_saluto_ae353e94", new JLabel(testo), 700, 160));
        }
    }
}
