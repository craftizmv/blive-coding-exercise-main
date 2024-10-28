
build:
    go build -ldflags "-X main.buildVersion=dev" -o ./bin/server

cover-build:
	go test -race -coverpkg="./..." -c -tags testrunmain -v -o bin/app.test .

cucumber *args: cover-build
    mkdir -p cucumber/coverage
    (cd cucumber && ./run_tests {{args}} || true )

unit:
    mkdir -p coverage
    go test -v -race -coverpkg="./..." -coverprofile=./coverage/unit-cover.profile ./...

test: unit cucumber

coverage: test
    gocovmerge coverage/unit-cover.profile cucumber/coverage/int-cover.profile | grep -v "sharedtest" > coverage/combined.profile
    go tool cover -func coverage/combined.profile | tail -n 1 | xargs

fmt:
    go fmt ./...
    go vet ./...
    goimports -w .
