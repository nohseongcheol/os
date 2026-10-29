// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class संकलन_चाचणी {
    public static void main(String[] a) {
        List<String> प्रविष्टी_यादी = new ArrayList<String>(); प्रविष्टी_यादी.add("한글"); प्रविष्टी_यादी.add("😀"); प्रविष्टी_यादी.add("日本語");
        System.out.println(प्रविष्टी_यादी.get(1)); System.out.println(प्रविष्टी_यादी.set(1, "बदल_करा_मूल्य")); System.out.println(प्रविष्टी_यादी.remove(0));
        System.out.println(प्रविष्टी_यादी.size()); System.out.println(प्रविष्टी_यादी.get(0));
        Map<String, Integer> शब्दकोश = new HashMap<String, Integer>();
        शब्दकोश.put("एक_मूल्य", 1); शब्दकोश.put("둘", 2); System.out.println(शब्दकोश.put("एक_मूल्य", 3).intValue());
        System.out.println(शब्दकोश.get("एक_मूल्य").intValue()); System.out.println(शब्दकोश.containsKey("둘"));
        System.gc(); System.out.println(शब्दकोश.remove("둘").intValue()); System.out.println(शब्दकोश.size());
        प्रविष्टी_यादी.clear(); शब्दकोश.clear(); System.out.println(प्रविष्टी_यादी.isEmpty()); System.out.println(शब्दकोश.isEmpty());
        System.out.println("한글😀वर्ण".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("पाठ्य")));
        String keep = "남는 पाठ्य"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
