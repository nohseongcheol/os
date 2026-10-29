// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumentos) throws Galego.자체.E_S_excepción {
        Galego.자체.Saída.escribir_liña("자체 컴파일러와 Galego biblioteca");
        int carácter_CONTAR = Galego.자체.문자.código_de_carácter_CONTAR("한글😀");
        Galego.자체.Saída.수쓰기(carácter_CONTAR);
        Galego.자체.Ficheiro.Escritura("한글자료.txt", "자체 kernel_VALOR 안에서 저장한 한글😀");
        Galego.자체.Saída.escribir_liña(Galego.자체.Ficheiro.Lectura("한글자료.txt"));
    }
}
