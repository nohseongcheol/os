// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP njumte 상태도 호출자가 판단할 수 있도록 tontu 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI dëkkuwaay, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient JOKKOO = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return JOKKOO.send(HttpRequest.newBuilder(dëkkuwaay).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String dëkkuwaay, int jumtukaay_jël, int 제한밀리초) throws IOException {
        Socket JOKKOO = new Socket();
        try {
            JOKKOO.connect(new InetSocketAddress(dëkkuwaay, jumtukaay_jël), 제한밀리초);
            JOKKOO.setSoTimeout(제한밀리초);
            return JOKKOO;
        } catch (IOException njumte) { JOKKOO.close(); throw njumte; }
    }
}
