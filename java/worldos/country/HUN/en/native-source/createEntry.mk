JavaCompiler ?= javac
javaLauncher ?= java
legacySourceFiles := $(shell find legacySource -type f -name '*.java' | sort)
classOutputDirectory := result/classValue
completionMarker := $(classOutputDirectory)/.isComplete

.PHONY: buildAll Checks Host checkHangul cleanBuild buildImage

buildAll: Checks

$(completionMarker): $(legacySourceFiles)
	mkdir -p $(classOutputDirectory)
	$(JavaCompiler) -encoding UTF-8 -Xlint:all -Werror -d $(classOutputDirectory) $(legacySourceFiles)
	touch $(completionMarker)

checkHangul:
	@sh tools/checkHangulNames.sh

Checks: checkHangul $(completionMarker)
	$(javaLauncher) -ea -cp $(classOutputDirectory) Hungary.JHunOS.tests.testAll

Host: Checks
	$(javaLauncher) -cp $(classOutputDirectory) Hungary.JHunOS.Host.hostStartup

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 legacySource/의 objectValue foundation 관리 kernelValue 전체를 AOT 변환하는 대상은 아니다.
buildImage:
	$(MAKE) -C os iso

cleanBuild:
	rm -rf result
