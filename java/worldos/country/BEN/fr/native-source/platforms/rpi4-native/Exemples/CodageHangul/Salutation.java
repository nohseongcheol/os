// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Salutation {
    static int ajouterValeurs(int ordinalPremier, int ordinalDeuxième) { return ordinalPremier + ordinalDeuxième; }
    public static void main(String[] arguments) {
        int valeurTotal = ajouterValeurs(20, 22);
        System.out.println("안녕하세요 · valeurTotal=" + valeurTotal);
    }
}
