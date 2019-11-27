# Random notes

## TODO

- Separate travis build stages for docker, packages, repository and jekyll site
- Build jekyll static site using docker to be ci-system-agnostic
- Build docker image in travis?
- Also push docker image to GitHub docker repo?
- Add other packages...

## Notes

```
docker build .docker --file .docker/Dockerfile --tag mageops/rpm-build:centos-7 && docker run --tty --volume $(pwd):/root/rpmbuild mageops/rpm-build:centos-7 --sign --create-repo && docker push mageops/rpm-build:centos-7
```

```
gpg --gen-key
gpg --export -a 'MageOps Package Manager' > rpm-gpg-key.pub.asc
gpg --export-secret-keys -a 'MageOps Package Manager' > rpm-gpg-key.sec.asc
```

```
travis login --pro
travis encrypt-file --com rpm-gpg-key.sec.asc
```

```
git tag | grep -v legacy | xargs -I{} git push origin :{}
git tag | grep -v legacy | xargs -I{} git tag -d {}
github-remove-all-releases mageops rpm -t $GITHUB_TOKEN
```


--- dummy ---
