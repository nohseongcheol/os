// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] Argumente) throws Română.propriu.I_O_excepție {
        Română.propriu.Rezultat.scriere_linie("propriu 컴파일러와 Română bibliotecă");
        int caracter_COUNT = Română.propriu.문자.cod_caracter_COUNT("한글😀");
        Română.propriu.Rezultat.수쓰기(caracter_COUNT);
        Română.propriu.Fișier.Scriere("한글자료.txt", "propriu nucleu_VALUE 안에서 저장한 한글😀");
        Română.propriu.Rezultat.scriere_linie(Română.propriu.Fișier.Citire("한글자료.txt"));
    }
}
