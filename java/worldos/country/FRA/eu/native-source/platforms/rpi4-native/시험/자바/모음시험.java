// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> sarrera_Zerrenda = new ArrayList<String>(); sarrera_Zerrenda.add("한글"); sarrera_Zerrenda.add("😀"); sarrera_Zerrenda.add("日本語");
        System.out.println(sarrera_Zerrenda.get(1)); System.out.println(sarrera_Zerrenda.set(1, "aldatu_balio")); System.out.println(sarrera_Zerrenda.remove(0));
        System.out.println(sarrera_Zerrenda.size()); System.out.println(sarrera_Zerrenda.get(0));
        Map<String, Integer> hiztegi = new HashMap<String, Integer>();
        hiztegi.put("하나", 1); hiztegi.put("둘", 2); System.out.println(hiztegi.put("하나", 3).intValue());
        System.out.println(hiztegi.get("하나").intValue()); System.out.println(hiztegi.containsKey("둘"));
        System.gc(); System.out.println(hiztegi.remove("둘").intValue()); System.out.println(hiztegi.size());
        sarrera_Zerrenda.clear(); hiztegi.clear(); System.out.println(sarrera_Zerrenda.isEmpty()); System.out.println(hiztegi.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Testua")));
        String keep = "남는 Testua"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
