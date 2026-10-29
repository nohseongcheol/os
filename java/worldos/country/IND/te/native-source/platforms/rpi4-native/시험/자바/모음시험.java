// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class 모음시험 {
    public static void main(String[] a) {
        List<String> ప్రవేశం_జాబితా = new ArrayList<String>(); ప్రవేశం_జాబితా.add("한글"); ప్రవేశం_జాబితా.add("😀"); ప్రవేశం_జాబితా.add("日本語");
        System.out.println(ప్రవేశం_జాబితా.get(1)); System.out.println(ప్రవేశం_జాబితా.set(1, "మార్చు_మూల్యం")); System.out.println(ప్రవేశం_జాబితా.remove(0));
        System.out.println(ప్రవేశం_జాబితా.size()); System.out.println(ప్రవేశం_జాబితా.get(0));
        Map<String, Integer> నిఘంటువు = new HashMap<String, Integer>();
        నిఘంటువు.put("하나", 1); నిఘంటువు.put("둘", 2); System.out.println(నిఘంటువు.put("하나", 3).intValue());
        System.out.println(నిఘంటువు.get("하나").intValue()); System.out.println(నిఘంటువు.containsKey("둘"));
        System.gc(); System.out.println(నిఘంటువు.remove("둘").intValue()); System.out.println(నిఘంటువు.size());
        ప్రవేశం_జాబితా.clear(); నిఘంటువు.clear(); System.out.println(ప్రవేశం_జాబితా.isEmpty()); System.out.println(నిఘంటువు.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("పాఠ్యము")));
        String keep = "남는 పాఠ్యము"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
