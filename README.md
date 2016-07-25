# Helper to build project

Build project in hardcoded directory, by path:
<hardcoded>/<currDir>/<gitBranch><-suffix>.
<-suffix> gotten from parameter.
Also provide ability to pass CMAKE or PROJECT defines. Project defines is just
defines with prepended `projectName_`.
