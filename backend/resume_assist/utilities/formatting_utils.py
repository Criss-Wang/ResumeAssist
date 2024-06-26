import markdown
import markdownify
import re
from bs4 import BeautifulSoup


def correct_markdown(text: str) -> str:
    """
    Corrects markdown string to ensure unordered lists and ordered lists have an extra newline before them.

    Following input should have few extra newlines.

    Before:
    =======================
    - unordered list item 1
    blah blah blah
    - unordered list item 2
    + unordered list item 3
    blah blah blah
    1. ordered list item 4
    2. ordered list item 5
    blah blah blah
    * unordered list item 6
    =======================

    After:
    =======================
    - unordered list item 1

    blah blah blah

    - unordered list item 2
    + unordered list item 3

    blah blah blah

    1. ordered list item 4
    2. ordered list item 5

    blah blah blah

    * unordered list item 6
    =======================
    """
    ul_prefixes = ["- ", "* ", "+ "]
    lines = text.split("\n")
    new_lines = []
    for i, line in enumerate(lines):
        if any(line.startswith(ul_prefix) for ul_prefix in ul_prefixes):
            if i > 0 and not any(
                lines[i - 1].startswith(ul_prefix) for ul_prefix in ul_prefixes
            ):
                new_lines.append("")
        elif any(line.startswith(f"{j}. ") for j in "123456789"):
            if i > 0 and not any(
                lines[i - 1].startswith(f"{j}. ") for j in "123456789"
            ):
                new_lines.append("")
        else:
            if i > 0 and any(
                lines[i - 1].startswith(ul_prefix) for ul_prefix in ul_prefixes
            ):
                new_lines.append("")
            elif i > 0 and any(lines[i - 1].startswith(f"{j}. ") for j in "1234566789"):
                new_lines.append("")
        new_lines.append(line)
    text = "\n".join(new_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def convert_from_markdown(text: str, formatting: str = "html") -> str:
    text = correct_markdown(text)
    if formatting == "html":
        text = markdown_to_html(text)
    elif formatting == "markdown":
        text = text
    elif formatting == "slack":
        text = markdown_to_slack(text)
    elif formatting == "ms_teams":
        text = markdown_to_ms_teams(text)
    elif formatting == "plaintext":
        text = markdown_to_plaintext(text)
    return text


def markdown_to_html(text: str) -> str:
    return markdown.markdown(text)


def markdown_to_slack(text: str) -> str:
    # TODO
    return text


def markdown_to_ms_teams(text: str) -> str:
    # TODO
    return text


def markdown_to_plaintext(text: str) -> str:
    text = markdown_to_html(text)
    # TODO: Preserve lists.
    text = "".join(BeautifulSoup(text, features="html5lib").findAll(string=True))
    return text.strip()


def convert_to_markdown(text: str, formatting: str = "html") -> str:
    if formatting == "html":
        text = html_to_markdown(text)
    elif formatting == "markdown":
        text = text
    elif formatting == "slack":
        text = slack_to_markdown(text)
    elif formatting == "ms_teams":
        text = ms_teams_to_markdown(text)
    elif formatting == "plaintext":
        text = plaintext_to_markdown(text)
    text = correct_markdown(text)
    return text


def html_to_markdown(text: str) -> str:
    return markdownify.markdownify(text)


def slack_to_markdown(text: str) -> str:
    # TODO
    return text


def ms_teams_to_markdown(text: str) -> str:
    # TODO
    return text


def plaintext_to_markdown(text: str) -> str:
    return text


if __name__ == "__main__":
    test = """
- unordered list item 1
blah *blah* **blah**
- unordered list item 2
+ unordered list item 3
blah blah blah
1. ordered list item 4
2. ordered list item 5
blah blah blah
* unordered list item 6
""".strip()
    print("===============")
    print("Original:")
    print("===============")
    print(test)
    print("===============")
    print("Corrected:")
    print("===============")
    test_corrected = correct_markdown(test)
    print(test_corrected)
    print("===============")
    print("HTML:")
    print("===============")
    test_html = convert_from_markdown(test, "html")
    print(test_html)
    print("===============")
    print("Back to Markdown:")
    print("===============")
    test_markdown = convert_to_markdown(test_html, "html")
    print(test_markdown)
    print("===============")
    print("Plaintext:")
    print("===============")
    test_plaintext = convert_from_markdown(test, "plaintext")
    print(test_plaintext)
