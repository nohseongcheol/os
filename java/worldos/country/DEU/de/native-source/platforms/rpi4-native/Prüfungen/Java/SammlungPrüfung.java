// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class SammlungPrüfung {
    public static void main(String[] a) {
        List<String> eintragListe = new ArrayList<String>(); eintragListe.add("한글"); eintragListe.add("😀"); eintragListe.add("日本語");
        System.out.println(eintragListe.get(1)); System.out.println(eintragListe.set(1, "wertÄndern")); System.out.println(eintragListe.remove(0));
        System.out.println(eintragListe.size()); System.out.println(eintragListe.get(0));
        Map<String, Integer> Wörterbuch = new HashMap<String, Integer>();
        Wörterbuch.put("einsWert", 1); Wörterbuch.put("둘", 2); System.out.println(Wörterbuch.put("einsWert", 3).intValue());
        System.out.println(Wörterbuch.get("einsWert").intValue()); System.out.println(Wörterbuch.containsKey("둘"));
        System.gc(); System.out.println(Wörterbuch.remove("둘").intValue()); System.out.println(Wörterbuch.size());
        eintragListe.clear(); Wörterbuch.clear(); System.out.println(eintragListe.isEmpty()); System.out.println(Wörterbuch.isEmpty());
        System.out.println("한글😀Zeichen".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Text")));
        String keep = "남는 Text"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
