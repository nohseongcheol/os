// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 표준 main을 가진 기존 코드의 비공개 보조 함수를 진입점으로 고르지 않는다. */
public class entrada_compatibilidade_teste {
    private static void iniciar() { System.out.println("보조 FUNÇÃO_VALOR 호출"); }
    public static void main(String[] argumentos) {
        iniciar();
        System.out.println("표준 ponto_de_entrada reter_VALOR");
    }
}
