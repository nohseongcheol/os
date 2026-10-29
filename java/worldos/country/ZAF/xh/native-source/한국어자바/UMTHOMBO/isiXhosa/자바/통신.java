// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package isiXhosa.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP Impazamo 상태도 호출자가 판단할 수 있도록 phendula 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI idilesi, Duration 제한시간)
            throws IOException, InterruptedException {
        HttpClient Nxulumanisa = HttpClient.newBuilder().connectTimeout(제한시간).build();
        return Nxulumanisa.send(HttpRequest.newBuilder(idilesi).timeout(제한시간).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String idilesi, int 포트, int 제한밀리초) throws IOException {
        Socket Nxulumanisa = new Socket();
        try {
            Nxulumanisa.connect(new InetSocketAddress(idilesi, 포트), 제한밀리초);
            Nxulumanisa.setSoTimeout(제한밀리초);
            return Nxulumanisa;
        } catch (IOException Impazamo) { Nxulumanisa.close(); throw Impazamo; }
    }
}
