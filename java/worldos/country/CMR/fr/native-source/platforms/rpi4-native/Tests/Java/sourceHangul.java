// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class sourceHangul {
    public static void main(String[] arguments) throws français.interne.ExceptionSortieEntrée {
        français.interne.Sortie.écrireLigne("interne 컴파일러와 français bibliothèque");
        int nombreÉlémentsCaractère = français.interne.Caractères.nombreÉlémentsPointCode("한글😀");
        français.interne.Sortie.écrireNuméro(nombreÉlémentsCaractère);
        français.interne.Fichier.écrire("한글자료.txt", "interne valeurNoyau 안에서 저장한 한글😀");
        français.interne.Sortie.écrireLigne(français.interne.Fichier.lire("한글자료.txt"));
    }
}
