"""This module allows you to create studyarch file through python.

Use class StudyArchive to create a studyarch object and add the content into it.
Then save the file to the appointed location.

Example:
    ::
        from stduy_archive_tool import StudyArchive
        arch = StudyArchive(path_to_save)
        group = arch.add_group('group1')
        group_in_group = group.add_group('group2')
        group_in_group = add_content(
            [
                {
                    'Text': 'text1',
                    'Audio': 'path/to/audio',
                    'Image': 'path/to/image'
                },
                # ...
            ]
        )
        arch.dump()

    You will find *.studyarch file in $path_to_save.
"""

import os
import shutil
import csv
from functools import reduce


def _safe_mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)


class _Container(object):
    """This is the basic container that contains words and metadata.

    Use add_content to append new word.
    Use dump_contents to save data into files.
    """

    def __init__(self):
        self.contents = []

    def add_content(self, content):
        """Add new content into container.

        Args:
            content (list): The content is a list whose each element is a dict
                represents a facet optionally has the keys: 'text', 'image', 'audio'.

                The value of 'text' must be string.
                The value of 'image' must be the path of the image in local.
                The value of 'audio' must be the path of the audio in local.

        Example:
            ::
                content = [
                    {
                        'Iext': 'example text',
                        'Image': '/path/to/the/file',
                        'Audio': '/path/to/the/file'
                    },
                    {
                        'Text': 'example text',
                        'Image': None
                    },
                ]
        """
        self.contents.append(content)

    def dump_contents(self, directory):
        """Dump the contents into the given directory.

        Args:
            directory (str): The path of the directory into which you want to dump.
        """
        def dump_resource(content):
            resource_types = ['audio', 'image']
            for r in resource_types:
                for facet in content:
                    if facet.get(r):
                        path = facet[r]
                        relative_path = os.path.split(path)[1]
                        shutil.copy(path, relative_path)
                        facet[r] = relative_path

        if self.contents:
            with open(os.path.join(directory, 'Data.csv'), 'w') as csvfile:
                facet_numebr = max([len(c) for c in self.contents])

                # set the column
                field_names = []
                for i in range(1, facet_numebr + 1):
                    field_names += [str(i) + ' Text', str(i) + ' Image', str(i) + ' Audio']

                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                for content in self.contents:
                    dump_resource(content)
                    csv_contents = [
                        dict(
                            [('%d %s' % (index + 1, name), value)
                                for name, value in facet.items()]
                        )
                        for index, facet in enumerate(content)
                    ]
                    row = {}
                    for item in csv_contents:
                        row.update(item)

                    writer.writerow(row)


class Group(_Container):
    def __init__(self, name, directory):
        super(Group, self).__init__()
        self.directory = directory
        _safe_mkdir(directory)
        self.groups = []

    def dump(self):
        self.dump_contents(self.directory)
        for group in self.groups:
            group.dump()

    def add_group(self, name):
        directory = os.path.join(self.directory, name)
        group = Group(name, directory)
        self.groups.append(group)
        return group


class StudyArchive(_Container):
    """A study archive can add elements and dump to file.

    Args:
        directory (str): The path into which you want to dump archive.

    Raises:
        TypeError: If the directory is not a directory or doesn't exisits.
    """

    def __init__(self, directory):
        super(StudyArchive, self).__init__()
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not os.path.isdir(directory):
            TypeError(
                'The directory must be a directory liked it\'s name said!',
                'Not this:', directory, '!'
            )

        self.groups = []
        self.base_directory = directory
        self.zip_directory = os.path.join(directory, 'zip_directory')
        self.directory = os.path.join(self.zip_directory, 'Archive')
        self.group_directory = os.path.join(self.directory, 'Groups')
        _safe_mkdir(self.group_directory)

    def add_group(self, name):
        directory = os.path.join(self.group_directory, name)
        group = Group(name, directory)
        self.groups.append(group)
        return group

    def dump(self):
        """Dump the content into local directory."""
        self.dump_contents(self.directory)
        for group in self.groups:
            group.dump()
        dump_arch_path = os.path.join(self.base_directory, 'arch')
        shutil.make_archive(
            dump_arch_path,
            'zip', root_dir=self.zip_directory
        )
        shutil.move(
            dump_arch_path + '.zip',
            os.path.join(self.base_directory, 'arch.studyarch')
        )


if __name__ == '__main__':
    x = StudyArchive('.')
