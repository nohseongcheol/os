// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 ଉପଭୋକ୍ତା 용어를 보존한다. 현재 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class ଫାଇଲ {
    private ଫାଇଲ() {}
    public static byte[] 바이트읽기(String ନାମ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try {
        FileInputStream ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ = new FileInputStream(ନାମ);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, ମୂଲ୍ୟ;
            while ((ମୂଲ୍ୟ = ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.read()) != -1) { if (수 == 임시.length) throw new ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ("ଫାଇଲ ଆକାର 제한"); 임시[수++] = (byte)ମୂଲ୍ୟ; }
            byte[] ମାପ = new byte[수]; System.arraycopy(임시, 0, ମାପ, 0, 수); return ମାପ;
        } finally { ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.close(); }
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static void ଲିଖନ_ବାଇଟ୍_ମୂଲ୍ୟ(String ନାମ, byte[] ବିଷୟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try {
        FileOutputStream ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ = new FileOutputStream(ନାମ);
        try { for (int ଲୁପ୍_ଅନୁକ୍ରମଣିକା = 0; ଲୁପ୍_ଅନୁକ୍ରମଣିକା < ବିଷୟ_ମୂଲ୍ୟ.length; ଲୁପ୍_ଅନୁକ୍ରମଣିକା++) ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.write(ବିଷୟ_ମୂଲ୍ୟ[ଲୁପ୍_ଅନୁକ୍ରମଣିକା] & 255); } finally { ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.close(); }
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static String ପଢନ୍ତୁ(String ନାମ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return 문자.ଡିକ୍ରିପ୍ଟ_ଡାଟା(바이트읽기(ନାମ));
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static void ଲେଖନ୍ତୁ(String ନାମ, String ବିଷୟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { ଲିଖନ_ବାଇଟ୍_ମୂଲ୍ୟ(ନାମ, 문자.부호화(ବିଷୟ_ମୂଲ୍ୟ));
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
}
