// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] 인수) throws Català.propi.E_S_excepció {
        Català.propi.Sortida.escriure_línia("propi 컴파일러와 Català biblioteca");
        int caràcter_COMPT = Català.propi.문자.codi_de_caràcter_COMPT("한글😀");
        Català.propi.Sortida.수쓰기(caràcter_COMPT);
        Català.propi.Fitxer.Escriptura("한글자료.txt", "propi nucli_VALOR 안에서 저장한 한글😀");
        Català.propi.Sortida.escriure_línia(Català.propi.Fitxer.Lectura("한글자료.txt"));
    }
}
