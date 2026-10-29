// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.awt.Font;

public final class FontFeatures {
    public static void main(String[] arguments) {
        String[] samples={"WorldOS", "한글", "日本語", "中文", "العربية", "עברית",
            "हिन्दी", "বাংলা", "ગુજરાતી", "ਪੰਜਾਬੀ", "தமிழ்", "తెలుగు", "ಕನ್ನಡ", "മലയാളം",
            "සිංහල", "ไทย", "ລາວ", "ខ្មែរ", "မြန်မာ", "བོད", "አማርኛ", "ქართული", "Հայերեն",
            "Русский", "ᏣᎳᎩ", "ᐃᓄᒃᑎᑐᑦ", "ދިވެހި"};
        for(String family:new String[]{"Dialog","Monospaced"}) {
            Font font=new Font(family,Font.PLAIN,17);
            for(String sample:samples) {
                if(font.canDisplayUpTo(sample)!=-1)
                    throw new AssertionError("Missing glyphs: "+family+" "+sample);
            }
        }
        System.out.println("PASS logical-fonts-27-script-samples");
    }
}
