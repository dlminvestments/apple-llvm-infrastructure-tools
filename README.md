# Apple LLVM Infrastructure Tools

This is a collection of tools for maintaining LLVM-project&ndash;related
infrastructure, including CI, automerging, monorepo transition, and others.

## Deploying `git-apple-llvm`

Prerequisites:
- Python 3
- Relatively recent git (git 2.20+ should work)

You can deploy `git-apple-llvm` by running the `install` target:

```
sudo make install                 # Installs into /usr/local/bin
make install PREFIX=/my/directory # Installs into /my/directory/bin
```

You can always uninstall the tools by running the `uninstall` target:

```
sudo make uninstall
```

## More documentation

`cd docs/ && make html && open _build/html/index.html` for more documentation.

<a href="https://codebeat.co/projects/github-com-dlminvestments-apple-llvm-infrastructure-tools-main"><img alt="codebeat badge" src="https://codebeat.co/badges/2be39a97-593e-4c38-80a4-ab9416cff7f4" /></a>
