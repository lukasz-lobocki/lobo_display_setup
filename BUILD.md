# lobo_display_setup

## Typical build workflow

```bash
git add --update
```

```bash
git commit -m "fix: change"
```

```bash
poetry run semantic-release version
```

```bash
git push
```

## Cookiecutter initiation

```bash
cookiecutter \
  ssh://git@github.com/lukasz-lobocki/py-pkgs-cookiecutter.git \
  package_name="lobo_display_setup"
```

### was run with following variables

- package_name: **`lobo_display_setup`**;
package_short_description: `Setting up different displays.`

- package_version: `0.2.2`; python_version: `3.10`

- author_name: `Lukasz Lobocki`;
open_source_license: `CC0 v1.0 Universal`

- __package_slug: `lobo_display_setup`; include_github_actions: `no`

### on

`2023-07-31 14:27:51 +0200`
