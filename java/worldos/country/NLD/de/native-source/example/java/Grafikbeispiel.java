// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Grafikbeispiel {
    public static void ausführenVorgang() {
        // Rote, grüne und blaue Rechtecke rechts auf der 640x480-Anzeige zeichnen.
        Deutsch.eigen.Bildschirm.rechteck(600, 400, 28, 20, 0x0000ff);
        Deutsch.eigen.Bildschirm.rechteck(600, 425, 28, 20, 0x00ff00);
        Deutsch.eigen.Bildschirm.rechteck(600, 450, 28, 20, 0xff0000);
        Deutsch.eigen.Ausgabe.zeileSchreiben("JAVA 그래픽: RGB");
        Deutsch.eigen.Ausgabe.zeileSchreiben("Enter");
        Deutsch.eigen.Bildschirm.abwarten();
    }
}
