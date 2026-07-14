# Upload this package to GitHub

Use the repository name exactly:

```text
partial-moment-stieltjes-quadrature
```

This keeps the URL embedded in the manuscript and `CITATION.cff`
correct:

```text
https://github.com/TurkeyOp/partial-moment-stieltjes-quadrature
```

## GitHub web interface

1. Sign in to GitHub and create a new repository.
2. Set the owner to `TurkeyOp`.
3. Enter the repository name above.
4. Do not initialize it with another README, license, or `.gitignore`.
5. Upload the **contents inside** the unzipped folder, not the outer ZIP
   as a single file.
6. Commit the upload.
7. Run the reproduction command locally or in a GitHub Codespace.
8. Select a license before treating the repository as an open-source
   public release.

## Command-line alternative

```bash
git init
git add .
git commit -m "Initial research release"
git branch -M main
git remote add origin https://github.com/TurkeyOp/partial-moment-stieltjes-quadrature.git
git push -u origin main
```

After the repository is public, verify that the manuscript link opens
and create a release tag such as `v1.0.0-preprint`.
