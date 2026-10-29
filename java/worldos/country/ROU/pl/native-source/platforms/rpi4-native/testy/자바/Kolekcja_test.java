// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class Kolekcja_test {
    public static void main(String[] a) {
        List<String> wpis_Lista = new ArrayList<String>(); wpis_Lista.add("한글"); wpis_Lista.add("😀"); wpis_Lista.add("日本語");
        System.out.println(wpis_Lista.get(1)); System.out.println(wpis_Lista.set(1, "zmienić_WARTOŚĆ")); System.out.println(wpis_Lista.remove(0));
        System.out.println(wpis_Lista.size()); System.out.println(wpis_Lista.get(0));
        Map<String, Integer> słownik = new HashMap<String, Integer>();
        słownik.put("하나", 1); słownik.put("둘", 2); System.out.println(słownik.put("하나", 3).intValue());
        System.out.println(słownik.get("하나").intValue()); System.out.println(słownik.containsKey("둘"));
        System.gc(); System.out.println(słownik.remove("둘").intValue()); System.out.println(słownik.size());
        wpis_Lista.clear(); słownik.clear(); System.out.println(wpis_Lista.isEmpty()); System.out.println(słownik.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("tekst")));
        String keep = "남는 tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
