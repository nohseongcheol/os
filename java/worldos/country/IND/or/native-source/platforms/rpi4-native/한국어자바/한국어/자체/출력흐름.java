// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** ନିର୍ଗମ(出力)과 ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ: 순서를 보존해 내보내는 바이트의 ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି. */
public final class 출력흐름 {
    private final java.io.OutputStream 표준흐름;
    출력흐름(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void ଲେଖନ୍ତୁ(int ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준흐름.write(ମୂଲ୍ୟ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public void ଲେଖନ୍ତୁ(byte[] ଡାଟା) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준흐름.write(ଡାଟା);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public void ଲେଖନ୍ତୁ(byte[] ଡାଟା, int ଚଳାନ୍ତୁ, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준흐름.write(ଡାଟା, ଚଳାନ୍ତୁ, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public void 내보내기() throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준흐름.flush();
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public void ବନ୍ଦ_କରନ୍ତୁ() throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준흐름.close();
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
}
