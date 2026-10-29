// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.ArrayList;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
public class ᎦᏟᏌᏅᎢ_ᎠᏓᎪᎵᏰᏍᎩ {
    public static void main(String[] a) {
        List<String> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ = new ArrayList<String>(); Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.add("한글"); Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.add("😀"); Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.add("日本語");
        System.out.println(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.get(1)); System.out.println(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.set(1, "ᎯᏁᏟᏴᎾ_ᏧᎬᏩᎶᏗᏯ")); System.out.println(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.remove(0));
        System.out.println(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.size()); System.out.println(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.get(0));
        Map<String, Integer> 사전 = new HashMap<String, Integer>();
        사전.put("하나", 1); 사전.put("둘", 2); System.out.println(사전.put("하나", 3).intValue());
        System.out.println(사전.get("하나").intValue()); System.out.println(사전.containsKey("둘"));
        System.gc(); System.out.println(사전.remove("둘").intValue()); System.out.println(사전.size());
        Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.clear(); 사전.clear(); System.out.println(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ.isEmpty()); System.out.println(사전.isEmpty());
        System.out.println("한글😀문자".substring(2, 4).concat("!")); System.out.println("한글".equals("한".concat("글")));
        String keep = "남는 ᎠᎪᎵᏰᏗ"; int sum = 0;
        for (int i = 0; i < 350; i++) { int[] garbage = new int[200]; garbage[0] = i; sum += garbage[0]; }
        System.out.println(sum); System.out.println(keep);
    }
}
