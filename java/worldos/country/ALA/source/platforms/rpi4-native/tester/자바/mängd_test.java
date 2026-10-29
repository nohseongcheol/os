// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class mängd_test {
    public static void main(String[] a) {
        List<String> post_ange = new ArrayList<String>(); post_ange.add("한글"); post_ange.add("😀"); post_ange.add("日本語");
        System.out.println(post_ange.get(1)); System.out.println(post_ange.set(1, "ändra_värde")); System.out.println(post_ange.remove(0));
        System.out.println(post_ange.size()); System.out.println(post_ange.get(0));
        Map<String, Integer> ordlista = new HashMap<String, Integer>();
        ordlista.put("하나", 1); ordlista.put("둘", 2); System.out.println(ordlista.put("하나", 3).intValue());
        System.out.println(ordlista.get("하나").intValue()); System.out.println(ordlista.containsKey("둘"));
        System.gc(); System.out.println(ordlista.remove("둘").intValue()); System.out.println(ordlista.size());
        post_ange.clear(); ordlista.clear(); System.out.println(post_ange.isEmpty()); System.out.println(ordlista.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("text")));
        String keep = "남는 text"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
