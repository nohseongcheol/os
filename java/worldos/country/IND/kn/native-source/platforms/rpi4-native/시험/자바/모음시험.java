// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ನಮೂದು_ಪಟ್ಟಿ = new ArrayList<String>(); ನಮೂದು_ಪಟ್ಟಿ.add("한글"); ನಮೂದು_ಪಟ್ಟಿ.add("😀"); ನಮೂದು_ಪಟ್ಟಿ.add("日本語");
        System.out.println(ನಮೂದು_ಪಟ್ಟಿ.get(1)); System.out.println(ನಮೂದು_ಪಟ್ಟಿ.set(1, "ಬದಲಿಸು_ಮೌಲ್ಯ")); System.out.println(ನಮೂದು_ಪಟ್ಟಿ.remove(0));
        System.out.println(ನಮೂದು_ಪಟ್ಟಿ.size()); System.out.println(ನಮೂದು_ಪಟ್ಟಿ.get(0));
        Map<String, Integer> ನಿಘಂಟು = new HashMap<String, Integer>();
        ನಿಘಂಟು.put("하나", 1); ನಿಘಂಟು.put("둘", 2); System.out.println(ನಿಘಂಟು.put("하나", 3).intValue());
        System.out.println(ನಿಘಂಟು.get("하나").intValue()); System.out.println(ನಿಘಂಟು.containsKey("둘"));
        System.gc(); System.out.println(ನಿಘಂಟು.remove("둘").intValue()); System.out.println(ನಿಘಂಟು.size());
        ನಮೂದು_ಪಟ್ಟಿ.clear(); ನಿಘಂಟು.clear(); System.out.println(ನಮೂದು_ಪಟ್ಟಿ.isEmpty()); System.out.println(ನಿಘಂಟು.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("ಪಠ್ಯ")));
        String keep = "남는 ಪಠ್ಯ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
