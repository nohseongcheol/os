// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
/** 통신(通信): IPv4 UDP 전문. 외부 주소는 ଅଙ୍କ_ମୂଲ୍ୟ 주소를 사용한다. */
public final class 통신 {
    private 통신() {}
    public static DatagramSocket ଖୋଲନ୍ତୁ(int ପୋର୍ଟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { return new DatagramSocket(ପୋର୍ଟ_ମୂଲ୍ୟ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static void ପଠାନ୍ତୁ(DatagramSocket 종단, int ପୋର୍ଟ_ମୂଲ୍ୟ, String ବିଷୟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try {
        ପଠାନ୍ତୁ(종단, "127.0.0.1", ପୋର୍ଟ_ମୂଲ୍ୟ, ବିଷୟ_ମୂଲ୍ୟ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static void ପଠାନ୍ତୁ(DatagramSocket 종단, String ଠିକଣା, int ପୋର୍ଟ_ମୂଲ୍ୟ, String ବିଷୟ_ମୂଲ୍ୟ) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try {
        byte[] ବାଇଟ୍_ମୂଲ୍ୟ = 문자.부호화(ବିଷୟ_ମୂଲ୍ୟ);
        종단.send(new DatagramPacket(ବାଇଟ୍_ମୂଲ୍ୟ, ବାଇଟ୍_ମୂଲ୍ୟ.length, InetAddress.getByName(ଠିକଣା), ପୋର୍ଟ_ମୂଲ୍ୟ));
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static String 받기(DatagramSocket 종단) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try {
        byte[] ବାଇଟ୍_ମୂଲ୍ୟ = new byte[512]; DatagramPacket 전문 = new DatagramPacket(ବାଇଟ୍_ମୂଲ୍ୟ, ବାଇଟ୍_ମୂଲ୍ୟ.length); 종단.receive(전문);
        byte[] ମାପ = new byte[전문.getLength()]; System.arraycopy(ବାଇଟ୍_ମୂଲ୍ୟ, 0, ମାପ, 0, ମାପ.length); return 문자.ଡିକ୍ରିପ୍ଟ_ଡାଟା(ମାପ);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static void 대기시간(DatagramSocket 종단, int 밀리초) throws ଇନପୁଟ୍_ଆଉଟପୁଟ୍_ବ୍ୟତିକ୍ରମ {
        try { 종단.setSoTimeout(밀리초);
        } catch (java.io.IOException ତ୍ରୁଟି) { throw 예외변환.ଇନପୁଟ୍_ଆଉଟପୁଟ୍(ତ୍ରୁଟି); }
        catch (RuntimeException ତ୍ରୁଟି) { throw 예외변환.ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ତ୍ରୁଟି); }
    }
    public static void ବନ୍ଦ_କରନ୍ତୁ(DatagramSocket 종단) { 종단.close(); }
}
