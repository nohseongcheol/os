// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class EsempioDisegno {
    public static void avvia() {
        // 640x480 schermata 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Italiano.nativo.schermata.rettangolo(600, 400, 28, 20, 0x0000ff);
        Italiano.nativo.schermata.rettangolo(600, 425, 28, 20, 0x00ff00);
        Italiano.nativo.schermata.rettangolo(600, 450, 28, 20, 0xff0000);
        Italiano.nativo.uscitaTesto.scrivere_riga("JAVA 그래픽: RGB");
        Italiano.nativo.uscitaTesto.scrivere_riga("Enter");
        Italiano.nativo.schermata.기다리기();
    }
}
