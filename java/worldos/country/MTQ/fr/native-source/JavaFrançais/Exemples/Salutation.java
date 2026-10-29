// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.Java.*;
import java.nio.file.Path;
import java.awt.GraphicsEnvironment;
import javax.swing.*;

public class Salutation {
    public static void main(String[] arguments) throws Exception {
        String texte = "안녕하세요 · Hello · 日本語 · العربية · 😀";
        Path chemin = Fichier.chemin("Salutation.txt");
        Fichier.écrire(chemin, texte);
        System.out.println(Fichier.lire(chemin));
        Thread valeurTravail = Tâche.lancer("Salutation Tâche", () -> System.out.println("Tâche valeurFilExécution exécuterCommande"));
        Tâche.attendreFin(valeurTravail);
        if (GraphicsEnvironment.isHeadless()) {
            System.out.println("그래픽 화면이 없어 terminal 출력만 실행했습니다. 창을 보려면 QEMU 데스크톱의 터미널에서 실행하세요.");
        } else {
            Écran.valeurUltérieur(() -> Écran.fenêtre("다국어 Salutation", new JLabel(texte), 700, 160));
        }
    }
}
