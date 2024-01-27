# MkDocs Exclude Unused (orphaned) Files

A simple plugin for excluding files from being included in the mkdocs output if they are not referenced on other pages.

## Installation

![pypi current version](https://img.shields.io/pypi/v/mkdocs-exclude-unused-files?style=flat-square)

Run `pip install --upgrade mkdocs-exclude-unused-files`

## Configuration

Basic Configuration in the `mkdocs.yml` file:

```yaml
plugins:
  - exclude-unused-files:
      file_types_to_check: ["png", "jpg", "jpeg", "gif"]
      enabled: !ENV [CI, false]
```

This configuration will exclude all files from the final mkdocs output that has one of the configured file endings and are not referenced/linked to other pages.

### Default types

The plugin uses a default set of file types:

`png, jpg, jpeg, gif, pdf, ico, drawio, tif, tiff, zip, tar.gz, rar, ogg, mp3, mp4, vtt , ogv, mov, svg, pot, potx, ppsx, ppt, pptx, xlt, xltx, xls, xlsx, doc, docx, dot, dotx, vst, vstx, vsd, vsdx`

### All Configuration Options

| Setting                      | Default                         | Description                                                                                                                                                                                                                                  |
|------------------------------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| enabled                      | `True`                          | Whether the plugin is enabled when building your project. If you want to switch the plugin off, e.g. for local builds, use an [environment variables](https://www.mkdocs.org/user-guide/configuration/#environment-variables).               |
| enabled_on_serve             | `False`                         | Whether the plugin is enabled when serving your project. It does not apply if `enabled` is False. It's just to explicitly enable the plugin during mkdocs serve.                                                                             |
| dry_run                      | `False`                         | Only print output into the command line and don't actually delete anything                                                                                                                                                                   |
| silent                       | `False`                         | Don't print out the found orphan files in the build process                                                                                                                                                                                  |
| force_delete                 | `False`                         | By default the plugin only deletes files that are actually in the configured mkdocs output directory (site_dir). If you want to delete these files anyways due to your setup, enable this flag                                               |
| file_types_to_check          | `[]`                            | Only check these file types for their usage and delete them if necessary.                                                                                                                                                                    |
| file_types_override_mode     | `replace`                       | Behavior of `file_types_to_check` towards default types: `replace` - uses only defined types, `append` - adds additional types to default list, `remove` - removes specified types from default.                                             |
| file_names_to_never_remove   | `["favicon"]`                   | Files with these names will never get deleted, even if no usage is detected.                                                                                                                                                                 |
| folders_to_never_remove_from | `["assets"]`                    | Files in these folders will never get deleted, even if no usage is detected. Useful for always including specific static files.                                                                                                              |
| file_name_suffixes_to_trim   | `["#only-light", "#only-dark"]` | Trim-away suffixes in this list when checking if a file-name is used. This is used for ignoring material-mkdoc's color-palette-toggle instructions (see [Issue-4](https://github.com/JonasDoesThings/mkdocs-exclude-unused-files/issues/4)). |
