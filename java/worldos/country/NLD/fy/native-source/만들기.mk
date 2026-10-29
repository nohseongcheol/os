자바컴파일러 ?= javac
자바실행기 ?= java
원천파일 := $(shell find 원천 -type f -name '*.java' | sort)
클래스위치 := 결과/클래스
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 호스트 한글검사 정리 이미지

모두: 검사

$(완료표시): $(원천파일)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(원천파일)
	touch $(완료표시)

한글검사:
	@sh 도구/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Nederlân.JNldOS.시험.전체시험

호스트: 검사
	$(자바실행기) -cp $(클래스위치) Nederlân.JNldOS.호스트.호스트시작

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 원천/의 객체 기반 관리 커널 전체를 AOT 변환하는 대상은 아니다.
이미지:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
