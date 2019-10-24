from invoke import task


@task
def tag(c):
    version = None
    with open("meshioReader.py") as fh:
        for line in fh:
            if line.startswith("__version__"):
                version = eval(line.partition(" = ")[2])
                break
    assert version is not None
    print(f"Tagging v{version}...")
    c.run(f"git tag v{version}")
    c.run("git push --tags")
