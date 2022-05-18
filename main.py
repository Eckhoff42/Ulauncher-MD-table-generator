from ctypes import alignment
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
import logging
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)


class MarkdownTableGenerator(Extension):

    def __init__(self):
        super(MarkdownTableGenerator, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def makeTable(self, col, row, alignment="default"):
        alignment = alignment.lower()

        # header row
        output = "|"
        for i in range(col):
            output += f" {i} |"
        output += "\n"

        # separator row
        output += "|"
        for i in range(col):
            if alignment == "center":
                output += ":-:|"
            elif alignment == "left":
                output += ":--|"
            elif alignment == "right":
                output += "--:|"
            else:  # alignment == "default"
                output += "---|"
        output += "\n"

        # rest of table
        for i in range(row):
            output += "|"
            for i in range(col):
                output += "   |"
            output += "\n"

        return output

    def on_event(self, event, extension):
        query = event.get_argument() or str()
        vals = query.split(' ')

        if len(vals) >= 2:
            col = int(vals[0])
            row = int(vals[1])
            alignment = vals[2] if (len(vals) >= 3 and type(
                vals[2]) == str) else "default"
            # create markdown table
            table = self.makeTable(col, row, alignment)

            items = [
                ExtensionResultItem(
                    icon='images/icon.svg',
                    name='create a %s md table' % event.get_argument(),
                    on_enter=CopyToClipboardAction(
                        table),
                )
            ]

        # if no arguments are given, show help
        else:
            items = [
                ExtensionResultItem(
                    icon='images/icon.svg',
                    name='specify table dimension (e.g. "3 4 centered")',
                    on_enter=None,
                )
            ]
        return RenderResultListAction(items)


if __name__ == '__main__':
    MarkdownTableGenerator().run()
