// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class TestCollection {
    public static void main(String[] a) {
        List<String> listeEntréeÉlément = new ArrayList<String>(); listeEntréeÉlément.add("한글"); listeEntréeÉlément.add("😀"); listeEntréeÉlément.add("日本語");
        System.out.println(listeEntréeÉlément.get(1)); System.out.println(listeEntréeÉlément.set(1, "changerValeur")); System.out.println(listeEntréeÉlément.remove(0));
        System.out.println(listeEntréeÉlément.size()); System.out.println(listeEntréeÉlément.get(0));
        Map<String, Integer> Dictionnaire = new HashMap<String, Integer>();
        Dictionnaire.put("valeurUn", 1); Dictionnaire.put("둘", 2); System.out.println(Dictionnaire.put("valeurUn", 3).intValue());
        System.out.println(Dictionnaire.get("valeurUn").intValue()); System.out.println(Dictionnaire.containsKey("둘"));
        System.gc(); System.out.println(Dictionnaire.remove("둘").intValue()); System.out.println(Dictionnaire.size());
        listeEntréeÉlément.clear(); Dictionnaire.clear(); System.out.println(listeEntréeÉlément.isEmpty()); System.out.println(Dictionnaire.isEmpty());
        System.out.println("한글😀Caractères".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("texte")));
        String keep = "남는 texte"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
