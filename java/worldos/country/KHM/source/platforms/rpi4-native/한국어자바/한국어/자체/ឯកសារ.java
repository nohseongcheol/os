// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 អ្នកប្រើ 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ឯកសារ {
    private ឯកសារ() {}
    public static byte[] 바이트읽기(String ឈ្មោះ) throws ចូល_ចេញ_ការលើកលែង {
        try {
        FileInputStream ស្ទ្រីម_តំលៃ = new FileInputStream(ឈ្មោះ);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, តំលៃ;
            while ((តំលៃ = ស្ទ្រីម_តំលៃ.read()) != -1) { if (수 == 임시.length) throw new ចូល_ចេញ_ការលើកលែង("ឯកសារ ដាក់ទំហំ 제한"); 임시[수++] = (byte)តំលៃ; }
            byte[] ការវាស់វែង = new byte[수]; System.arraycopy(임시, 0, ការវាស់វែង, 0, 수); return ការវាស់វែង;
        } finally { ស្ទ្រីម_តំលៃ.close(); }
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static void សរសេរ_បៃ_តំលៃ(String ឈ្មោះ, byte[] មាតិកា_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try {
        FileOutputStream ស្ទ្រីម_តំលៃ = new FileOutputStream(ឈ្មោះ);
        try { for (int រង្វិលជុំ_សន្ទស្សន៏ = 0; រង្វិលជុំ_សន្ទស្សន៏ < មាតិកា_តំលៃ.length; រង្វិលជុំ_សន្ទស្សន៏++) ស្ទ្រីម_តំលៃ.write(មាតិកា_តំលៃ[រង្វិលជុំ_សន្ទស្សន៏] & 255); } finally { ស្ទ្រីម_តំលៃ.close(); }
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static String អាន(String ឈ្មោះ) throws ចូល_ចេញ_ការលើកលែង {
        try { return 문자.ដោះកូដ_ទិន្នន័យ(바이트읽기(ឈ្មោះ));
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static void សរសេរ(String ឈ្មោះ, String មាតិកា_តំលៃ) throws ចូល_ចេញ_ការលើកលែង {
        try { សរសេរ_បៃ_តំលៃ(ឈ្មោះ, 문자.부호화(មាតិកា_តំលៃ));
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
}
