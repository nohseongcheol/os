// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> stavka_Lista = new ArrayList<String>(); stavka_Lista.add("한글"); stavka_Lista.add("😀"); stavka_Lista.add("日本語");
        System.out.println(stavka_Lista.get(1)); System.out.println(stavka_Lista.set(1, "promeniti_VALUE")); System.out.println(stavka_Lista.remove(0));
        System.out.println(stavka_Lista.size()); System.out.println(stavka_Lista.get(0));
        Map<String, Integer> rečnik = new HashMap<String, Integer>();
        rečnik.put("하나", 1); rečnik.put("둘", 2); System.out.println(rečnik.put("하나", 3).intValue());
        System.out.println(rečnik.get("하나").intValue()); System.out.println(rečnik.containsKey("둘"));
        System.gc(); System.out.println(rečnik.remove("둘").intValue()); System.out.println(rečnik.size());
        stavka_Lista.clear(); rečnik.clear(); System.out.println(stavka_Lista.isEmpty()); System.out.println(rečnik.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
