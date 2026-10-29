// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class incasso_test {
    public static void main(String[] a) {
        List<String> invoer_Lijst_f07b3200 = new ArrayList<String>(); invoer_Lijst_f07b3200.add("한글"); invoer_Lijst_f07b3200.add("😀"); invoer_Lijst_f07b3200.add("日本語");
        System.out.println(invoer_Lijst_f07b3200.get(1)); System.out.println(invoer_Lijst_f07b3200.set(1, "wijzigen_WAARDE")); System.out.println(invoer_Lijst_f07b3200.remove(0));
        System.out.println(invoer_Lijst_f07b3200.size()); System.out.println(invoer_Lijst_f07b3200.get(0));
        Map<String, Integer> woordenlijst = new HashMap<String, Integer>();
        woordenlijst.put("하나", 1); woordenlijst.put("둘", 2); System.out.println(woordenlijst.put("하나", 3).intValue());
        System.out.println(woordenlijst.get("하나").intValue()); System.out.println(woordenlijst.containsKey("둘"));
        System.gc(); System.out.println(woordenlijst.remove("둘").intValue()); System.out.println(woordenlijst.size());
        invoer_Lijst_f07b3200.clear(); woordenlijst.clear(); System.out.println(invoer_Lijst_f07b3200.isEmpty()); System.out.println(woordenlijst.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("tekst")));
        String keep = "남는 tekst"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
