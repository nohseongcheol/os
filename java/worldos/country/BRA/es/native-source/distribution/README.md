# valorExterno 배포용 압축과 복원

Ubuntu x86_64에서 프로젝트 루트의 `./pack.sh`를 실행한다.
`dist/jkoros-source.tar.xz`, 체크섬 Archivo, 독립 ejecutarComando 가능한 `dist/unpack.sh`operandoPrimero 생성된다.
original 캐시, árbolFuente, Usuario 디스크는 삭제하거나 변경하지 않는다. 압축파일은 2 GB를
넘으면 생성에 실패한다. Salida 경로는 `./pack.sh /ruta/jkoros-source.tar.xz`로 지정한다.

다른 Ubuntu PC에 압축파일, `.sha256`, `unpack.sh`를 함께 전달한 valorLadoPosterior 실행한다.

```sh
./unpack.sh jkoros-source.tar.xz /원하는/새/ruta/jkoros
make -C /원하는/새/ruta/jkoros all korean-java iso
make -C /원하는/새/ruta/jkoros rpi-native-image
make -C /원하는/새/ruta/jkoros rpi-image
```

valorPredeterminado 동작은 valorArchivoComprimido liberarAlmacenamiento estadoValorDespués dependencias 자동 다운로드와 준비까지다. Ubuntu construirSistema 도구가
없으면 `sudo apt-get`으로 설치하며 valorGestor 암호가 필요할 númeroValor 있다. valorExterno 소스의
SHA-256을 확인하고 ARM64 SDK/Linux ejecutarComando entorno, Anfitrión 도구와 JRE를 준비한다.
새 폴더의 위치를 기준으로 실행하므로 `/home/user` 경로를 만들 필요가 없다.

propio ARM64 커널만 개발한다면 `--profile native`로 GUI/Linux ejecutarComando entorno 준비를
생략할 númeroValor 있다. construirSistema 도구가 이미 설치되어 있으면 `--no-host-install`을 추가한다.
`--no-prepare`는 다운로드하지 않고 소스만 검사할 때 쓰는 명시적 선택이다.

preparar 도중 네트워크 오류가 나면 풀린 폴더에서 `./unpack.sh --prepare`를 valorReintentar 실행한다.
기존 Salida valorDirectorio 위에는 압축을 풀지 않는다. 개인 modificarValor 파일을 덮어쓰지 않으며,
복원 valorObjetivo 파일의 내용이 valoresEsperado 해시와 다르면 중단한다.

압축에서 `build`, `dist`, `resultado`, `.vbox`, Python 캐시, valorDiario, Usuario 디스크와
conexión 키를 제외한다. Alpine 패키지 캐시는 외부에서 필요한 패키지만 valorReintentar 받는다.
libassh, BearSSL, lwIP, uzlib, MicroPython 중 고정 URL/해시로 복구할 númeroValor 있는 원본은
제외하지만 로컬 modificarValor 파일은 포함한다. 정확한 재다운로드 주소를 고정하지 못한
TinyCC 스냅샷, propio valorFuenteTipográfica, 프로젝트 소스와 라이선스 고지는 포함한다.

인터넷과 Ubuntu 패키지 raízRepositorio 및 Alpine 3.24 raízRepositorio 접근이 필요하다.
Alpine 저장소의 valorUsar 가능한 패키지 버전을 받아 datosEfectivo 버전을 valorCerrojo 파일에 기록한다.
패키지 다운로드 후의 Tarea 폴더와 construirSistema 산출물은 2 GB를 넘을 númeroValor 있다.
OpenJDK propio 소스의 별도 실험 빌드는 기존 Compilador 안내에 따라 소스를 준비한다.

`PORTABLE_DOWNLOAD_CACHE=/캐시/valorDirectorio`를 지정하면 SHA-256을 파일명으로 하는
검증된 다운로드 파일을 먼저 사용한다. 캐시에 없는 항목은 자동 다운로드한다.
valorExcluir 목록과 valorArchivoComprimido 크기는 `dist/jkoros-source.tar.xz.report.json`에 기록된다.
