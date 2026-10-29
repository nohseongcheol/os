// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> entrata_Lista = new ArrayList<String>(); entrata_Lista.add("한글"); entrata_Lista.add("😀"); entrata_Lista.add("日本語");
        System.out.println(entrata_Lista.get(1)); System.out.println(entrata_Lista.set(1, "bidel_VALUE")); System.out.println(entrata_Lista.remove(0));
        System.out.println(entrata_Lista.size()); System.out.println(entrata_Lista.get(0));
        Map<String, Integer> dizzjunarju = new HashMap<String, Integer>();
        dizzjunarju.put("하나", 1); dizzjunarju.put("둘", 2); System.out.println(dizzjunarju.put("하나", 3).intValue());
        System.out.println(dizzjunarju.get("하나").intValue()); System.out.println(dizzjunarju.containsKey("둘"));
        System.gc(); System.out.println(dizzjunarju.remove("둘").intValue()); System.out.println(dizzjunarju.size());
        entrata_Lista.clear(); dizzjunarju.clear(); System.out.println(entrata_Lista.isEmpty()); System.out.println(dizzjunarju.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
