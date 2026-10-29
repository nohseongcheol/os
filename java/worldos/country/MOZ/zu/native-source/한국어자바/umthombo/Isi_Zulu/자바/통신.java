// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Isi_Zulu.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Iphutha 상태도 호출자가 판단할 수 있도록 phendula 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ikheli, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Xhumanisa = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Xhumanisa.send(HttpRequest.newBuilder(ikheli).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ikheli, int 포트, int 제한밀리초) throws IOException {
        Socket Xhumanisa = new Socket();
        try {
            Xhumanisa.connect(new InetSocketAddress(ikheli, 포트), 제한밀리초);
            Xhumanisa.setSoTimeout(제한밀리초);
            return Xhumanisa;
        } catch (IOException Iphutha) { Xhumanisa.close(); throw Iphutha; }
    }
}
