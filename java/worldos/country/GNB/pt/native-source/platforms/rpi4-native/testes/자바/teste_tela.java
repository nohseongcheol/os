// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class teste_tela {
    public static void main(String[] args) {
        Português.nativo.tela.retângulo(400, 400, 20, 20, 0x123456);
        try { Português.nativo.tela.retângulo(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("tela recortar rejeitar_VALOR"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
