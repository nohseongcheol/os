export WORK_DIR=`pwd`
export BUILD_ABS_DIR="$WORK_DIR/build"
export GOPATH="$WORK_DIR"

GOARCH=386 GOOS=linux go build -gcflags '-N -l' -n  2>&1 |
	sed \
	-e "1s|^|set -e\n|" \
	-e "1s|^|mkdir -p $BUILD_ABS_DIR/b000\nprintf 'package cgo\n' > $BUILD_ABS_DIR/b000/cgo.go\n/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o $BUILD_ABS_DIR/b000/_pkg_.a -p runtime/cgo -complete -pack $BUILD_ABS_DIR/b000/cgo.go\n|" \
        -e "s|\$WORK|$BUILD_ABS_DIR|" \
	-e "/^EOF$/i packagefile runtime/cgo=$BUILD_ABS_DIR/b000/_pkg_.a" \
        -e "1s|^|export GOOS=linux\n|" \
        -e "1s|^|export GOARCH=386\n|" \
        -e "1s|^|export GOROOT=/usr/lib/go-1.10\n|" \
        -e "1s|^|export GOPATH=$BUILD_ABS_DIR\n|" \
	-e "1s|^|export CGO_ENABLED=0\n|" \
 	-e "1s|^|alias pack='go tool pack'\n|" \
	-e "/\/buildid/d" \
        -e "1s|^|WORK=\"$BUILD_ABS_DIR\"\n|" \
        -e "/^mv/d" \
        -e "s|-extld|-tmpdir='$BUILD_ABS_DIR'  -linkmode=external -extldflags='-nostartfiles -nodefaultlibs -nostdlib -r' -extld|g" 
        #-e "s|-extld|-tmpdir='$BUILD_ABS_DIR'  -linkmode=external -extldflags='-nostdlib' -extld|g" 
        #-e "s|-extld|-tmpdir='$BUILD_ABS_DIR'  -linkmode=external -extldflags=' -nostdlib -r' -extld|g" 
