// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package اردو.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP غلطی 상태도 호출자가 판단할 수 있도록 جواب_دیں 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI پتہ, Duration وقت_کی_حد)
            throws IOException, InterruptedException {
        HttpClient متصل_ہوں = HttpClient.newBuilder().connectTimeout(وقت_کی_حد).build();
        return متصل_ہوں.send(HttpRequest.newBuilder(پتہ).timeout(وقت_کی_حد).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String پتہ, int 포트, int 제한밀리초) throws IOException {
        Socket متصل_ہوں = new Socket();
        try {
            متصل_ہوں.connect(new InetSocketAddress(پتہ, 포트), 제한밀리초);
            متصل_ہوں.setSoTimeout(제한밀리초);
            return متصل_ہوں;
        } catch (IOException غلطی) { متصل_ہوں.close(); throw غلطی; }
    }
}
