// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class Samling_test {
    public static void main(String[] a) {
        List<String> oppføring_Liste = new ArrayList<String>(); oppføring_Liste.add("한글"); oppføring_Liste.add("😀"); oppføring_Liste.add("日本語");
        System.out.println(oppføring_Liste.get(1)); System.out.println(oppføring_Liste.set(1, "endre_VERDI")); System.out.println(oppføring_Liste.remove(0));
        System.out.println(oppføring_Liste.size()); System.out.println(oppføring_Liste.get(0));
        Map<String, Integer> ordliste = new HashMap<String, Integer>();
        ordliste.put("하나", 1); ordliste.put("둘", 2); System.out.println(ordliste.put("하나", 3).intValue());
        System.out.println(ordliste.get("하나").intValue()); System.out.println(ordliste.containsKey("둘"));
        System.gc(); System.out.println(ordliste.remove("둘").intValue()); System.out.println(ordliste.size());
        oppføring_Liste.clear(); ordliste.clear(); System.out.println(oppføring_Liste.isEmpty()); System.out.println(ordliste.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Tekst")));
        String keep = "남는 Tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
