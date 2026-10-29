// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ExempleDessin {
    public static void lancer() {
        // Dessiner des rectangles rouge, vert et bleu à droite de l’affichage 640x480.
        français.interne.Écran.rectangle(600, 400, 28, 20, 0x0000ff);
        français.interne.Écran.rectangle(600, 425, 28, 20, 0x00ff00);
        français.interne.Écran.rectangle(600, 450, 28, 20, 0xff0000);
        français.interne.Sortie.écrireLigne("JAVA 그래픽: RGB");
        français.interne.Sortie.écrireLigne("Enter");
        français.interne.Écran.attendreFin();
    }
}
