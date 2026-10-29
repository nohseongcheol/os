// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> go_tsenya_tshedimošo_Lenaneo = new ArrayList<String>(); go_tsenya_tshedimošo_Lenaneo.add("한글"); go_tsenya_tshedimošo_Lenaneo.add("😀"); go_tsenya_tshedimošo_Lenaneo.add("日本語");
        System.out.println(go_tsenya_tshedimošo_Lenaneo.get(1)); System.out.println(go_tsenya_tshedimošo_Lenaneo.set(1, "fetoša_boleng")); System.out.println(go_tsenya_tshedimošo_Lenaneo.remove(0));
        System.out.println(go_tsenya_tshedimošo_Lenaneo.size()); System.out.println(go_tsenya_tshedimošo_Lenaneo.get(0));
        Map<String, Integer> lefelopolokelo = new HashMap<String, Integer>();
        lefelopolokelo.put("하나", 1); lefelopolokelo.put("둘", 2); System.out.println(lefelopolokelo.put("하나", 3).intValue());
        System.out.println(lefelopolokelo.get("하나").intValue()); System.out.println(lefelopolokelo.containsKey("둘"));
        System.gc(); System.out.println(lefelopolokelo.remove("둘").intValue()); System.out.println(lefelopolokelo.size());
        go_tsenya_tshedimošo_Lenaneo.clear(); lefelopolokelo.clear(); System.out.println(go_tsenya_tshedimošo_Lenaneo.isEmpty()); System.out.println(lefelopolokelo.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Sengwalwa")));
        String keep = "남는 Sengwalwa"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
