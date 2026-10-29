// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class ExemploDesenho {
    public static void iniciar() {
        // 640x480 tela 오른쪽에 빨강/초록/파랑 사각형을 그린다.
        Português.nativo.tela.retângulo(600, 400, 28, 20, 0x0000ff);
        Português.nativo.tela.retângulo(600, 425, 28, 20, 0x00ff00);
        Português.nativo.tela.retângulo(600, 450, 28, 20, 0xff0000);
        Português.nativo.saídaTexto.gravar_linha("JAVA 그래픽: RGB");
        Português.nativo.saídaTexto.gravar_linha("Enter");
        Português.nativo.tela.기다리기();
    }
}
