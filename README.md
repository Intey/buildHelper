# Helper to build project

Build project in hardcoded directory, by path:
<hardcoded>/<currDir>/<gitBranch><-suffix>.
<-suffix> gotten from parameter.
Also provide ability to pass CMAKE or PROJECT defines. Project defines is just
defines with prepended `projectName_`.

# Requirements
* python2.7/3.4/3.5
* ~~docopt - python library for generate CLI from doc string in .py file.~~

docopt included in repo, but i hope, i get time to exclude it.
