# MKDocs Exclude Unused (orphaned) Files

A simple plugin for excluding files from being included in the mkdocs output if they are not referenced in other pages.  

## Instalation

![pypi current version](https://img.shields.io/pypi/v/mkdocs-exclude-unused-files?style=flat-square)

Run `pip install --upgrade mkdocs-exclude-unused-files`

## Configuration

Basic Configuration in the `mkdocs.yml` file:

```yaml
plugins:
  - mkdocs_exclude_unused_files:
      file_types_to_check: ["png", "jpg", "jpeg", "gif"]
```

This configuration will exclude all files from the final mkdocs output that have one of the configured file endings and are not referenced / linked to in other pages.  

### All Configuration Options

| Setting                      | Default                                                                                                                                                                                                                                                                        | Description                                                                                                                                                                                    |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dry_run                      | False                                                                                                                                                                                                                                                                          | Only print output into the command line and don't actually delete anything                                                                                                                     |
| silent                       | False                                                                                                                                                                                                                                                                          | Don't print out the found orphan files in the build process                                                                                                                                    |
| force_delete                 | False                                                                                                                                                                                                                                                                          | By default the plugin only deletes files that are actually in the configured mkdocs output directory (site_dir). If you want to delete these files anyways due to your setup, enable this flag |
| file_types_to_check          | ["png", "jpg", "jpeg", "gif", "pdf", "ico", "drawio", "tif", "tiff", "zip", "tar.gz", "rar", "ogg", "mp3", "mp4", "vtt ", "ogv", "mov", "svg", "pot", "potx", "ppsx", "ppt", "pptx", "xlt", "xltx", "xls", "xlsx", "doc", "docx", "dot", "dotx", "vst", "vstx", "vsd", "vsdx"] | Only check these file types for their usage and delete them if necessary.                                                                                                                      |
| file_names_to_never_remove   | ["favicon"]                                                                                                                                                                                                                                                                    | Files with these names will never get deleted, even if no usage is detected.                                                                                                                   |
| folders_to_never_remove_from | ["assets"]                                                                                                                                                                                                                                                                     | Files in these folders will never get deleted, even if no usage is detected. Useful for always including specific static files.                                                                |
