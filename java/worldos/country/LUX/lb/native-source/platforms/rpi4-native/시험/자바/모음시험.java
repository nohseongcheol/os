// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> Agab_Lëscht = new ArrayList<String>(); Agab_Lëscht.add("한글"); Agab_Lëscht.add("😀"); Agab_Lëscht.add("日本語");
        System.out.println(Agab_Lëscht.get(1)); System.out.println(Agab_Lëscht.set(1, "änneren_VALUE")); System.out.println(Agab_Lëscht.remove(0));
        System.out.println(Agab_Lëscht.size()); System.out.println(Agab_Lëscht.get(0));
        Map<String, Integer> Dictionnaire = new HashMap<String, Integer>();
        Dictionnaire.put("하나", 1); Dictionnaire.put("둘", 2); System.out.println(Dictionnaire.put("하나", 3).intValue());
        System.out.println(Dictionnaire.get("하나").intValue()); System.out.println(Dictionnaire.containsKey("둘"));
        System.gc(); System.out.println(Dictionnaire.remove("둘").intValue()); System.out.println(Dictionnaire.size());
        Agab_Lëscht.clear(); Dictionnaire.clear(); System.out.println(Agab_Lëscht.isEmpty()); System.out.println(Dictionnaire.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
