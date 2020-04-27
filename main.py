from itertools import groupby

with open("clippings.txt", "r", encoding="utf-8-sig") as f:
    contents = f.read()
splitter = "=========="
split_contents = [c.strip().replace("\ufeff", "") for c in contents.split(splitter)]
print(len(split_contents))


def parse(clipping):
    lines = clipping.split("\n")
    if len(lines) == 1:
        return None
    title, metadata, _, content = lines
    first, datetime = metadata.split("Added on ")
    first = first.split("- Your ")[1].split(" on ")
    kind = first[0]
    location = first[1].strip()
    return title, kind, location, datetime, content


def is_highlight(c) -> bool:
    if c is None:
        return False
    return c[1] == "Highlight"


def title(c):
    return c[0]


highlights = [parse(c) for c in split_contents if is_highlight(parse(c))]
sorted_highlights = sorted(highlights, key=title)


grouped = groupby(sorted_highlights, key=title)
for i, (title, highlight_tuples) in enumerate(grouped):
    highlight_tuples = list(highlight_tuples)  # type: ignore
    print(len(highlight_tuples))  # type: ignore
    with open(f"mds/{i}.md", "w+") as fd:
        split_title = title.rsplit(")")  # type: ignore
        if len(split_title) > 2:
            author = split_title[-2]
            author = author.rsplit("(")[-1]
            title = ")".join(split_title[:-2]) + ")"  # type: ignore
        elif len(split_title) == 2:
            author = split_title[0]
            title, author = author.rsplit("(")
        fd.write(f"# {title}\n\n")
        fd.write(f"## by {author}\n\n")
        for highlight_tuple in highlight_tuples:
            content = highlight_tuple[-1]
            fd.write(f"> {content}")
            fd.write("\n\n")
            fd.write("&nbsp;")
            fd.write("\n\n")
