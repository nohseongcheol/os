// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> प्रवेश_सुची = new ArrayList<String>(); प्रवेश_सुची.add("한글"); प्रवेश_सुची.add("😀"); प्रवेश_सुची.add("日本語");
        System.out.println(प्रवेश_सुची.get(1)); System.out.println(प्रवेश_सुची.set(1, "बदलचें_मोल")); System.out.println(प्रवेश_सुची.remove(0));
        System.out.println(प्रवेश_सुची.size()); System.out.println(प्रवेश_सुची.get(0));
        Map<String, Integer> डिक्शनरी = new HashMap<String, Integer>();
        डिक्शनरी.put("하나", 1); डिक्शनरी.put("둘", 2); System.out.println(डिक्शनरी.put("하나", 3).intValue());
        System.out.println(डिक्शनरी.get("하나").intValue()); System.out.println(डिक्शनरी.containsKey("둘"));
        System.gc(); System.out.println(डिक्शनरी.remove("둘").intValue()); System.out.println(डिक्शनरी.size());
        प्रवेश_सुची.clear(); डिक्शनरी.clear(); System.out.println(प्रवेश_सुची.isEmpty()); System.out.println(डिक्शनरी.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 SMS"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
