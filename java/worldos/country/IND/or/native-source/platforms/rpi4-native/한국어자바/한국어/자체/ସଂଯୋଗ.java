// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** ସଂଯୋଗ_କରନ୍ତୁ(連結)·ଚ୍ୟାନେଲ୍_ଏଣ୍ଟ୍ରି(通路): 상대와 이어진 TCP ବାଇଟ୍_ମୂଲ୍ୟ 흐름의 종단. */
public final class ସଂଯୋଗ {
    private final java.net.Socket 표준연결;
    ସଂଯୋଗ(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ସଂଯୋଗ ଖୋଲନ୍ତୁ(String ଠିକଣା, int ପୋର୍ଟ୍_ନମ୍ଵର୍) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try {
            return new ସଂଯୋଗ(new java.net.Socket(ଠିକଣା, ପୋର୍ଟ୍_ନମ୍ଵର୍));
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public 입력흐름 입력() throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public 출력흐름 ନିର୍ଗମ() throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public void 대기시간(int 밀리초) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public int ପୋର୍ଟ୍_ନମ୍ଵର୍() { return 표준연결.getPort(); }
    public int ସ୍ଥାନୀୟ_ପୋର୍ଟ୍_ନମ୍ଵର୍() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void ବନ୍ଦ_କରନ୍ତୁ() throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 표준연결.close();
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
}
