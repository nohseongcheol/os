// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ସଂଯୋଗ ଖୋଲନ୍ତୁ(String ଠିକଣା, int ପୋର୍ଟ୍_ନମ୍ଵର୍) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return ସଂଯୋଗ.ଖୋଲନ୍ତୁ(ଠିକଣା, ପୋର୍ଟ୍_ନମ୍ଵର୍);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static 수신창구 수신열기(int ପୋର୍ଟ୍_ନମ୍ଵର୍) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return 수신창구.ଖୋଲନ୍ତୁ(ପୋର୍ଟ୍_ନମ୍ଵର୍);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static Socket ସଂଯୋଗ_କରନ୍ତୁ(String ଠିକଣା, int ପୋର୍ଟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return new Socket(ଠିକଣା, ପୋର୍ଟ_ମୂଲ୍ୟ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static ServerSocket 듣기(int ପୋର୍ଟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return new ServerSocket(ପୋର୍ଟ_ମୂଲ୍ୟ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static Socket 받기(ServerSocket ସର୍ଭର୍_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return ସର୍ଭର୍_ମୂଲ୍ୟ.accept();
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
}
