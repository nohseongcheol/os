// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> unos_Popis = new ArrayList<String>(); unos_Popis.add("한글"); unos_Popis.add("😀"); unos_Popis.add("日本語");
        System.out.println(unos_Popis.get(1)); System.out.println(unos_Popis.set(1, "promijeniti_VALUE")); System.out.println(unos_Popis.remove(0));
        System.out.println(unos_Popis.size()); System.out.println(unos_Popis.get(0));
        Map<String, Integer> rječnik = new HashMap<String, Integer>();
        rječnik.put("하나", 1); rječnik.put("둘", 2); System.out.println(rječnik.put("하나", 3).intValue());
        System.out.println(rječnik.get("하나").intValue()); System.out.println(rječnik.containsKey("둘"));
        System.gc(); System.out.println(rječnik.remove("둘").intValue()); System.out.println(rječnik.size());
        unos_Popis.clear(); rječnik.clear(); System.out.println(unos_Popis.isEmpty()); System.out.println(rječnik.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Tekst")));
        String keep = "남는 Tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
