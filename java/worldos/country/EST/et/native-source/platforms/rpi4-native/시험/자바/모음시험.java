// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> kirje_Loend = new ArrayList<String>(); kirje_Loend.add("한글"); kirje_Loend.add("😀"); kirje_Loend.add("日本語");
        System.out.println(kirje_Loend.get(1)); System.out.println(kirje_Loend.set(1, "muutma_VALUE")); System.out.println(kirje_Loend.remove(0));
        System.out.println(kirje_Loend.size()); System.out.println(kirje_Loend.get(0));
        Map<String, Integer> sõnastik = new HashMap<String, Integer>();
        sõnastik.put("하나", 1); sõnastik.put("둘", 2); System.out.println(sõnastik.put("하나", 3).intValue());
        System.out.println(sõnastik.get("하나").intValue()); System.out.println(sõnastik.containsKey("둘"));
        System.gc(); System.out.println(sõnastik.remove("둘").intValue()); System.out.println(sõnastik.size());
        kirje_Loend.clear(); sõnastik.clear(); System.out.println(kirje_Loend.isEmpty()); System.out.println(sõnastik.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Tekst")));
        String keep = "남는 Tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
