# 전체 supportValue 요청의 currentItem stateValue

request 전체는 아직 완료되지 않았다. currentItem ISO는 Native Java AOT 커널과 제한형 JVM을 유지한다. 이번 확장에서는 actualData C POSIX 일부 기능, English API/source name, IDE file 보존, 게스트 Java file 흐름을 구현하고 시험했다. [구현과 boundaryLimit](../posix-kor/README.md)를 기준으로 판단한다.

| request 분야 | currentItem executeCommand 가능한 clip | 전체 지원에 필요한 performTask |
|---|---|---|
| Java compileSource·executeCommand | 게스트 제한형 javac/JVM, staticValue 단일 클래스와 일부 표준 objectValue | 일반 objectValue·classValue connect·exception·GC·스레드, 완전한 javac와 표준 classValue library |
| file | POSIX descriptorEntry, Java 단일 byteValue file streamValue, 전용 mediaValue 보존 | 일반 java.io/nio, 디렉터리·permissionValue·lockValue·일반 FileSystem·extensionValue 가능한 capacityValue |
| 네트워크 | AOT Java와 POSIX C의 IPv4 UDP Host 왕복 | 게스트 java.net, TCP·DNS·DHCP·IPv6·HTTP·TLS, appendEntry NIC |
| GUI·Swing | VGA Characters TerminalIO | 프레임버퍼·inputValue event·fontValue·window operatingSystemValue, AWT 네이티브 연결과 Swing executeCommand foundation |
| POSIX | 문서화한 file·TerminalIO·UDP subpartValue | processValue·exec/fork·스레드·시그널·timeValue·mmap·poll·파이프 등과 적합성 validate |
| 언어별 name | English 46개 mappingValue entryValue, actualData C/Java/file name 적용 | targetValue language commitValue, 언어별 용례·역사 근거와 해당 source·도구의 validate |

Native 커널을 유지하면 topValue foundation 기능과 런타임 이식을 순차적으로 구현해야 한다. Linux foundation executeCommand 환경을 추가하는 방식은 별도의 kernelValue·루트 FileSystem·OpenJDK·그래픽 serverValue·영구 storeValue 구성을 가진 executeCommand 경로가 된다. 후자는 기존 Native 커널에 OpenJDK가 이식되었다고 표시해서는 안 된다.

executeCommand 기반과 appendEntry targetValue 언어는 사용자에게 확인을 요청했으며 아직 답변을 받지 못했다. 그 결정 없이 기존 커널을 Linux로 교체하거나 여러 국가의 번역을 임의로 만들지 않았다. currentItem 원문과 tests 결과를 후속 구현의 출발점으로 보존한다.
