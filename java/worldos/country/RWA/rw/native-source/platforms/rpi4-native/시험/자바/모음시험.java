// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> icyinjizwa_Urutonde = new ArrayList<String>(); icyinjizwa_Urutonde.add("한글"); icyinjizwa_Urutonde.add("😀"); icyinjizwa_Urutonde.add("日本語");
        System.out.println(icyinjizwa_Urutonde.get(1)); System.out.println(icyinjizwa_Urutonde.set(1, "guhindura_agaciro_16f64fe4")); System.out.println(icyinjizwa_Urutonde.remove(0));
        System.out.println(icyinjizwa_Urutonde.size()); System.out.println(icyinjizwa_Urutonde.get(0));
        Map<String, Integer> inkoranyamagambo = new HashMap<String, Integer>();
        inkoranyamagambo.put("하나", 1); inkoranyamagambo.put("둘", 2); System.out.println(inkoranyamagambo.put("하나", 3).intValue());
        System.out.println(inkoranyamagambo.get("하나").intValue()); System.out.println(inkoranyamagambo.containsKey("둘"));
        System.gc(); System.out.println(inkoranyamagambo.remove("둘").intValue()); System.out.println(inkoranyamagambo.size());
        icyinjizwa_Urutonde.clear(); inkoranyamagambo.clear(); System.out.println(icyinjizwa_Urutonde.isEmpty()); System.out.println(inkoranyamagambo.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Umwandiko")));
        String keep = "남는 Umwandiko"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
