from typing import Optional

import logging
import os
from os import path
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import unquote

import mkdocs.config
import mkdocs.config.config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


class ExcludeUnusedFilesPluginConfig(mkdocs.config.base.Config):
    dry_run = mkdocs.config.config_options.Type(bool, default=False)
    silent = mkdocs.config.config_options.Type(bool, default=False)
    force_delete = mkdocs.config.config_options.Type(bool, default=False)
    file_types_to_check = mkdocs.config.config_options.Type(list, default=["png", "jpg", "jpeg", "gif", "pdf", "ico"])
    file_names_to_never_remove = mkdocs.config.config_options.Type(list, default=["favicon"])
    folders_to_never_remove_from = mkdocs.config.config_options.Type(list, default=["assets"])


class ExcludeUnusedFilesPlugin(BasePlugin[ExcludeUnusedFilesPluginConfig]):
    asset_files = set()

    @mkdocs.plugins.event_priority(-100)
    def on_files(self, files: Files, config: MkDocsConfig) -> Optional[Files]:
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

            for file_type in self.config.file_types_to_check:
                if file.src_path.endswith(file_type):
                    self.asset_files.add(file.abs_dest_path)
                    break
        return files

    @mkdocs.plugins.event_priority(-100)
    def on_post_page(self, output: str, page: Page, config: MkDocsConfig) -> Optional[str]:
        # todo: allow configuring custom parsers
        # see https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
        soup = BeautifulSoup(output, "html.parser")
        for file in soup.find_all('img'):
            self.asset_files.discard(str(Path(path.join(path.dirname(page.file.abs_dest_path), unquote(file['src']))).resolve()))
        for file in soup.find_all('a'):
            self.asset_files.discard(str(Path(path.join(path.dirname(page.file.abs_dest_path), unquote(file['href']))).resolve()))
        for file in soup.find_all('video'):
            self.asset_files.discard(str(Path(path.join(path.dirname(page.file.abs_dest_path), unquote(file['src']))).resolve()))

        return output

    def on_post_build(self, config: MkDocsConfig) -> None:
        if not self.config.silent:
            log.info("found %s unused assets" % str(len(self.asset_files)))
            log.info(self.asset_files)

        if not self.config.dry_run:
            delete_count = 0
            for file in self.asset_files:
                if not file.startswith(config.site_dir) and not self.config.force_delete:
                    log.warning("cannot delete file, since it's not inside the configured mkdocs site_dir output directory. use the force flag to overwrite")
                    log.warning("file in question: %s" % file)
                    continue

                try:
                    os.remove(file)
                    delete_count += 1
                except OSError as e:
                    log.warning("failed deleting file %s, an error occurred %s" % (e.filename, e.strerror))

            log.info("deleted " + str(delete_count) + " unused assets from final output")
