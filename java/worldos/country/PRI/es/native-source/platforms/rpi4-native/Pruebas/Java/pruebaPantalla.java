// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class pruebaPantalla {
    public static void main(String[] args) {
        español.propio.Pantalla.rectángulo(400, 400, 20, 20, 0x123456);
        try { español.propio.Pantalla.rectángulo(639, 479, 2, 2, 0); } catch (IllegalArgumentException e) { System.out.println("Pantalla recortar rechazarValor"); }
        System.out.println("JAVA FRAMEBUFFER PASS");
    }
}
