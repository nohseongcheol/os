// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ਦਾਖਲਾ_ਸੂਚੀ = new ArrayList<String>(); ਦਾਖਲਾ_ਸੂਚੀ.add("한글"); ਦਾਖਲਾ_ਸੂਚੀ.add("😀"); ਦਾਖਲਾ_ਸੂਚੀ.add("日本語");
        System.out.println(ਦਾਖਲਾ_ਸੂਚੀ.get(1)); System.out.println(ਦਾਖਲਾ_ਸੂਚੀ.set(1, "ਬਦਲੋ_ਕੀਮਤ")); System.out.println(ਦਾਖਲਾ_ਸੂਚੀ.remove(0));
        System.out.println(ਦਾਖਲਾ_ਸੂਚੀ.size()); System.out.println(ਦਾਖਲਾ_ਸੂਚੀ.get(0));
        Map<String, Integer> ਸ਼ਬਦਕੋਸ਼ = new HashMap<String, Integer>();
        ਸ਼ਬਦਕੋਸ਼.put("하나", 1); ਸ਼ਬਦਕੋਸ਼.put("둘", 2); System.out.println(ਸ਼ਬਦਕੋਸ਼.put("하나", 3).intValue());
        System.out.println(ਸ਼ਬਦਕੋਸ਼.get("하나").intValue()); System.out.println(ਸ਼ਬਦਕੋਸ਼.containsKey("둘"));
        System.gc(); System.out.println(ਸ਼ਬਦਕੋਸ਼.remove("둘").intValue()); System.out.println(ਸ਼ਬਦਕੋਸ਼.size());
        ਦਾਖਲਾ_ਸੂਚੀ.clear(); ਸ਼ਬਦਕੋਸ਼.clear(); System.out.println(ਦਾਖਲਾ_ਸੂਚੀ.isEmpty()); System.out.println(ਸ਼ਬਦਕੋਸ਼.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("ਟੈਕਸਟ")));
        String keep = "남는 ਟੈਕਸਟ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
