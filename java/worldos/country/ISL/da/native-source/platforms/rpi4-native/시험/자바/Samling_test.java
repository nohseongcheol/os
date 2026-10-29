// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class Samling_test {
    public static void main(String[] a) {
        List<String> post_Liste = new ArrayList<String>(); post_Liste.add("한글"); post_Liste.add("😀"); post_Liste.add("日本語");
        System.out.println(post_Liste.get(1)); System.out.println(post_Liste.set(1, "ændre_VÆRDI")); System.out.println(post_Liste.remove(0));
        System.out.println(post_Liste.size()); System.out.println(post_Liste.get(0));
        Map<String, Integer> ordbog = new HashMap<String, Integer>();
        ordbog.put("하나", 1); ordbog.put("둘", 2); System.out.println(ordbog.put("하나", 3).intValue());
        System.out.println(ordbog.get("하나").intValue()); System.out.println(ordbog.containsKey("둘"));
        System.gc(); System.out.println(ordbog.remove("둘").intValue()); System.out.println(ordbog.size());
        post_Liste.clear(); ordbog.clear(); System.out.println(post_Liste.isEmpty()); System.out.println(ordbog.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Tekst")));
        String keep = "남는 Tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
