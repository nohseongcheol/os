// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Gwall 상태도 호출자가 판단할 수 있도록 ateb 전체를 반환한다. */
    public static HttpResponse<String> TAKE_VALUE(URI ADDRESS, Duration terfyn_amser)
            throws IOException, InterruptedException {
        HttpClient Cysylltu = HttpClient.newBuilder().connectTimeout(terfyn_amser).build();
        return Cysylltu.send(HttpRequest.newBuilder(ADDRESS).timeout(terfyn_amser).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ADDRESS, int 포트, int 제한밀리초) throws IOException {
        Socket Cysylltu = new Socket();
        try {
            Cysylltu.connect(new InetSocketAddress(ADDRESS, 포트), 제한밀리초);
            Cysylltu.setSoTimeout(제한밀리초);
            return Cysylltu;
        } catch (IOException Gwall) { Cysylltu.close(); throw Gwall; }
    }
}
