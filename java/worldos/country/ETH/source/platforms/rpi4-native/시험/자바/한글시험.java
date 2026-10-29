// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import አማርኛ.자체.문자;
import አማርኛ.자체.ፋይል;
import አማርኛ.자체.ምዝግብ_ዝርዝር;
import አማርኛ.자체.መዝገበ_ቃላት;
import አማርኛ.자체.ውጤት;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        ውጤት.ጻፍ_መስመር(문자.ምስጠራውን_ፍታ_ውሂብ(문자.부호화(인사))); ውጤት.수쓰기(문자.코드포인트수("한글😀"));
        ፋይል.መጻፊያ("한글자료.txt", 인사); ውጤት.ጻፍ_መስመር(ፋይል.ማንበቢያ("한글자료.txt"));
        ምዝግብ_ዝርዝር 이름들 = new ምዝግብ_ዝርዝር(); 이름들.더하기("가람"); 이름들.더하기("누리"); ውጤት.ጻፍ_መስመር(이름들.ማንበቢያ(1));
        መዝገበ_ቃላት 뜻 = new መዝገበ_ቃላት(); 뜻.넣기("가람", "강"); System.gc(); ውጤት.ጻፍ_መስመር(뜻.አግኝ_ምዝግብ("가람"));
        try { 문자.ምስጠራውን_ፍታ_ውሂብ(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { ውጤት.ጻፍ_መስመር("UTF-8 ስህተት አትቀበል_እሴት"); }
        ውጤት.ጻፍ_መስመር("አማርኛ ማከማቻ_ስፍራ 완료");
    }
}
