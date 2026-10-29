// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ingizo_Orodha = new ArrayList<String>(); ingizo_Orodha.add("한글"); ingizo_Orodha.add("😀"); ingizo_Orodha.add("日本語");
        System.out.println(ingizo_Orodha.get(1)); System.out.println(ingizo_Orodha.set(1, "badilisha_thamani_16f64fe4")); System.out.println(ingizo_Orodha.remove(0));
        System.out.println(ingizo_Orodha.size()); System.out.println(ingizo_Orodha.get(0));
        Map<String, Integer> kamusi = new HashMap<String, Integer>();
        kamusi.put("하나", 1); kamusi.put("둘", 2); System.out.println(kamusi.put("하나", 3).intValue());
        System.out.println(kamusi.get("하나").intValue()); System.out.println(kamusi.containsKey("둘"));
        System.gc(); System.out.println(kamusi.remove("둘").intValue()); System.out.println(kamusi.size());
        ingizo_Orodha.clear(); kamusi.clear(); System.out.println(ingizo_Orodha.isEmpty()); System.out.println(kamusi.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
