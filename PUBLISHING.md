# Publishing tidypolars-extra to PyPI

This guide walks you through all the steps needed to publish `tidypolars-extra` to PyPI.

## Prerequisites

### 1. Create Accounts

- **PyPI**: Register at https://pypi.org/account/register/
- **TestPyPI**: Register at https://test.pypi.org/account/register/

### 2. Set Up Trusted Publishing (OIDC)

The publish workflow uses `pypa/gh-action-pypi-publish` with OIDC trusted publishing, so no API tokens are needed. You need to register this repository as a trusted publisher on both sites.

**On TestPyPI** — go to https://test.pypi.org/manage/account/publishing/ and add a new pending publisher:

| Field           | Value              |
|-----------------|--------------------|
| Owner           | `mdmanurung`       |
| Repository      | `tidypolars-extra` |
| Workflow name   | `publish.yml`      |
| Environment     | `testpypi`         |

**On PyPI** — go to https://pypi.org/manage/account/publishing/ and add a new pending publisher:

| Field           | Value              |
|-----------------|--------------------|
| Owner           | `mdmanurung`       |
| Repository      | `tidypolars-extra` |
| Workflow name   | `publish.yml`      |
| Environment     | `pypi`             |

### 3. Create GitHub Environments

The publish workflow references two GitHub environments. Go to your repository **Settings → Environments** and create:

- `testpypi`
- `pypi`

Consider adding protection rules (e.g., required reviewers) on the `pypi` environment for safety.

## Publishing a Release

### 1. Update the Version

Bump the version in `pyproject.toml`:

```toml
version = "0.1.0"
```

### 2. Update the Changelog

Add a new entry to `CHANGELOG.md` documenting the changes in this release.

### 3. Verify the Build Locally

```bash
pip install build
python -m build
```

This creates `dist/tidypolars_extra-<version>.tar.gz` and `dist/tidypolars_extra-<version>-py3-none-any.whl`. Inspect them to verify the right files are included:

```bash
# Check wheel contents
python -m zipfile -l dist/tidypolars_extra-*.whl

# Check sdist contents
tar tzf dist/tidypolars_extra-*.tar.gz
```

### 4. Create a GitHub Release

1. Go to your repository → **Releases → Create a new release**
2. Create a new tag matching the version (e.g., `v0.1.0`)
3. Fill in the release title and notes
4. Click **Publish release**

The publish workflow will automatically:
1. Build the package
2. Publish to TestPyPI
3. Publish to PyPI

### 5. Verify the Published Package

```bash
# Test install from TestPyPI
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ tidypolars-extra

# Test install from PyPI (after it propagates)
pip install tidypolars-extra
```

> **Note**: The `--extra-index-url` flag for TestPyPI ensures that dependencies (like `polars`, `numpy`, etc.) are still resolved from the real PyPI.

## Troubleshooting

### Build Failures

If `python -m build` fails, make sure `hatchling` is installed:

```bash
pip install hatchling
```

### Publish Workflow Failures

- **403 Forbidden**: Verify the trusted publisher is configured correctly on PyPI/TestPyPI (owner, repo, workflow name, and environment must match exactly).
- **Environment not found**: Make sure the `testpypi` and `pypi` environments exist in your repository settings.
- **Version conflict**: PyPI does not allow re-uploading the same version. Bump the version in `pyproject.toml` before creating a new release.
