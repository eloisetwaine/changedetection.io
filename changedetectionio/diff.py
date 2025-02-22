# used for the notifications, the front-end is using a JS library

import difflib


def same_slicer(l, a, b):
    if a == b:
        return [l[a]]
    else:
        return l[a:b]

# like .compare but a little different output
def customSequenceMatcher(before, after, include_equal=False, include_removed=True, include_added=True):
    cruncher = difflib.SequenceMatcher(isjunk=lambda x: x in " \\t", a=before, b=after)

    # @todo Line-by-line mode instead of buncghed, including `after` that is not in `before` (maybe unset?)
    for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
        if include_equal and tag == 'equal':
            g = before[alo:ahi]
            yield g
        elif include_removed and tag == 'delete':
            g = ["(removed) " + i for i in same_slicer(before, alo, ahi)]
            yield g
        elif tag == 'replace':
            g = ["(changed) " + i for i in same_slicer(before, alo, ahi)]
            g += ["(into) " + i for i in same_slicer(after, blo, bhi)]
            yield g
        elif include_added and tag == 'insert':
            g = ["(added) " + i for i in same_slicer(after, blo, bhi)]
            yield g

# only_differences - only return info about the differences, no context
# line_feed_sep could be "<br>" or "<li>" or "\n" etc
def render_diff(previous_version_file_contents, newest_version_file_contents, include_equal=False, include_removed=True, include_added=True, line_feed_sep="\n"):

    newest_version_file_contents = [line.rstrip() for line in newest_version_file_contents.splitlines()]

    if previous_version_file_contents:
            previous_version_file_contents = [line.rstrip() for line in previous_version_file_contents.splitlines()]
    else:
        previous_version_file_contents = ""

    rendered_diff = customSequenceMatcher(previous_version_file_contents,
                                          newest_version_file_contents,
                                          include_equal, include_removed, include_added)

    # Recursively join lists
    f = lambda L: line_feed_sep.join([f(x) if type(x) is list else x for x in L])
    return f(rendered_diff)
