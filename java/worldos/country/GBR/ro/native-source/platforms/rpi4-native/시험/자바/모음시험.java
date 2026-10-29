// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> intrare_Listă = new ArrayList<String>(); intrare_Listă.add("한글"); intrare_Listă.add("😀"); intrare_Listă.add("日本語");
        System.out.println(intrare_Listă.get(1)); System.out.println(intrare_Listă.set(1, "schimba_VALUE")); System.out.println(intrare_Listă.remove(0));
        System.out.println(intrare_Listă.size()); System.out.println(intrare_Listă.get(0));
        Map<String, Integer> dicționar = new HashMap<String, Integer>();
        dicționar.put("하나", 1); dicționar.put("둘", 2); System.out.println(dicționar.put("하나", 3).intValue());
        System.out.println(dicționar.get("하나").intValue()); System.out.println(dicționar.containsKey("둘"));
        System.gc(); System.out.println(dicționar.remove("둘").intValue()); System.out.println(dicționar.size());
        intrare_Listă.clear(); dicționar.clear(); System.out.println(intrare_Listă.isEmpty()); System.out.println(dicționar.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
