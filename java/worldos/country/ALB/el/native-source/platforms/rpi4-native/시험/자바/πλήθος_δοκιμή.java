// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class πλήθος_δοκιμή {
    public static void main(String[] a) {
        List<String> καταχώρηση_Λίστα = new ArrayList<String>(); καταχώρηση_Λίστα.add("한글"); καταχώρηση_Λίστα.add("😀"); καταχώρηση_Λίστα.add("日本語");
        System.out.println(καταχώρηση_Λίστα.get(1)); System.out.println(καταχώρηση_Λίστα.set(1, "αλλάζω_τιμή")); System.out.println(καταχώρηση_Λίστα.remove(0));
        System.out.println(καταχώρηση_Λίστα.size()); System.out.println(καταχώρηση_Λίστα.get(0));
        Map<String, Integer> λεξικό = new HashMap<String, Integer>();
        λεξικό.put("하나", 1); λεξικό.put("둘", 2); System.out.println(λεξικό.put("하나", 3).intValue());
        System.out.println(λεξικό.get("하나").intValue()); System.out.println(λεξικό.containsKey("둘"));
        System.gc(); System.out.println(λεξικό.remove("둘").intValue()); System.out.println(λεξικό.size());
        καταχώρηση_Λίστα.clear(); λεξικό.clear(); System.out.println(καταχώρηση_Λίστα.isEmpty()); System.out.println(λεξικό.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("Κείμενο")));
        String keep = "남는 Κείμενο"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
