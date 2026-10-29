// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> įrašas_Sąrašas = new ArrayList<String>(); įrašas_Sąrašas.add("한글"); įrašas_Sąrašas.add("😀"); įrašas_Sąrašas.add("日本語");
        System.out.println(įrašas_Sąrašas.get(1)); System.out.println(įrašas_Sąrašas.set(1, "keisti_VALUE")); System.out.println(įrašas_Sąrašas.remove(0));
        System.out.println(įrašas_Sąrašas.size()); System.out.println(įrašas_Sąrašas.get(0));
        Map<String, Integer> žodynas = new HashMap<String, Integer>();
        žodynas.put("하나", 1); žodynas.put("둘", 2); System.out.println(žodynas.put("하나", 3).intValue());
        System.out.println(žodynas.get("하나").intValue()); System.out.println(žodynas.containsKey("둘"));
        System.gc(); System.out.println(žodynas.remove("둘").intValue()); System.out.println(žodynas.size());
        įrašas_Sąrašas.clear(); žodynas.clear(); System.out.println(įrašas_Sąrašas.isEmpty()); System.out.println(žodynas.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Tekstas")));
        String keep = "남는 Tekstas"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
