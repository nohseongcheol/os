// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Saludo {
    static int añadirValores(int ordinalPrimero, int ordinalSegundo) { return ordinalPrimero + ordinalSegundo; }
    public static void main(String[] argumentos) {
        int valorTotal = añadirValores(20, 22);
        System.out.println("안녕하세요 · valorTotal=" + valorTotal);
    }
}
