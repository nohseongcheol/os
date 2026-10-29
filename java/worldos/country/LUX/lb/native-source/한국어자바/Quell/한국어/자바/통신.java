// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Feeler 상태도 호출자가 판단할 수 있도록 äntweren 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI Adress, Duration Zäitlimitt)
            throws IOException, InterruptedException {
        HttpClient Verbannen = HttpClient.newBuilder().connectTimeout(Zäitlimitt).build();
        return Verbannen.send(HttpRequest.newBuilder(Adress).timeout(Zäitlimitt).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String Adress, int 포트, int 제한밀리초) throws IOException {
        Socket Verbannen = new Socket();
        try {
            Verbannen.connect(new InetSocketAddress(Adress, 포트), 제한밀리초);
            Verbannen.setSoTimeout(제한밀리초);
            return Verbannen;
        } catch (IOException Feeler) { Verbannen.close(); throw Feeler; }
    }
}
