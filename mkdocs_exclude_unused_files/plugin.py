import logging
import os
from os import path
from pathlib import Path
from typing import Optional, Set
from urllib.parse import unquote

import mkdocs.config
import mkdocs.config.config_options
from bs4 import BeautifulSoup
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


class ExcludeUnusedFilesPluginConfig(mkdocs.config.base.Config):
    enabled = mkdocs.config.config_options.Type(bool, default=True)
    enabled_on_serve = mkdocs.config.config_options.Type(bool, default=False)
    dry_run = mkdocs.config.config_options.Type(bool, default=False)
    silent = mkdocs.config.config_options.Type(bool, default=False)
    force_delete = mkdocs.config.config_options.Type(bool, default=False)
    file_types_to_check = mkdocs.config.config_options.Type(list, default=[])
    file_types_override_mode = mkdocs.config.config_options.Choice(
        choices=["append", "replace", "remove"], default="replace"
    )
    file_names_to_never_remove = mkdocs.config.config_options.Type(list, default=["favicon"])
    folders_to_never_remove_from = mkdocs.config.config_options.Type(list, default=["assets"])
    file_name_suffixes_to_trim = mkdocs.config.config_options.Type(list, default=["#only-light", "#only-dark"])


class ExcludeUnusedFilesPlugin(BasePlugin[ExcludeUnusedFilesPluginConfig]):
    asset_files: Set[str] = set()
    file_types_to_check = [
        "png",
        "jpg",
        "jpeg",
        "gif",
        "pdf",
        "ico",
        "drawio",
        "tif",
        "tiff",
        "zip",
        "rar",
        "tar.gz",
        "ogg",
        "mp3",
        "mp4",
        "vtt ",
        "ogv",
        "mov",
        "svg",
        "pot",
        "potx",
        "ppsx",
        "ppt",
        "pptx",
        "xlt",
        "xltx",
        "xls",
        "xlsx",
        "doc",
        "docx",
        "dot",
        "dotx",
        "vst",
        "vstx",
        "vsd",
        "vsdx",
    ]

    @mkdocs.plugins.event_priority(-100)
    def on_startup(self, *, command, dirty) -> None:
        if not self.config.enabled:
            log.debug("exclude-unused-files plugin disabled")
            return
        # Disable plugin when the documentation is served, i.e., "mkdocs serve" is used
        if command == "serve" and not self.config.enabled_on_serve:
            log.debug("exclude-unused-files plugin disabled while MkDocs is running in 'serve' mode.")
            self.config.enabled = False

        if self.config.enabled:
            if self.config.file_types_override_mode == "append" and self.config.file_types_to_check != []:
                log.debug("extending default file_types_to_check: %s", ", ".join(self.config.file_types_to_check))
                self.file_types_to_check.extend(self.config.file_types_to_check)
            elif self.config.file_types_override_mode == "replace" and self.config.file_types_to_check != []:
                log.debug("replacing default file_types_to_check with: %s", ", ".join(self.config.file_types_to_check))
                self.file_types_to_check = self.config.file_types_to_check
            elif self.config.file_types_override_mode == "remove" and self.config.file_types_to_check != []:
                log.debug("removing from default file_types_to_check: %s", ", ".join(self.config.file_types_to_check))
                for file_type in self.config.file_types_to_check:
                    self.file_types_to_check.remove(file_type)

            self.file_types_to_check = [*set(self.file_types_to_check)]
            log.debug("final file_types_to_check: %s", ", ".join(self.file_types_to_check))

    @mkdocs.plugins.event_priority(-100)
    def on_files(self, files: Files, config: MkDocsConfig) -> Optional[Files]:
        if not self.config.enabled:
            log.debug("exclude-unused-files plugin disabled")
            return None

        for file in files.media_files():
            is_file_dir_excluded_from_analysis = False
            for excluded_folder in self.config.folders_to_never_remove_from:
                if file.src_uri.startswith(path.join(excluded_folder, "")):
                    is_file_dir_excluded_from_analysis = True
                    continue

            if is_file_dir_excluded_from_analysis:
                continue

            if file.name in self.config.file_names_to_never_remove:
                continue

            for file_type in self.file_types_to_check:
                if file.src_path.endswith(file_type):
                    log.debug("asset file: %s", file.abs_dest_path)
                    self.asset_files.add(file.abs_dest_path)
                    break
        return files

    @mkdocs.plugins.event_priority(-100)
    def on_post_page(self, output: str, page: Page, config: MkDocsConfig) -> Optional[str]:
        if not self.config.enabled:
            log.debug("exclude-unused-files plugin disabled")
            return None

        # todo: allow configuring custom parsers
        # see https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
        soup = BeautifulSoup(output, "html.parser")

        html_tags = {}
        html_tags["a"] = "href"
        html_tags["area"] = "href"
        html_tags["link"] = "href"
        html_tags["img"] = "src"
        html_tags["video"] = "src"
        html_tags["audio"] = "src"
        html_tags["embed"] = "src"
        html_tags["iframe"] = "src"
        html_tags["source"] = "src"
        html_tags["track"] = "src"

        for tag, attr in html_tags.items():
            for file in soup.find_all(tag, {attr: True}):
                if unquote(file[attr]).startswith(("http://", "https://")):
                    continue

                path_check = path.join(path.dirname(page.file.abs_dest_path), unquote(file[attr]))
                for suffix in self.config.file_name_suffixes_to_trim:
                    if path_check.endswith(suffix):
                        path_check = path_check[: -len(suffix)]

                if path.exists(Path(path_check).resolve()):
                    discarded_path = str(Path(path_check).resolve())
                    log.debug("discarded path: %s", discarded_path)
                    self.asset_files.discard(discarded_path)

        return output

    def on_post_build(self, config: MkDocsConfig) -> None:
        if not self.config.enabled:
            log.debug("exclude-unused-files plugin disabled")
            return None

        if not self.config.silent:
            log.info("found %s unused assets", str(len(self.asset_files)))
            log.debug(self.asset_files)

        if not self.config.dry_run:
            delete_count = 0
            for file in self.asset_files:
                if not file.startswith(config.site_dir) and not self.config.force_delete:
                    log.warning(
                        "cannot delete file, since it's not inside the configured "
                        "mkdocs site_dir output directory. "
                        "use the force flag to overwrite"
                    )
                    log.warning("file in question: %s", str(file))
                    continue

                try:
                    os.remove(file)
                    delete_count += 1
                except OSError as error:
                    log.warning("failed deleting file %s, an error occurred %s", str(error.filename), error.strerror)

            log.info("deleted %s unused assets from final output", str(delete_count))
