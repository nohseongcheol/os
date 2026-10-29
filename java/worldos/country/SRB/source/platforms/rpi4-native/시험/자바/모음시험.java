// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> унос_Листа = new ArrayList<String>(); унос_Листа.add("한글"); унос_Листа.add("😀"); унос_Листа.add("日本語");
        System.out.println(унос_Листа.get(1)); System.out.println(унос_Листа.set(1, "промијенити_вриједност")); System.out.println(унос_Листа.remove(0));
        System.out.println(унос_Листа.size()); System.out.println(унос_Листа.get(0));
        Map<String, Integer> речник = new HashMap<String, Integer>();
        речник.put("하나", 1); речник.put("둘", 2); System.out.println(речник.put("하나", 3).intValue());
        System.out.println(речник.get("하나").intValue()); System.out.println(речник.containsKey("둘"));
        System.gc(); System.out.println(речник.remove("둘").intValue()); System.out.println(речник.size());
        унос_Листа.clear(); речник.clear(); System.out.println(унос_Листа.isEmpty()); System.out.println(речник.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Текст")));
        String keep = "남는 Текст"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
