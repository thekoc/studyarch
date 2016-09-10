# studyarch

A toolkit that helps you make .stduyarch file for flash card app with python.

Can be used to import flash card for [Studies](http://www.studiesapp.com).

Use class StudyArchive to create a studyarch object and add the content into it.
Then save the file to the appointed location.

Example:

```python
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
```

You will find *.studyarch file in $path_to_save.
